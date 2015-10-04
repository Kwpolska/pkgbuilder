# -*- encoding: utf-8 -*-
# PKGBUILDer v4.2.4
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2015, Chris Warrick.
# See /LICENSE for licensing information.

"""
Build AUR packages.

:Copyright: © 2011-2015, Chris Warrick.
:License: BSD (see /LICENSE).
"""

from . import DS, _
import pkgbuilder.aur
import pkgbuilder.exceptions
import pkgbuilder.package
import pkgbuilder.transaction
import pkgbuilder.ui
import pkgbuilder.utils
import sys
import os
import platform
import pyalpm
import srcinfo.parse
import re
import subprocess
import functools
import glob

__all__ = ('auto_build', 'clone', 'rsync', 'prepare_deps', 'depcheck',
           'fetch_runner', 'build_runner')


def auto_build(pkgname, performdepcheck=True,
               pkginstall=True, completelist=[]):
    """A function that builds everything, that should be used by everyone.

    This function makes building AUR deps possible.
    If you can, use it.


    .. note::

        This function returns a list of packages to install with pacman -U.
        Please take care of it.  Running PKGBUILDer/PBWrapper standalone or
        .__main__.main() will do that.

    """
    build_result = build_runner(pkgname, performdepcheck, pkginstall)
    try:
        if build_result[0] == 0:
            DS.fancy_msg(_('The build succeeded.'))
        elif build_result[0] >= 0 and build_result[0] < 256:
            raise pkgbuilder.exceptions.MakepkgError(build_result[0])
        elif build_result[0] == 72336:
            # existing package, do nothing
            pass
        elif build_result[0] == 72337:
            DS.fancy_warning(_('Building more AUR packages is required.'))
            toinstall2 = []
            sigs2 = []
            for pkgname2 in build_result[1]:
                toinstall = []
                if pkgname2 in completelist:
                    if (completelist.index(pkgname2) <
                            completelist.index(pkgname)):
                        # Already built the package.
                        toinstall, sigs = find_packagefile(
                            os.path.join(os.getcwd(), pkgname2))
                        if toinstall:
                            DS.fancy_msg2(_('found an existing package for '
                                            '{0}').format(pkgname2))
                        # Note that the package will be reinstalled later.
                        # This, however, isn’t a problem.
                    else:
                        # We won’t rebuild it and reinstall it later.  Doing
                        # that solely because I can and because this won’t
                        # introduce hacks.
                        completelist.remove(pkgname2)

                if not toinstall:
                    try:
                        br = auto_build(
                            pkgname2, performdepcheck, pkginstall,
                            build_result[1])
                        toinstall, sigs = br[1]
                    except IndexError:
                        return br

                toinstall2 += toinstall
                sigs2 += sigs

            if toinstall2:
                tx = pkgbuilder.transaction.Transaction(
                    pkgnames=build_result[1],
                    pkgpaths=toinstall2,
                    sigpaths=sigs2,
                    asdeps=True,
                    filename=pkgbuilder.transaction.generate_filename(),
                    delete=True)
                tx.run(standalone=False, validate=DS.validation)

            return auto_build(pkgname, performdepcheck, pkginstall,
                              completelist)

        return build_result
    # Non-critical exceptions that shouldn’t crash PKGBUILDer as a whole are
    # handled here.  Some are duplicated for various reasons.
    except pkgbuilder.exceptions.MakepkgError as e:
        DS.fancy_error(_('makepkg (or someone else) failed and '
                         'returned {0}.').format(e.retcode))
        return []
    except pkgbuilder.exceptions.AURError as e:
        DS.fancy_error(str(e))
        return []
    except pkgbuilder.exceptions.PackageError as e:
        DS.fancy_error(str(e))
        return []


def clone(pkgbase):
    """Clone or update a git repo.

    .. versionadded:: 4.0.0
    """
    if os.path.exists('./{0}/'.format(pkgbase)):
        if os.path.exists('./{0}/.git'.format(pkgbase)):
            # git repo, pull
            try:
                os.chdir(pkgbase)
                subprocess.check_call(['git', 'pull'])
            except subprocess.CalledProcessError as e:
                raise pkgbuilder.exceptions.CloneError(e.returncode)
            finally:
                os.chdir('..')
        else:
            raise pkgbuilder.exceptions.ClonePathExists(pkgbase)
    else:
        repo_url = pkgbuilder.aur.AUR.base + '/' + pkgbase + '.git'
        if DS.deepclone:
            cloneargs = []
        else:
            cloneargs = ['--depth', '1']
        try:
            subprocess.check_call(['git', 'clone'] + cloneargs +
                                  [repo_url, pkgbase])
        except subprocess.CalledProcessError as e:
            raise pkgbuilder.exceptions.CloneError(e.returncode)


