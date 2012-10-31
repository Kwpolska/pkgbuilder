#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.1.5.8
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2012, Kwpolska.
# See /LICENSE for licensing information.

# Names convention: pkg = a package object, pkgname = a package name.

"""
    pkgbuilder.build
    ~~~~~~~~~~~~~~~~
    Functions for building packages.

    :Copyright: © 2011-2012, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, _, PBError
from .utils import Utils
import sys
import os
import pyalpm
import pycman
import requests
import re
import tarfile
import subprocess
import functools
import glob
import datetime


### Build       build functions and helpers ###
class Build:
    """Functions for building packages."""

    utils = Utils()
    aururl = '{}://aur.archlinux.org{}'

    def validate(self, pkgnames):
        """Check if packages were installed."""
        DS.fancy_msg(_('Validating installation status...'))
        DS.log.info('Validating: ' + '; '.join(pkgnames))
        pyc = pycman.config.init_with_config('/etc/pacman.conf')
        localdb = pyc.get_localdb()

        aurpkgs = {i['Name']: i['Version'] for i in self.utils.info(pkgnames)}

        for pkgname in pkgnames:
            pkg = localdb.get_pkg(pkgname)
            try:
                aurversion = aurpkgs[pkgname]
            except KeyError:
                if not pkg:
                    DS.fancy_error2(_('{}: not an AUR package').format(
                                    pkgname))
                else:
                    DS.fancy_msg2(_('{}: installed {}').format(pkgname,
                                  pkg.version))
            else:
                if not pkg:
                    DS.fancy_error2(_('{}: NOT installed').format(pkgname))
                else:
                    if pyalpm.vercmp(aurversion, pkg.version) > 0:
                        DS.fancy_error2(_('{}: outdated {}').format(pkgname,
                                        pkg.version))
                    else:
                        DS.fancy_msg2(_('{}: installed {}').format(pkgname,
                                      pkg.version))

    def install(self, pkgpaths, sigpaths=[]):
        """Install packages through ``pacman -U``."""
        DS.fancy_msg(_('Installing built packages...'))

        DS.log.info('pkgs={}; sigs={}'.format(pkgpaths, sigpaths))
        DS.log.debug('cp {} {} /var/cache/pacman/pkg/'.format(pkgpaths,
                                                              sigpaths))
        DS.sudo('cp', pkgpaths + sigpaths, '/var/cache/pacman/pkg/')
        DS.log.debug('$PACMAN -U {}'.format(pkgpaths))
        DS.sudo(DS.paccommand, '-U', pkgpaths)

    def auto_build(self, pkgname, performdepcheck=True,
                   pkginstall=True):
        """
        NOT the actual build function.
        This function makes building AUR deps possible.
        If you can, use it.


        .. note::

            This function returns a list of packages to install with pacman -U.
            Please take care of it.  Running PKGBUILDer/PBWrapper standalone or
            .main.main() will do that.
        """
        build_result = self.build_runner(pkgname, performdepcheck,
                                         pkginstall)
        os.chdir('../')
        try:
            if build_result[0] == 0:
                DS.fancy_msg(_('The build function reported a proper build.'))

            elif build_result[0] >= 0 and build_result[0] < 72000:  # PBxxx.
                raise PBError(_('makepkg (or someone else) failed and '
                                'returned {}.').format(build_result[0]))
                exit(build_result[0])
            elif build_result[0] == 72789:  # PBSUX.
                raise PBError(_('PKGBUILDer had a problem.'))
                exit(1)
            elif build_result[0] == 72101:  # I/O error.
                raise PBError(_('There was an input/output error.'))
                exit(1)
            elif build_result[0] == 72337:  # PBDEP.
                DS.fancy_warning(_('Building more AUR packages is required.'))
                toinstall2 = []
                sigs2 = []
                for pkgname2 in build_result[1]:
                    (toinstall, sigs) = self.auto_build(pkgname2,
                                                        performdepcheck,
                                                        pkginstall)[0]
                    toinstall2 += toinstall
                    sigs2 += sigs

                if toinstall2 and sigs2:
                    self.install(toinstall2, sigs2)

                if DS.validate:
                    self.validate(build_result[1])

                # Setting all the deps installed to be marked as such.  Using
                # pacman because I need root, and I can’t get one there.
                DS.sudo(DS.paccommand, '-D', '--asdeps', build_result[1])

                self.auto_build(pkgname, performdepcheck,
                                pkginstall)

            return build_result
        except PBError as inst:
            DS.fancy_error(str(inst))

    def download(self, urlpath, filename, prot='http'):
        """Downloads an AUR tarball (http) to the current directory."""
        r = requests.get(self.aururl.format(prot, urlpath))

        # Error handling.
        if r.status_code != 200:
            raise PBError(_('download: HTTP Error {}').format(
                r.status_code))
        elif r.headers['content-length'] == '0':
            raise PBError(_('download: 0 bytes downloaded'))

        f = open(filename, 'wb')
        f.write(r.content)
        f.close()
        return r.headers['content-length']

    def extract(self, filename):
        """Extracts an AUR tarball."""
        thandle = tarfile.open(filename, 'r:gz')
        thandle.extractall()
        names = thandle.getnames()
        thandle.close()
        if names != []:
            return len(names)
        else:
            raise PBError(_('extract: no files extracted'))

    def prepare_deps(self, pkgbuild):
        """Gets (make)depends from a PKGBUILD and returns them."""
        # I decided to use Popen instead of pyparsing magic.  Less deps
        # for PB itself and no problems if makedepends are before depends
        # in the file.  (eg. python-gitdb)
        # And it takes only 7 lines instead of about 40 in the pyparsing
        # implementation.

        deps = subprocess.check_output('source ' + pkgbuild + '; for i in '
                                       '${depends[*]}; do echo $i; done; for '
                                       'i in ${makedepends[*]}; do echo $i; '
                                       'done',
                                       shell=True)
        deps = deps.decode('utf-8')
        deps = deps.split('\n')

        return deps

    def depcheck(self, depends):
        """Performs a dependency check."""
        if depends == []:
            # THANK YOU, MAINTAINER, FOR HAVING NO DEPS AND DESTROYING ME!
            return {}
        else:
            parseddeps = {}
            pyc = pycman.config.init_with_config('/etc/pacman.conf')
            localpkgs = pyc.get_localdb().pkgcache
            syncpkgs = []
            for j in [i.pkgcache for i in pyc.get_syncdbs()]:
                syncpkgs.append(j)
            syncpkgs = functools.reduce(lambda x, y: x + y, syncpkgs)
            for dep in depends:
                if dep == '':
                    continue

                if re.search('[<=>]', dep):
                    vpat = ('>=<|><=|=><|=<>|<>=|<=>|>=|=>|><|<>|=<|'
                            '<=|>|=|<')
                    ver_base = re.split(vpat, dep)
                    dep = ver_base[0]

                if pyalpm.find_satisfier(localpkgs, dep):
                    parseddeps[dep] = 0
                elif pyalpm.find_satisfier(syncpkgs, dep):
                    parseddeps[dep] = 1
                elif self.utils.info([dep]):
                    parseddeps[dep] = 2
                else:
                    parseddeps[dep] = -1
                    raise PBError(_('depcheck: cannot find {} '
                                    'anywhere').format(dep))
            return parseddeps

    def build_runner(self, pkgname, performdepcheck=True,
                     pkginstall=True):
        """
        A build function, which actually links to others.  Do not use it
        unless you re-implement auto_build.
        """
        try:
            pkg = None
            try:
                pkg = self.utils.info([pkgname])
                pkg = pkg[0]
                useabs = False
            except IndexError:
                try:
                    DS.log.info('{} not found in the AUR, checking in '
                                'ABS'.format(pkgname))
                    pyc = pycman.config.init_with_config('/etc/pacman.conf')
                    syncpkgs = []
                    for j in [i.pkgcache for i in pyc.get_syncdbs()]:
                        syncpkgs.append(j)
                    syncpkgs = functools.reduce(lambda x, y: x + y, syncpkgs)
                    abspkg = pyalpm.find_satisfier(syncpkgs, pkgname)
                    pkg = {'CategoryID': '0', 'Category': abspkg.db.name,
                            'Name': abspkg.name, 'Version': abspkg.version,
                            'Description': abspkg.desc, 'OutOfDate': '0',
                            'NumVotes': 'n/a', 'Arch': abspkg.arch}
                    useabs = True
                except AttributeError:
                    pass

            if not pkg:
                raise PBError(_('Package {} not found.').format(pkgname))

            pkgname = pkg['Name']
            DS.fancy_msg(_('Building {}...').format(pkgname))
            self.utils.print_package_search(pkg,
                                            prefix=DS.colors['blue'] +
                                            '  ->' + DS.colors['all_off'] +
                                            DS.colors['bold'] + ' ',
                                            prefixp='  -> ')
            sys.stdout.write(DS.colors['all_off'])
            if useabs:
                DS.fancy_msg(_('Synchronizing the ABS tree...'))
                rsync = ['rsync', '-mrtv', '--no-motd', '--delete-after',
                         '--no-p', '--no-o', '--no-g', # '--delete-excluded',
                         '--include=/{}'.format(pkg['Category']),
                         '--include=/{}/{}'.format(pkg['Category'],
                             pkg['Name']),
                         '--exclude=/{}/*'.format(pkg['Category']),
                         '--exclude=/*',
                         'rsync.archlinux.org::abs/{}/'.format(pkg['Arch']),
                         '.']
                rstatus = subprocess.call(rsync)
                if rstatus > 0:
                    raise PBError(_('Failed to synchronize the ABS tree.'))

                os.chdir('./{}/'.format(pkg['Category']))
            else:
                filename = pkgname + '.tar.gz'
                DS.fancy_msg(_('Downloading the tarball...'))
                downloadbytes = self.download(pkg['URLPath'], filename)
                kbytes = int(downloadbytes) / 1000
                DS.fancy_msg2(_('{} kB downloaded').format(kbytes))

                DS.fancy_msg(_('Extracting...'))
                DS.fancy_msg2(_('{} files extracted').format(self.extract(
                    filename)))
            os.chdir('./{}/'.format(pkgname))

            if performdepcheck:
                DS.fancy_msg(_('Checking dependencies...'))
                depends = self.prepare_deps(os.path.abspath('./PKGBUILD'))
                deps = self.depcheck(depends)
                pkgtypes = [_('found in system'), _('found in repos'),
                            _('found in the AUR')]
                aurbuild = []
                if not deps:
                    DS.fancy_msg2(_('none found'))

                for dpkg, pkgtype in deps.items():
                    # I checked for -1 here.  Dropped this one as it was
                    # handled by the depcheck function already.
                    if pkgtype == 2:
                        aurbuild.append(dpkg)

                    DS.fancy_msg2('{}: {}'.format(dpkg,
                                                  pkgtypes[pkgtype]))
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
                # .pkg.tar.xz FTW, but some people change that.
                pkgfilestr = os.path.abspath('./{}-{}-{}.pkg.*')
                # I hope nobody builds VCS packages at 23:5* local.  And if
                # they do, they will be caught by the 2nd fallback (crappy
                # packages)
                datep = datetime.date.today().strftime('%Y%m%d')
                att0 = set(glob.glob(pkgfilestr.format(pkgname,
                                     pkg['Version'], '*')))
                att1 = set(glob.glob(pkgfilestr.format(pkgname, datep, '*')))
                att2 = set(glob.glob(pkgfilestr.format(pkgname, '*', '*')))
                sigf = set(glob.glob(pkgfilestr.format(pkgname, '*', '*' +
                                                       'sig')))
                if not sigf:
                    sigf = set()
                att0 = list(att0 - sigf)
                att1 = list(att1 - sigf)
                att2 = list(att2 - sigf)
                if att0:
                    # Standard run, for humans.
                    toinstall = [att0, list(sigf)]
                elif att1:
                    # Fallback #1, for VCS packages
                    toinstall = [att1, list(sigf)]
                elif att2:
                    # Fallback #2, for crappy packages
                    toinstall = [att2, list(sigf)]
                else:
                    toinstall = [None, None]
            else:
                toinstall = [None, None]

            return [mpstatus, toinstall, useabs]
        except PBError as inst:
            DS.fancy_error(str(inst))
            return [72789, None]
        except IOError as inst:
            DS.fancy_error(str(inst))
            return [72101, None]
