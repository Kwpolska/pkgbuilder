#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.1.3.1
# An AUR helper/library.
# Copyright (C) 2011-2012, Kwpolska.
# See /LICENSE for licensing information.

# Names convention: pkg = a package object, pkgname = a package name.

"""
    pkgbuilder.Build
    ~~~~~~~~~~~~~~~~
    Functions for building packages.

    :Copyright: (C) 2011-2012, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, T, _, PBError
from .utils import Utils
from pyparsing import OneOrMore, Word
import os
import pyalpm
import pycman
import requests
import re
import tarfile
import subprocess
import functools


### Build       build functions and helpers ###
class Build:
    """Functions for building packages."""

    def __init__(self):
        """Build init.

:Arguments: none.
:Input: none.
:Output: none.
:Returns: a Build object.
:Exceptions: none.
:Message codes: none."""
        self.utils = Utils()
        self.aururl = '{0}://aur.archlinux.org{1}'

    def auto_build(self, pkgname, validate=True, performdepcheck=True,
                   makepkginstall=True):
        """NOT the actual build function.
This function makes validation and building AUR deps possible.
If you can, use it.

:Arguments: package name, validate installation, perform dependency checks.
:Input: none.
:Output: text.
:Returns: nothing.
:Exceptions: PBError.
:Message codes:
    WRN3401, ERR3402, INF3450, ERR3451, ERR3452.
:Former data:
    2.0 Name: build."""
        build_result = self.build_runner(pkgname, performdepcheck,
                                         makepkginstall)
        try:
            if build_result[0] == 0:
                DS.fancy_msg(_('The build function reported a proper build.'))
                os.chdir('../')
                if validate:
                    # check if installed
                    H = pycman.config.init_with_config('/etc/pacman.conf')
                    localdb = H.get_localdb()
                    pkg = localdb.get_pkg(pkgname)
                    aurversion = self.utils.info(pkgname)['Version']
                    if pkg is None:
                        DS.fancy_error2(_('[ERR3451] validation: NOT \
installed'))
                    else:
                        if pyalpm.vercmp(aurversion, pkg.version) > 0:
                            DS.fancy_error2(_('[ERR3452] validation: \
outdated {0}').format(pkg.version))
                        else:
                            DS.fancy_msg2(_('[INF3450] validation: \
installed {0}').format(pkg.version))
            elif build_result[0] >= 0 and build_result[0] <= 15:
                os.chdir('../')
                raise PBError(_('[ERR3402] Something went wrong.  \
EC={0} EM={1}').format(build_result[0], build_result[1]))
            elif build_result[0] == 16:
                os.chdir('../')
                DS.fancy_warning(_('[WRN3401] Building more AUR packages is \
required.'))
                for pkgname2 in build_result[1]:
                    self.auto_build(pkgname2, validate, performdepcheck,
                                    makepkginstall)
                self.auto_build(pkgname, validate, performdepcheck,
                                makepkginstall)
        except PBError as inst:
            DS.fancy_error(str(inst))

    def download(self, urlpath, filename, prot='http'):
        """Downloads an AUR tarball (http) to the current directory.

:Arguments: URL, filename for saving, protocol.
:Input: none.
:Output: none.
:Returns: bytes downloaded.
:Exceptions:
    PBError, IOError, requests.exceptions.*
:Message codes: ERR3101, ERR3102."""
        r = requests.get(self.aururl.format(prot, urlpath))

        # Error handling.
        if r.status_code != 200:
            raise PBError(_('[ERR3102] download: HTTP Error {0}').format(
                r.status_code))
        elif r.headers['content-length'] == '0':
            raise PBError(_('[ERR3101] download: 0 bytes downloaded'))

        f = open(filename, 'wb')
        f.write(r.content)
        f.close()
        return r.headers['content-length']

    def extract(self, filename):
        """Extracts an AUR tarball.

:Arguments: filename.
:Input: none.
:Output: none.
:Returns: file count.
:Exceptions: PBError, IOError.
:Message codes: ERR3151."""
        thandle = tarfile.open(filename, 'r:gz')
        thandle.extractall()
        names = thandle.getnames()
        thandle.close()
        if names != []:
            return len(names)
        else:
            raise PBError(_('[ERR3151] extract: no files extracted'))

    def prepare_deps(self, pkgbuild):
        """Gets (make)depends from a PKGBUILD and returns them.

:Arguments: PKGBUILD contents
:Input: none.
:Output: none.
:Returns:
    a list with entries from PKGBUILD's depends and makedepends
    (can be empty.)
:Exceptions: IOError.
:Message codes: none."""
        fixedp = '0123456789abcdefghijklmnopqrstuvwxyz\
ABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&*+,-./:;<=>?@[]^_`{|}~"\''
        pattern1 = 'depends=(' + OneOrMore(Word(fixedp)) + ')'
        pattern2 = 'makedepends=(' + OneOrMore(Word(fixedp)) + ')'

        try:
            bashdepends = next(pattern1.scanString(pkgbuild))
        except StopIteration:
            bashdepends = []
            depends = []
        try:
            bmdepends = next(pattern2.scanString(pkgbuild))
        except StopIteration:
            bmdepends = []
            makedepends = []
        if bashdepends != []:
            depends = [s.rstrip() for s in bashdepends[0][1:-1]]
        if bmdepends != []:
            makedepends = [s.rstrip() for s in bmdepends[0][1:-1]]

        bothdepends = depends + makedepends
        return [s.replace('"', '').replace('\'', '') for s in bothdepends]

    def depcheck(self, depends):
        """Performs a dependency check.