def rsync(pkg, quiet=False):
    """Run rsync for a package."""
    if quiet:
        qv = '--quiet'
    else:
        qv = '--verbose'
    return DS.run_command(['rsync', qv, '-mr', '--no-motd', '--delete-after',
                           '--no-p', '--no-o', '--no-g',
                           '--include=/{0}'.format(pkg.repo),
                           '--include=/{0}/{1}'.format(pkg.repo, pkg.name),
                           '--exclude=/{0}/*'.format(pkg.repo), '--exclude=/*',
                           'rsync.archlinux.org::abs/{0}/'.format(pkg.arch),
                           '.'])


def _check_and_append(data, field, out):
    """Check if `field` exists in `data`, and if it does, append to `out`."""
    if field in data:
        out += data[field]


def prepare_deps(srcinfo_path, pkgname=None):
    """Get (make)depends from a .SRCINFO file and returns them.

    (pkgname is now discarded, because it messes up one-build split packages.)

    .. versionchanged:: 4.0.1

    In the past, this function used to get data via `bash -c`.
    """
    arch = platform.machine()

    with open(srcinfo_path, encoding='utf-8') as fh:
        raw = fh.read()

    data, errors = srcinfo.parse.parse_srcinfo(raw)
    if errors:
        raise pkgbuilder.exceptions.PackageError(
            'malformed .SRCINFO: {0}'.format(errors), 'prepare_deps')
    all_depends = []
    _check_and_append(data, 'depends', all_depends)
    _check_and_append(data, 'makedepends', all_depends)
    _check_and_append(data, 'depends_' + arch, all_depends)
    _check_and_append(data, 'makedepends_' + arch, all_depends)
    for pdata in data['packages'].values():
        _check_and_append(pdata, 'depends', all_depends)
        _check_and_append(pdata, 'makedepends', all_depends)
        _check_and_append(pdata, 'depends_' + arch, all_depends)
        _check_and_append(pdata, 'makedepends_' + arch, all_depends)

    depends = []
    for d in all_depends:
        if d not in depends:
            depends.append(d)
    return depends


def _test_dependency(available, difference, wanted):
    """Test a dependency requirement."""
    if '-' in available:
        # Stripping the pkgver.
        available = available.split('-')[0]

    vercmp = pyalpm.vercmp(available, wanted)

    return (('<' in difference and vercmp == -1) or
            ('=' in difference and vercmp == 0) or
            ('>' in difference and vercmp == 1))


def depcheck(depends, pkgobj=None):
    """Perform a dependency check."""
    if depends == []:
        # THANK YOU, MAINTAINER, FOR HAVING NO DEPS AND DESTROYING ME!
        return {}
    else:
        parseddeps = {}
        localpkgs = DS.pyc.get_localdb().pkgcache
        syncpkgs = []
        for j in [i.pkgcache for i in DS.pyc.get_syncdbs()]:
            syncpkgs.append(j)
        syncpkgs = functools.reduce(lambda x, y: x + y, syncpkgs)
        for dep in depends:
            if dep == '':
                continue

            if re.search('[<=>]', dep):
                vpat = ('>=<|><=|=><|=<>|<>=|<=>|>=|=>|><|<>|=<|'
                        '<=|>|=|<')
                ver_base = re.split(vpat, dep)
                fdep = dep
                dep = ver_base[0]
                try:
                    ver = ver_base[1]
                    diff = re.match('{0}(.*){1}'.format(dep, ver),
                                    fdep).groups()[0]
                except IndexError:
                    # No version requirement, no need to bother.  We do the
                    # actual checks later not to waste time.
                    pass
                else:
                    depmatch = False
                    lsat = pyalpm.find_satisfier(localpkgs, dep)
                    if lsat:
                        depmatch = _test_dependency(lsat.version, diff, ver)
                        parseddeps[dep] = 0

                    if not depmatch:
                        ssat = pyalpm.find_satisfier(syncpkgs, dep)
                        if ssat:
                            depmatch = _test_dependency(ssat.version, diff,
                                                        ver)
                            parseddeps[dep] = 1

                        if not depmatch:
                            asat = pkgbuilder.utils.info([dep])
                            if asat:
                                depmatch = _test_dependency(asat[0].version,
                                                            diff, ver)
                                parseddeps[dep] = 2

                            if not depmatch:
                                raise pkgbuilder.exceptions.PackageError(
                                    _('Failed to fulfill package dependency '
                                      'requirement: {0}').format(fdep),
                                    req=fdep, source=pkgobj)

            if dep not in parseddeps:
                if pyalpm.find_satisfier(localpkgs, dep):
                    parseddeps[dep] = 0
                elif pyalpm.find_satisfier(syncpkgs, dep):
                    parseddeps[dep] = 1
                elif pkgbuilder.utils.info([dep]):
                    parseddeps[dep] = 2
                else:
                    raise pkgbuilder.exceptions.PackageNotFoundError(
                        dep, 'depcheck')

        return parseddeps


