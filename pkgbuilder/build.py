#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v3.1.5
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2014, Kwpolska.
# See /LICENSE for licensing information.

"""
    pkgbuilder.build
    ~~~~~~~~~~~~~~~~

    Functions for building packages.

    :Copyright: © 2011-2014, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, _
import pkgbuilder.exceptions
import pkgbuilder.package
import pkgbuilder.ui
import pkgbuilder.utils
import sys
import os
import pyalpm
import requests
import requests.exceptions
import re
import tarfile
import subprocess
import functools
import glob

__all__ = ['validate', 'install', 'safeupgrade', 'auto_build', 'download',
           'rsync', 'extract', 'prepare_deps', 'depcheck', 'fetch_runner',
           'build_runner']


def validate(pkgnames):
    """Check if packages were installed."""
    DS.fancy_msg(_('Validating installation status...'))
    DS.log.info('Validating: ' + '; '.join(pkgnames))
    DS.pycreload()
    localdb = DS.pyc.get_localdb()

    aurpkgs = {aurpkg.name: aurpkg.version for aurpkg in
               pkgbuilder.utils.info(pkgnames)}

    wrong = len(pkgnames)

    for pkgname in pkgnames:
        lpkg = localdb.get_pkg(pkgname)
        try:
            aurversion = aurpkgs[pkgname]
        except KeyError:
            if not lpkg:
                DS.fancy_error2(_('{0}: not an AUR package').format(
                                pkgname))
            else:
                wrong -= 1
                DS.fancy_msg2(_('{0}: installed {1}').format(pkgname,
                                                             lpkg.version))
        else:
            if not lpkg:
                DS.fancy_error2(_('{0}: NOT installed').format(pkgname))
            else:
                if pyalpm.vercmp(aurversion, lpkg.version) > 0:
                    DS.fancy_error2(_('{0}: outdated {1}').format(
                        pkgname, lpkg.version))
                else:
                    wrong -= 1
                    DS.fancy_msg2(_('{0}: installed {1}').format(
                        pkgname, lpkg.version))

    return wrong


def install(pkgpaths, sigpaths, asdeps, uopt=''):
    """Install packages through ``pacman -U``."""
    DS.fancy_msg(_('Installing built packages...'))

    DS.log.info('pkgs={0}; sigs={1}'.format(pkgpaths, sigpaths))
    DS.log.debug('cp {0} {1} /var/cache/pacman/pkg/'.format(pkgpaths,
                                                            sigpaths))
    DS.sudo(['cp'] + pkgpaths + sigpaths + ['/var/cache/pacman/pkg/'])

    if asdeps:
        uopt = (uopt + ' --asdeps').strip()

    if uopt:
        DS.log.debug('$PACMAN -U {0} {1}'.format(uopt, pkgpaths))
        DS.sudo([DS.paccommand, '-U', uopt] + pkgpaths)
    else:
        DS.log.debug('$PACMAN -U {0}'.format(pkgpaths))
        DS.sudo([DS.paccommand, '-U'] + pkgpaths)


def safeupgrade(pkgname):
    """Perform a safe upgrade of PKGBUILDer."""
    DS.fancy_msg(_('Fetching package information...'))
    pkg = pkgbuilder.utils.info([pkgname])[0]
    DS.fancy_msg2('-'.join((pkg.name, pkg.version)))
    filename = pkg.name + '.tar.gz'
    DS.fancy_msg(_('Downloading the tarball...'))
    downloadbytes = download(pkg.urlpath, filename)
    kbytes = int(downloadbytes) / 1000
    DS.fancy_msg2(_('{0} kB downloaded').format(kbytes))

    DS.fancy_msg(_('Extracting...'))
    DS.fancy_msg2(_('{0} files extracted').format(extract(filename)))
    os.chdir('./{0}/'.format(pkg.name))
    DS.fancy_msg(_('Building {0}...').format(pkg.name))

    if DS.uid == 0:
        DS.fancy_warning(_('Performing a safe upgrade as root!'))
        DS.fancy_warning2(_('It is recommended to restart PKGBUILDer as a '
                            'regular user instead.'))
        asroot = ' --asroot'
    else:
        asroot = ''
    mpstatus = subprocess.call('makepkg -sicf{0}'.format(asroot), shell=True)
    DS.fancy_msg(_('Build finished with return code {0}.').format(mpstatus))
    return mpstatus


def auto_build(pkgname, performdepcheck=True,
               pkginstall=True, completelist=[]):
    """
    NOT the actual build function.
    This function makes building AUR deps possible.
    If you can, use it.


    .. note::

        This function returns a list of packages to install with pacman -U.
        Please take care of it.  Running PKGBUILDer/PBWrapper standalone or
        .main.main() will do that.
    """
    build_result = build_runner(pkgname, performdepcheck, pkginstall)
    os.chdir('../')
    try:
        if build_result[0] == 0:
            DS.fancy_msg(_('The build function reported a proper build.'))
        elif build_result[0] >= 0 and build_result[0] < 256:
            raise pkgbuilder.exceptions.MakepkgError(build_result[0])
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
                install(toinstall2, sigs2, True)

            if DS.validate:
                validate(build_result[1])

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


def download(urlpath, filename):
    """Downloads an AUR tarball to the current directory."""
    try:
        r = requests.get('https://aur.archlinux.org' + urlpath)
        r.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        raise pkgbuilder.exceptions.ConnectionError(str(e), e)
    except requests.exceptions.HTTPError as e:
        raise pkgbuilder.exceptions.HTTPError(r, e)
    except requests.exceptions.RequestException as e:
        raise pkgbuilder.exceptions.NetworkError(str(e), e)

    # Sanity check.
    if r.headers['content-length'] == '0':
        raise pkgbuilder.exceptions.SanityError(_('0 bytes downloaded'),
                                                source=r)

    f = open(filename, 'wb')
    f.write(r.content)
    f.close()
    return r.headers['content-length']


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


def extract(filename):
    """Extracts an AUR tarball."""
    thandle = tarfile.open(filename, 'r:gz')
    thandle.extractall()
    names = thandle.getnames()
    thandle.close()
    if names:
        return len(names)
    else:
        raise pkgbuilder.exceptions.SanityError(_('No files extracted.'),
                                                names)


def prepare_deps(pkgbuild_path):
    """Gets (make)depends from a PKGBUILD and returns them."""
    # Back in the  day,  there  was  a  comment  praising  replacing  pyparsing
    # with shell magic.   It  claimed  that  we  will  have  no  fuckups  ever.
    #  OF  COURSE  WE  DID.   SPLIT  PACKAGES.   PKGBUILDer  crashed  when   it
    # encountered one.  Here comes the output from sh:
    #
    #  PKGBUILD: line  XX: `package_package-name': not a valid identifier
    #
    # shell=True with subprocess.check_output() uses  /bin/sh,  which  is  more
    # strict than /bin/bash used by makepkg.
    #
    # So, I replaced it  by  a  call  to  /usr/bin/bash  (which  is  equivalent
    # to /bin/bash on Arch Linux).
    #
    # And if the PKGBUILD is malicious, we speed up the destroying of the  user
    # system by about 10 seconds,  so  it  makes  no  sense  not  to  do  this.
    # Moreover, it takes only 7 lines instead of  about  40  in  the  pyparsing
    # implementation.
    #
    # PS.  I am amazed that `bash -c`  ignores  !events.   That  saved  me  one
    #      replace.  I am also amazed that it ignored \a and \n.
    #
    # FULL DISCLOSURE:  the  following  path  was  used  to  test  the  current
    #                   implementation.    I    may    have    not    noticed
    #                   something  else  that  is   not   accounted   for   by
    #                   this  very  path,   so   if   you   know   that   some
    #                   breakage  occurs,  tell me.
    #
    # I am an "idiot"/no, 'really'/exclamation!mark, seriously/backsl\ash/a\n

    ppath = pkgbuild_path.replace('"', r'\"').join(('"', '"'))

    deps = subprocess.check_output(('/usr/bin/bash', '-c', 'source ' +
                                    ppath + ';for i in ${depends[*]};'
                                    'do echo $i;done;for i in '
                                    '${makedepends[*]};do echo $i; done'))
    deps = deps.decode('utf-8')
    deps = deps.split('\n')

    return deps


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
    """Performs a dependency check."""
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
                pm.msg(_('retrieving {0}').format(pkg.name), True)
                filename = pkg.name + '.tar.gz'
                download(pkg.urlpath, filename)

            print(':: ' + _('Extracting AUR packages...'))
            for pkg in aurpkgs:
                filename = pkg.name + '.tar.gz'
                extract(filename)

        print(_('Successfully fetched: ') + ' '.join(pkgnames))
    except pkgbuilder.exceptions.PBException as e:
        print(':: ERROR: ' + str(e.msg))
        exit(1)


def build_runner(pkgname, performdepcheck=True,
                 pkginstall=True):
    """
    A build function, which actually links to others.  Do not use it
    unless you re-implement auto_build.
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

        os.chdir('./{0}/'.format(pkg.repo))
    else:
        filename = pkg.name + '.tar.gz'
        DS.fancy_msg(_('Downloading the tarball...'))
        downloadbytes = download(pkg.urlpath, filename)
        kbytes = int(downloadbytes) / 1000
        DS.fancy_msg2(_('{0} kB downloaded').format(kbytes))

        DS.fancy_msg(_('Extracting...'))
        DS.fancy_msg2(_('{0} files extracted').format(extract(filename)))
    os.chdir('./{0}/'.format(pkg.name))

    if performdepcheck:
        DS.fancy_msg(_('Checking dependencies...'))
        depends = prepare_deps(os.path.abspath('./PKGBUILD'))
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
            return [72337, aurbuild]

    mpparams = ''

    if DS.cleanup:
        mpparams += ' -c'

    if DS.uid == 0:
        mpparams += ' --asroot'

    mpstatus = subprocess.call('makepkg -sf' + mpparams,
                               shell=True)

    if pkginstall:
        toinstall = find_packagefile(os.getcwd())
    else:
        toinstall = ([], [])

    if pkg.is_abs:
        os.chdir('../')

    return [mpstatus, toinstall]