:Arguments: a python dependency list.
:Input: none.
:Output: none.
:Returns:
    a dict, key is the package name, and value is: -1 = nowhere, 0 = system,
    1 = repos, 2 = AUR.
:Exceptions: PBError.
:Message codes: ERR3201.
:Former data:
    2.0 Returns: no -1"""
        if depends == []:
            # THANK YOU, MAINTAINER, FOR HAVING NO DEPS AND DESTROYING ME!
            return {}
        else:
            parseddeps = {}
            H = pycman.config.init_with_config('/etc/pacman.conf')
            localpkgs = H.get_localdb().pkgcache
            syncpkgs = []
            for j in [i.pkgcache for i in H.get_syncdbs()]:
                syncpkgs.append(j)
            syncpkgs = functools.reduce(lambda x, y: x + y, syncpkgs)
            for dep in depends:
                if re.search('[<=>]', dep):
                    vpat = '>=<|><=|=><|=<>|<>=|<=>|>=|=>|><|<>|=<|\
<=|>|=|<'
                    ver_base = re.split(vpat, dep)
                    dep = ver_base[0]
                if pyalpm.find_satisfier(localpkgs, dep):
                    parseddeps[dep] = 0
                elif pyalpm.find_satisfier(syncpkgs, dep):
                    parseddeps[dep] = 1
                elif self.utils.info(dep) is not None:
                    parseddeps[dep] = 2
                else:
                    parseddeps[dep] = -1
                    raise PBError(_('[ERR3201] depcheck: cannot find {0} \
anywhere').format(dep))
            return parseddeps

    def build_runner(self, pkgname, performdepcheck=True,
                     makepkginstall=True):
        """A build function, which actually links to others.  Do not use it
unless you re-implement auto_build.

:Arguments: pkgname, perform dependency checks.
:Input: none.
:Output: text.
:Returns: ::
    [makepkg's/auto_build's retcode OR 16 if an AUR dep is needed,
        [AUR deps or retcode source]]
:Exceptions: PBError.
:Message codes: ERR3001, ERR3201, ERR3202.
:Former data:
    2.0 Behavior: all functions inside

    2.0 Name: buildSub"""
        try:
            # exists
            pkg = self.utils.info(pkgname)
            if pkg is None:
                raise PBError(_('[ERR3001] Package {0} not found.').format(
                              pkgname))
            pkgname = pkg['Name']
            DS.fancy_msg(_('Building {0}...').format(pkgname))
            self.utils.print_package_search(pkg,
                                            prefix=DS.colors['blue'] +
                                            '  ->' + DS.colors['all_off'] +
                                            DS.colors['bold'] + ' ',
                                            prefixp='  -> ')
            filename = pkgname + '.tar.gz'
            # Okay, this package exists, great then.  Thanks, user.

            DS.fancy_msg(_('Downloading the tarball...'))
            downloadbytes = self.download(pkg['URLPath'], filename)
            kbytes = int(downloadbytes) / 1000
            DS.fancy_msg2(_('{0} kB downloaded').format(kbytes))

            DS.fancy_msg(_('Extracting...'))
            DS.fancy_msg2(_('{0} files extracted').format(self.extract(
                filename)))
            os.chdir('./' + pkgname + '/')
            if performdepcheck:
                DS.fancy_msg(_('Checking dependencies...'))
                try:
                    fhandle = open('./PKGBUILD', 'rb')
                    pbcontents = fhandle.read().decode('utf8', 'ignore')
                    fhandle.close()
                    depends = self.prepare_deps(pbcontents)
                    deps = self.depcheck(depends)
                    pkgtypes = [_('found in system'), _('found in repos'),
                                _('found in the AUR')]
                    aurbuild = []
                    if deps == {}:
                        DS.fancy_msg2(_('none found'))

                    for pkg, pkgtype in deps.items():
                        if pkgtype == -1:
                            raise PBError(_('[ERR3201] depcheck: cannot \
find {0} anywhere').format(pkg))
                        if pkgtype == 2:
                            aurbuild.append(pkg)

                        DS.fancy_msg2('{0}: {1}'.format(pkg,
                                                        pkgtypes[pkgtype]))
                    if aurbuild != []:
                        return [16, aurbuild]
                except UnicodeDecodeError as inst:
                    DS.fancy_error2(_('[ERR3202] depcheck: UnicodeDecodeEr\
ror.  The PKGBUILD cannot be read.  There are invalid UTF-8 characters (\
eg. in the Maintainer field.)  Error message: {0}').format(str(inst)))

            mpparams = ''

            if makepkginstall is not False:
                mpparams = mpparams + 'i'

            if os.geteuid() == 0:
                mpparams = mpparams + ' --asroot'

            return [subprocess.call('/usr/bin/makepkg -s' + mpparams,
                    shell=True), 'makepkg']
        except PBError as inst:
            DS.fancy_error(str(inst))
            return [3, ['pb']]
        except requests.exceptions.ConnectionError as inst:
            DS.fancy_error(str(inst))
            return [3, ['requests.exceptions.ConnectionError']]
        except requests.exceptions.HTTPError as inst:
            DS.fancy_error(str(inst))
            return [3, ['requests.exceptions.HTTPError']]
        except requests.exceptions.Timeout as inst:
            DS.fancy_error(str(inst))
            return [3, ['requests.exceptions.Timeout']]
        except requests.exceptions.TooManyRedirects as inst:
            DS.fancy_error(str(inst))
            return [3, ['requests.exceptions.TooManyRedirects']]
        except IOError as inst:
            DS.fancy_error(str(inst))
            return [3, ['io']]