def find_packagefile(pdir):
        """Find a package file (*.pkg.tar.xz) and signatures, if any."""
        # .pkg.tar.xz FTW, but some people change that.
        # (note that PKGBUILDs can do it, too!)
        # Moreover, dumb PKGBUILDs can remove that `.pkg.tar` part.  `makepkg`s
        # `case` switch for PKGEXT uses: *tar *tar.xz *tar.gz *.tar.bz2
        #                                *tar.lrz *tar.lzo *.tar.Z
        # …and a catch-all that shows a warning and makes a .tar anyways.
        # I decided to leave it in, because we would catch e.g. source tarballs
        # or ANYTHING, REALLY if I did not.
        pkgfilestr = os.path.abspath(os.path.join(pdir, '*-*-*.pkg.tar*{0}'))

        # We use sets so we can do stuff easier down there.
        #
        # Originally, this code was much longer, completely ignored
        # split packages and other shenanigans.  Moreover, the first two
        # asterisk wildcards in the pkgfilestr were format-tokens.  Three tests
        # occurred:
        #
        # 1. pkg.name; pkg.version; ''
        # 2. pkg.name; date in yyyymmdd format (old practice); ''
        # 3. pkg.name; *; * [called “crappy packages”]
        #
        # To add insult to injury: if-elif-elif.

        pkgs = set(glob.glob(pkgfilestr.format('')))
        sigs = set(glob.glob(pkgfilestr.format('.sig')))

        return list(pkgs - sigs), list(sigs)


def fetch_runner(pkgnames, preprocessed=False):
    """Run the fetch procedure."""
    abspkgs = []
    aurpkgs = []
    allpkgs = []
    try:
        if preprocessed:
            allpkgs = pkgnames
            pkgnames = [p.name for p in allpkgs]
        else:
            print(':: ' + _('Fetching package information...'))
            for pkgname in pkgnames:
                pkg = None
                try:
                    pkg = pkgbuilder.utils.info([pkgname])[0]
                except IndexError:
                    try:
                        DS.log.info('{0} not found in the AUR, checking in '
                                    'ABS'.format(pkgname))
                        syncpkgs = []
                        for j in [i.pkgcache for i in DS.pyc.get_syncdbs()]:
                            syncpkgs.append(j)
                        syncpkgs = functools.reduce(lambda x, y: x + y,
                                                    syncpkgs)
                        abspkg = pyalpm.find_satisfier(syncpkgs, pkgname)
                        pkg = pkgbuilder.package.ABSPackage.from_pyalpm(abspkg)

                    except AttributeError:
                        pass
                allpkgs.append(pkg)

        for pkg in allpkgs:
            if not pkg:
                raise pkgbuilder.exceptions.PackageNotFoundError(pkgname,
                                                                 'fetch')
            if pkg.is_abs:
                abspkgs.append(pkg)
            else:
                aurpkgs.append(pkg)

        if abspkgs:
            print(_(':: Retrieving packages from abs...'))
            pm = pkgbuilder.ui.Progress(len(abspkgs))
            for pkg in abspkgs:
                pm.msg(_('retrieving {0}').format(pkg.name), True)
                rc = rsync(pkg, True)
                if rc > 0:
                    raise pkgbuilder.exceptions.NetworkError(
                        _('Failed to retieve {0} (from ABS/rsync).').format(
                            pkg.name), pkg=pkg, retcode=rc)

        if aurpkgs:
            print(_(':: Retrieving packages from aur...'))
            pm = pkgbuilder.ui.Progress(len(aurpkgs))
            for pkg in aurpkgs:
                pm.msg(_('cloning {0}').format(pkg.packagebase), True)
                clone(pkg.packagebase)

        print(_('Successfully fetched: ') + ' '.join(pkgnames))
    except pkgbuilder.exceptions.PBException as e:
        print(':: ERROR: ' + str(e.msg))
        exit(1)


def build_runner(pkgname, performdepcheck=True,
                 pkginstall=True):
    """A build function, which actually links to others.

    DO NOT use it unless you re-implement auto_build!

    """
    pkg = None
    try:
        pkg = pkgbuilder.utils.info([pkgname])[0]
    except IndexError:
        DS.log.info('{0} not found in the AUR, checking in ABS'.format(
            pkgname))
        syncpkgs = []
        for j in [i.pkgcache for i in DS.pyc.get_syncdbs()]:
            syncpkgs.append(j)
        syncpkgs = functools.reduce(lambda x, y: x + y, syncpkgs)
        abspkg = pyalpm.find_satisfier(syncpkgs, pkgname)
        if abspkg:  # abspkg can be None or a pyalpm.Package object.
            pkg = pkgbuilder.package.ABSPackage.from_pyalpm(abspkg)

    if not pkg:
        raise pkgbuilder.exceptions.PackageNotFoundError(pkgname, 'build')

    DS.fancy_msg(_('Building {0}...').format(pkg.name))
    pkgbuilder.utils.print_package_search(pkg,
                                          prefix=DS.colors['blue'] +
                                          '  ->' + DS.colors['all_off'] +
                                          DS.colors['bold'] + ' ',
                                          prefixp='  -> ')
    sys.stdout.write(DS.colors['all_off'])
    if pkg.is_abs:
        DS.fancy_msg(_('Retrieving from ABS...'))
        rc = rsync(pkg)
        if rc > 0:
            raise pkgbuilder.exceptions.NetworkError(
                _('Failed to retieve {0} (from ABS/rsync).').format(
                    pkg.name), pkg=pkg, retcode=rc)

        existing = find_packagefile(pkg.name)
        if any(pkg.name in i for i in existing[0]):
            DS.fancy_msg(_('Found an existing package for '
                           '{0}').format(pkgname))
            if not pkginstall:
                existing = ([], [])
            return [72336, existing]
        try:
            os.chdir('./{0}/{1}'.format(pkg.repo, pkg.name))
        except FileNotFoundError:
            raise pkgbuilder.exceptions.PBException(
                'The package download failed.\n    This package might '
                'be generated from a split PKGBUILD.  Please find out the '
                'name of the “main” package (eg. python- instead of python2-) '
                'and try again.', '/'.join((pkg.repo, pkg.name)), exit=False)
    else:
        existing = find_packagefile(pkg.packagebase)
        if any(pkg.name in i for i in existing[0]):
            DS.fancy_msg(_('Found an existing package for '
                           '{0}').format(pkgname))
            if not pkginstall:
                existing = ([], [])
            return [72336, existing]
        DS.fancy_msg(_('Cloning the git repository...'))
        clone(pkg.packagebase)
        os.chdir('./{0}/'.format(pkg.packagebase))
        if not os.path.exists('.SRCINFO'):
            raise pkgbuilder.exceptions.EmptyRepoError(pkg.packagebase)

    if performdepcheck:
        DS.fancy_msg(_('Checking dependencies...'))
        depends = prepare_deps(os.path.abspath('./.SRCINFO'))
        deps = depcheck(depends, pkg)
        pkgtypes = [_('found in system'), _('found in repos'),
                    _('found in the AUR')]
        aurbuild = []
        if not deps:
            DS.fancy_msg2(_('none found'))

        for dpkg, pkgtype in deps.items():
            if pkgtype == 2:
                aurbuild.append(dpkg)

            DS.fancy_msg2(': '.join((dpkg, pkgtypes[pkgtype])))
        if aurbuild != []:
            os.chdir('../')
            return [72337, aurbuild]

    mpparams = ['makepkg', '-sf']

    if DS.clean:
        mpparams.append('-c')

    if not DS.pgpcheck:
        mpparams.append('--skippgpcheck')

    if not DS.confirm:
        mpparams.append('--noconfirm')

    if not DS.depcheck:
        mpparams.append('--nodeps')

    if not DS.colors_status:
        mpparams.append('--nocolor')

    DS.log.info("Running makepkg: {0}".format(mpparams))
    mpstatus = subprocess.call(mpparams, shell=False)
    DS.log.info("makepkg status: {0}".format(mpstatus))

    if pkginstall:
        toinstall = find_packagefile(os.getcwd())
    else:
        toinstall = ([], [])

    if pkg.is_abs:
        os.chdir('../../')
    else:
        os.chdir('../')

    DS.log.info("Found package files: {0}".format(toinstall))

    return [mpstatus, toinstall]
