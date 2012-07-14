#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.1.2.30
# A Python AUR helper/library.
# Copyright (C) 2011-2012, Kwpolska.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the author of this software nor the names of
#    contributors to this software may be used to endorse or promote
#    products derived from this software without specific prior written
#    consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Names convention: pkg = a package object, pkgname = a package name.

"""PKGBUILDer.  An AUR helper."""
from pyparsing import OneOrMore, Word   # python-pyparsing from [community]
import pyalpm                           # pyalpm in [extra]
import pycman                           # pyalpm in [extra]
import argparse
import sys
import os
import json
import re
import urllib.request
import urllib.error
import tarfile
import subprocess
import datetime
import gettext
import functools

VERSION = '2.1.2.30'
T = gettext.translation('pkgbuilder', '/usr/share/locale', fallback='C')
_ = T.gettext

### PBDS            PB global data storage  ###
class PBDS:
    """PKGBUILDer Data Storage."""
    def __init__(self):
        """PBDS init.

:Arguments: none.
:Input: none.
:Output: none.
:Returns: a PBDS object.
:Exceptions: none.
:Message codes: none."""
        # For fancy-schmancy messages stolen from makepkg.
        self.colors = {
                        'all_off':    '\x1b[1;0m',
                        'bold':       '\x1b[1;1m',
                        'blue':       '\x1b[1;1m\x1b[1;34m',
                        'green':      '\x1b[1;1m\x1b[1;32m',
                        'red':        '\x1b[1;1m\x1b[1;31m',
                        'yellow':     '\x1b[1;1m\x1b[1;33m'
                      }
        self.pacman = False
        self.validate = True
        self.depcheck = True
        self.mkpginst = True
        self.categories = ['ERROR', 'ERROR', 'daemons', 'devel',
                           'editors', 'emulators', 'games', 'gnome',
                           'i18n', 'kde', 'lib', 'modules', 'multimedia',
                           'network', 'office', 'science', 'system', 'x11',
                           'xfce', 'kernels']
        self.inttext = _('[ERR5001] Aborted by user! Exiting…')

    def colorson(self):
        """Colors on.

:Arguments: none.
:Input: none.
:Output: none.
:Returns: nothing.
:Exceptions: none.
:Message codes: none."""
        self.colors = {
                        'all_off':    '\x1b[1;0m',
                        'bold':       '\x1b[1;1m',
                        'blue':       '\x1b[1;1m\x1b[1;34m',
                        'green':      '\x1b[1;1m\x1b[1;32m',
                        'red':        '\x1b[1;1m\x1b[1;31m',
                        'yellow':     '\x1b[1;1m\x1b[1;33m'
                      }


    def colorsoff(self):
        """Colors off.

:Arguments: none.
:Input: none.
:Output: none.
:Returns: nothing.
:Exceptions: none.
:Message codes: none."""
        self.colors = {
                        'all_off':    '',
                        'bold':       '',
                        'blue':       '',
                        'green':      '',
                        'red':        '',
                        'yellow':     ''
                      }

# Useless since python3-aur was replaced, but we'd make use of it.
def pblog(msg, tofile = False, tostderr = False):
    """A log function.  Executed when requested and by fancy_*.

:Arguments: a message, write logs to file, write logs to stderr.
:Input: none.
:Output: none.
:Returns: nothing.
:Exceptions: none.
:Message codes: none."""
    if tofile == True:
        open('pkgbuilder.log', 'a').write(msg)

    if tostderr == True:
        sys.stderr.write(msg)

DS = PBDS()

# Fancy-schmancy messages stolen from makepkg.
def fancy_msg(text):
    """makepkg's msg().  Use for main messages.

:Arguments: a message.
:Input: none.
:Output: text.
:Returns: nothing.
:Exceptions: none.
:Message codes: none."""
    sys.stderr.write(DS.colors['green']+'==>'+DS.colors['all_off']+
                     DS.colors['bold']+' '+text+DS.colors['all_off']+'\n')
    pblog('(auto fancy_msg    ) '+text)

def fancy_msg2(text):
    """makepkg's msg2().  Use for sub-messages.

:Arguments: a message.
:Input: none.
:Output: text.
:Returns: nothing.
:Exceptions: none.
:Message codes: none."""
    sys.stderr.write(DS.colors['blue']+'  ->'+DS.colors['all_off']+
                     DS.colors['bold']+' '+text+DS.colors['all_off']+'\n')
    pblog('(auto fancy_msg2   ) '+text)

def fancy_warning(text):
    """makepkg's warning().  Use when you have problems.

:Arguments: a message.
:Input: none.
:Output: text.
:Returns: nothing.
:Exceptions: none.
:Message codes: none."""
    sys.stderr.write(DS.colors['yellow']+'==> '+_('WARNING:')+
                     DS.colors['all_off']+DS.colors['bold']+' '+text+
                     DS.colors['all_off']+'\n')
    pblog('(auto fancy_warning) '+text)

def fancy_error(text):
    """makepkg's error().  Use for errors.  Exitting is suggested.

:Arguments: a message.
:Input: none.
:Output: text.
:Returns: nothing.
:Exceptions: none.
:Message codes: none."""
    sys.stderr.write(DS.colors['red']+'==> '+_('ERROR:')+
                     DS.colors['all_off']+DS.colors['bold']+
                     ' '+text+DS.colors['all_off']+'\n')
    pblog('(auto fancy_error  ) '+text)

def fancy_error2(text):
    """like fancy_error, but looks like a sub-message (fancy_msg2).

:Arguments: a message.
:Input: none.
:Output: text.
:Returns: nothing.
:Exceptions: none.
:Message codes: none."""
    sys.stderr.write(DS.colors['red']+'  ->'+DS.colors['all_off']+
                     DS.colors['bold']+' '+text+DS.colors['all_off']+'\n')
    pblog('(auto fancy_error2 ) '+text)

### PBError         errors raised here      ###
class PBError(Exception):
    """Exceptions raised by the PKGBUILDer."""

    def __init__(self, msg):
        """PBError init.

:Arguments: a message.
:Input: none.
:Output: none.
:Returns: nothing.
:Exceptions: none.
:Message codes: none."""
        self.msg = msg

    def __str__(self):
        """You want to see error messages, don't you?"""
        return self.msg


### AUR             AUR RPC calls           ###
class AUR:
    """A class for calling the AUR API.  Basics only."""

    def __init__(self):
        """AUR init.

:Arguments: none.
:Input: none.
:Output: none.
:Returns: an AUR object.
:Exceptions: none.
:Message codes: none."""
        self.rpc = '{0}://aur.archlinux.org/rpc.php?type={1}&arg={2}'
        self.mrpc = '{0}://aur.archlinux.org/rpc.php?type=multiinfo{1}'

    def jsonreq(self, rtype, arg, prot = 'http'):
        """Makes a request and returns plain JSON data.

:Arguments: request type, argument (package name), protocol.
:Input: none.
:Output: none.
:Returns: JSON data from the API.
:Exceptions: urllib.error.URLError, urllib.error.HTTPError.
:Message codes: none."""
        rhandle = urllib.request.urlopen(self.rpc.format(prot, rtype, arg))
        return rhandle.read().decode()

    def jsonmultiinfo(self, args, prot = 'http'):
        """Makes a multiinfo request and returns plain JSON data.

:Arguments: a list of packages, protocol.
:Input: none.
:Output: none.
:Returns: JSON data from the API.
:Exceptions: urllib.error.URLError, urllib.error.HTTPError.
:Message codes: none."""
        urlargs = '&arg[]='+'&arg[]='.join(args)
        rhandle = urllib.request.urlopen(self.mrpc.format(prot, urlargs))
        return rhandle.read().decode()

    def request(self, rtype, arg, prot = 'http'):
        """Makes a request.

:Arguments: request type, argument (package name), protocol.
:Input: none.
:Output: none.
:Returns: data from the API.
:Exceptions: urllib.error.URLError, urllib.error.HTTPError.
:Message codes: none."""
        return json.loads(self.jsonreq(rtype, arg, prot))

    def multiinfo(self, args, prot = 'http'):
        """Makes a multiinfo request.

:Arguments: a list of packages, protocol.
:Input: none.
:Output: none.
:Returns: data from the API.
:Exceptions: urllib.error.URLError, urllib.error.HTTPError.
:Message codes: none."""

        return json.loads(self.jsonmultiinfo(args, prot))

### Utils           common global utilities ###
class Utils:
    """Common global utilities.  Provides useful data."""

    def __init__(self):
        """Utils init.

:Arguments: none.
:Input: none.
:Output: none.
:Returns: a Utils object."""
        self.aur = AUR()
    def info(self, pkgname):
        """Returns info about a package.

:Arguments: package name.
:Input: none.
:Output: none.
:Returns: a dict OR None.
:Exceptions: none.
:Message codes: none.
:Former data:
    2.1.2.1 Returns: a dict OR False.

    2.0 Returns: aur_pkgs, list->dict, not null.

    2.0 Behavior: exception and quit when not found."""
        aur_pkgs = self.aur.request('info', pkgname)
        if aur_pkgs['results'] == 'No results found':
            return None
        else:
            return aur_pkgs['results']

    def search(self, pkgname):
        """Searches for AUR packages.

:Arguments: package name.
:Input: none.
:Output: none.
:Returns: a list.
:Exceptions: none.
:Message codes: none."""
        aur_pkgs = self.aur.request('search', pkgname)
        if aur_pkgs['results'] == 'No results found':
            return []
        else:
            return aur_pkgs['results']

    def print_package(self, pkg, use_categories = True, prefix=''):
        """Outputs info about package.

:Arguments: package name, use categories, line prefix.
:Input: none.
:Output:
    ::

    category/name version (num votes) [installed: version] [out of date]
        description

:Returns: nothing.
:Exceptions: none.
:Message codes: none.
:Former data:
    2.0 Name: showInfo."""
        H = pycman.config.init_with_config('/etc/pacman.conf')
        localdb = H.get_localdb()
        lpkg = localdb.get_pkg(pkg['Name'])

        category = ''
        installed = ''
        if lpkg != None:
            if pyalpm.vercmp(pkg['Version'], lpkg.version) != 0:
                installed = _(' [installed: {0}]').format(lpkg.version)
            else:
                installed = _(' [installed]')
        if pkg['OutOfDate'] == 1:
            installed = (installed + ' '+DS.colors['red']+_(
            '[out of date]')+DS.colors['all_off'])
        if use_categories == True:
            category = DS.categories[int(pkg['CategoryID'])]
        else:
            category = 'aur'
        if prefix == '':
            base = prefix+'{0}/{1} {2} ({4} '+_('votes')+'){5}\n'+prefix+'\
    {3}'
        else:
            base = prefix+' {0}/{1} {2} ({4} '+_('votes')+'){5}\n\
'+prefix+'     {3}'

        print(base.format(category, pkg['Name'], pkg['Version'],
                          pkg['Description'], pkg['NumVotes'], installed))

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

    def auto_build(self, pkgname, validate = True, performdepcheck = True,
                   makepkginstall = True):
        """NOT the actual build function.
This function makes validation and building AUR deps possible.
If you can, use it.

:Arguments: package name, validate installation, perform dependency checks.
:Input: none.
:Output: text.
:Returns: nothing.
:Exceptions: PBError.
:Message codes:
    ERR3301, ERR34?? (ERR3401, ERR3450, ERR3451, ERR3452), INF3450.
:Former data:
    2.0 Name: build."""
        build_result = self.build_runner(pkgname, performdepcheck,
                                         makepkginstall)
        try:
            if build_result[0] == 0:
                fancy_msg(_('The build function reported a proper build.'))
                os.chdir('../')
                if validate == True:
                    # check if installed
                    H = pycman.config.init_with_config('/etc/pacman.conf')
                    localdb = H.get_localdb()
                    pkg = localdb.get_pkg(pkgname)
                    aurversion = self.utils.info(pkgname)['Version']
                    if pkg is None:
                        fancy_error2(_('[ERR3451] validation: NOT \
installed'))
                    else:
                        if pyalpm.vercmp(aurversion, pkg.version) > 0:
                            fancy_error2(_('[ERR3452] validation: \
outdated {0}').format(pkg.version))
                        else:
                            fancy_msg2(_('[INF3450] validation: \
installed {0}').format(pkg.version))
            elif build_result[0] >= 0 and build_result[0] <= 15:
                os.chdir('../')
                raise PBError(_('[ERR3301] makepkg returned 1.'))
                # I think that only makepkg can do that.  Others would
                # raise an exception.
            elif build_result[0] == 16:
                os.chdir('../')
                fancy_warning(_('[ERR3401] Building more AUR packages is \
required.'))
                for pkgname2 in build_result[1]:
                    self.auto_build(pkgname2, validate, performdepcheck,
                                    makepkginstall)
                self.auto_build(pkgname, validate, performdepcheck,
                                makepkginstall)
        except PBError as inst:
            fancy_error(str(inst))

    def download(self, urlpath, filename, prot = 'http'):
        """Downloads an AUR tarball (http) to the current directory.

:Arguments: URL, filename for saving, protocol.
:Input: none.
:Output: none.
:Returns: bytes downloaded.
:Exceptions:
    PBError, IOError,
    urllib.error.URLError, urllib.error.HTTPError
:Message codes: ERR3101."""
        rhandle = urllib.request.urlopen(self.aururl.format(prot, urlpath))
        headers = rhandle.info()
        fhandle = open(filename, 'wb')
        fhandle.write(rhandle.read())
        fhandle.close()
        if headers['Content-Length'] != 0:
            return headers['Content-Length']
        else:
            raise PBError(_('[ERR3101] download: 0 bytes downloaded'))

    def extract(self, filename):
        """        Extracts an AUR tarball.

:Arguments: filename.
:Input: none.
:Output: none.
:Returns: file count.
:Exceptions: PBError, IOError.
:Message codes: ERR3151."""
        thandle = tarfile.open(filename, 'r:gz')
        thandle.extractall()
        names = thandle.getnames()
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
        # This code is bad.  If you want to, fix it.
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
            depends = [ s.rstrip() for s in bashdepends[0][1:-1] ]
        if bmdepends != []:
            makedepends = [ s.rstrip() for s in bmdepends[0][1:-1] ]

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
:Suggested way of handling:
    ::

    types = ['system', 'repos', 'aur']
    for pkg, pkgtype in depcheck([…]).items():
        print('{0}: found in {1}'.format(pkg, types[pkgtype])
        if pkgtype == 2: #AUR
            #build pkg here

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
            for j in [ i.pkgcache for i in H.get_syncdbs() ]:
                syncpkgs.append(j)
            syncpkgs = functools.reduce(lambda x,y:x+y,syncpkgs)
            #can someone help me fix the above line? TODO.
            for dep in depends:
                if re.search('[<=>]', dep):
                    vpat = '>=<|><=|=><|=<>|<>=|<=>|>=|=>|><|<>|=<|\
<=|>|=|<'
                    ver_base = re.split(vpat, dep)
                    dep = ver_base[0]
                #pkg = localdb.get_pkg(dep)
                #repos = dict((db.name, db) for db in pyalpm.get_syncdbs())
                if pyalpm.find_satisfier(localpkgs, dep): #pkg != None:
                    parseddeps[dep] = 0
                elif pyalpm.find_satisfier(syncpkgs, dep):
                    #pycman.action_sync.find_sync_package(dep, repos)[0]:
                    parseddeps[dep] = 1
                elif self.utils.info(dep) != None:
                    parseddeps[dep] = 2
                else:
                    parseddeps[dep] = -1
                    raise PBError(_('[ERR3201] depcheck: cannot find {0} \
anywhere').format(dep))
            return parseddeps
    def build_runner(self, pkgname, performdepcheck = True,
                     makepkginstall = True):
        """A build function, which actually links to others.  Do not use it
unless you re-implement auto_build.

:Arguments: pkgname, perform dependency checks.
:Input: none.
:Output: text.
:Returns: ::

    [makepkg's retcode or 3 if fails or 16 if needs an AUR dep,
        [AUR deps or 'makepkg'] or nothing
    ]

:Exceptions: PBError.
:Message codes: ERR3001, ERR3201, ERR3202.
:Former data:
    2.0 Behavior: all functions inside

    2.0 Name: buildSub"""
        try:
            # exists
            pkg = self.utils.info(pkgname)
            if pkg == None:
                raise PBError(_('[ERR3001] Package {0} not found.').format(
                              pkgname))
            pkgname = pkg['Name']
            fancy_msg(_('Building {0}…').format(pkgname))
            self.utils.print_package(pkg,
                                     prefix=DS.colors['blue']+'  ->'+
                                     DS.colors['all_off']+
                                     DS.colors['bold'])
            filename = pkgname+'.tar.gz'
            # Okay, this package exists, great then.  Thanks, user.

            fancy_msg(_('Downloading the tarball…'))
            downloadbytes = self.download(pkg['URLPath'], filename)
            kbytes = int(downloadbytes) / 1000
            fancy_msg2(_('{0} kB downloaded').format(kbytes))

            fancy_msg(_('Extracting…'))
            fancy_msg2(_('{0} files extracted').format(self.extract(
                                                       filename)))
            os.chdir('./'+pkgname+'/')
            if performdepcheck == True:
                fancy_msg(_('Checking dependencies…'))
                try:
                    depends = self.prepare_deps(open('./PKGBUILD',
                              'rb').read().decode('utf8', 'ignore'))
                    deps = self.depcheck(depends)
                    pkgtypes = [_('found in system'), _('found in repos'),
                                _('found in the AUR')                     ]
                    aurbuild = []
                    if deps == {}:
                        fancy_msg2(_('none found'))

                    for pkg, pkgtype in deps.items():
                        if pkgtype == -1:
                            raise PBError(_('[ERR3201] depcheck: cannot \
find {0} anywhere').format(pkg))
                        if pkgtype == 2:
                            aurbuild.append(pkg)

                        fancy_msg2('{0}: {1}'.format(pkg,
                                                     pkgtypes[pkgtype]))
                    if aurbuild != []:
                        return [16, aurbuild]
                except UnicodeDecodeError as inst:
                    fancy_error2(_('[ERR3202] depcheck: UnicodeDecodeEr\
ror.  The PKGBUILD cannot be read.  There are invalid UTF-8 characters (\
eg. in the Maintainer field.)  Error message: {0}').format(str(inst)))

            mpparams = ''

            if makepkginstall != False:
                mpparams = mpparams+'i'

            if os.geteuid() == 0:
                mpparams = mpparams+' --asroot'

            return [subprocess.call('/usr/bin/makepkg -s'+mpparams,
            shell=True), 'makepkg']
            # In version 2.0, this comment couldn't believe that
            # the main function takes only one line.  But, right now,
            # it doesn't think so.  Others look like it, too.
        except PBError as inst:
            fancy_error(str(inst))
            return [3, ['pb']]
        except urllib.error.URLError as inst:
            fancy_error(str(inst))
            return [3, ['urllib']]
        except urllib.error.HTTPError as inst:
            fancy_error(str(inst))
            return [3, ['urllib']]
        except IOError as inst:
            fancy_error(str(inst))
            return [3, ['io']]

### Upgrade     upgrade AUR packages        ###
class Upgrade:
    """Tools for performing an upgrade."""
    def __init__(self):
        """Upgrade init."""
        self.aur = AUR()
        self.build = Build()
        self.H = pycman.config.init_with_config('/etc/pacman.conf')
        self.localdb = self.H.get_localdb()

    def gather_foreign_pkgs(self):
        """Gathers a list of all foreign packages.

:Arguments: none.
:Input: none.
:Output: none.
:Returns: foreign packages.
:Exceptions: none.
:Message codes: none."""

        # Based on paconky.py.
        installed = set(p for p in self.localdb.pkgcache)

        syncdbs = self.H.get_syncdbs()
        for sdb in syncdbs:
            for pkg in list(installed):
                if sdb.get_pkg(pkg.name):
                    installed.remove(pkg)

        foreign = dict([(p.name, p) for p in installed])

        return foreign

    def list_upgradeable(self, pkglist):
        """Compares package versions and returns upgradeable ones.

:Arguments: a package list.
:Input:
    a list of packages to be compared.

    suggestion: self.gather_foreign_pkgs().keys()
:Output: none.
:Returns: upgradeable packages.
:Exceptions: none.
:Message codes: none."""

        aurlist = self.aur.multiinfo(pkglist)['results'] # It's THAT easy.
        # Oh, and by the way: it is much, MUCH faster than others.
        # It makes ONE multiinfo request rather than $installed_packages
        # info requests.
        upgradeable = []

        for i in aurlist:
            pkg = self.localdb.get_pkg(i['Name'])
            if pyalpm.vercmp(i['Version'], pkg.version) > 0:
                upgradeable.append(i['Name'])
        return upgradeable

    def auto_upgrade(self):
        """Upgrades packages.  Simillar to Build.auto_build().

:Arguments: none.
:Input: user interaction.
:Output: text.
:Returns: 0 or nothing.
:Exceptions: none.
:Message codes: none.
:Notice: things break here A LOT."""
        pblog('Ran auto_upgrade.')
        if DS.pacman:
            print(':: '+_('Gathering data about packages…'))
        else:
            fancy_msg(_('Gathering data about packages…'))

        foreign = self.gather_foreign_pkgs()
        upgradeable = self.list_upgradeable(foreign.keys())
        upglen = len(upgradeable)
        if DS.pacman:
            print(_('Targets ({0}): ').format(upglen), end='')
        else:
            fancy_msg(_('{0} upgradeable packages found:').format(upglen))

        if upglen == 0:
            if DS.pacman:
                print(_('there is nothing to do'))
            else:
                fancy_msg2(_('there is nothing to do'))

            return 0
        if DS.pacman:
            print('  '.join(upgradeable))
            query = _('Proceed with installation? [Y/n] ')
        else:
            fancy_msg2('  '.join(upgradeable))
            query = (DS.colors['green']+'==>'+DS.colors['all_off']+
                DS.colors['bold']+' '+_('Proceed with installation? \
[Y/n] ')+DS.colors['all_off'])

        yesno = input(query)
        yesno = yesno + ' ' # cheating…
        if yesno[0] == 'n' or yesno[0] == 'N':
            return 0
        for pkgname in upgradeable:
            pblog('Building {0}'.format(pkgname))
            self.build.auto_build(pkgname, DS.validate, DS.depcheck,
                                  DS.mkpginst)

pblog('Initialized.')

def main_routine():
    """Main routine.

:Arguments: none.
:Input: none.
:Output: text.
:Returns: nothing.
:Exceptions: PBError.
:Message codes: ERR5002.
"""
    pblog('Running argparse.')
    parser = argparse.ArgumentParser(description=_('A python3 AUR helper \
(sort of.)  Wrapper-friendly (pacman-like output.)'), epilog=_('You can \
use pacman syntax if you want to.'))

    parser.add_argument('-v', '--version', action='version',
                        version='PKGBUILDer v'+VERSION)
    parser.add_argument('pkgs', metavar='PACKAGE', action='store',
                        nargs='*', help=_('packages to build'))

    argopt = parser.add_argument_group('options')
    argopr = parser.add_argument_group('operations')
    argopt.add_argument('-C', '--nocolor', action='store_false',
                        default=True, dest='color', help=_('don\'t use \
                        colors in output'))
    argopt.add_argument('-D', '--nodepcheck', action='store_false',
                        default=True, dest='depcheck', help=_('don\'t \
                        check dependencies (may break makepkg)'))
    argopt.add_argument('-w', '--buildonly', action='store_false',
                        default=True, dest='mkpginst', help=_('don\'t \
                        install packages after building'))
    argopt.add_argument('-V', '--novalidation', action='store_false',
                        default=True, dest='valid', help=_('don\'t check \
                        if packages were installed after build'))

    argopt.add_argument('-S', '--sync', action='store_true', default=False,
                        dest='pac', help=_('pacman syntax compatiblity'))
    argopt.add_argument('-y', '--refresh', action='store_true',
                        default=False, dest='pacupd', help=_('pacman \
                        syntax compatiblity'))

    argopr.add_argument('-i', '--info', action='store_true', default=False,
                        dest='info', help=_('view package information'))
    argopr.add_argument('-s', '--search', action='store_true',
                        default=False, dest='search', help=_('search the \
                        AUR for matching strings'))
    argopr.add_argument('-u', '--sysupgrade', action='store_true',
                        default=False, dest='upgrade',
                        help=_('upgrade installed AUR packages'))

    args = parser.parse_args()
    DS.validate = args.valid
    DS.depcheck = args.depcheck
    DS.pacman = args.pac
    DS.mkpginst = args.mkpginst
    try:
        utils = Utils()
        build = Build()
        pblog('Arguments parsed.')

        if args.color == False:
            # That's awesome in variables AND 2.x series.
            # …and it was moved to PBDS.
            DS.colorsoff()

        if args.info == True:
            for pkgname in args.pkgs:
                pkg = utils.info(pkgname)
                if pkg == None:
                    raise PBError(_('Package {0} not found.').format(
                          pkgname))
                ### TRANSLATORS: space it properly.  `yes/no' below are
                ### for `out of date'.
                print(_("""Category       : {cat}
Name           : {nme}
Version        : {ver}
URL            : {url}
Licenses       : {lic}
Votes          : {cmv}
Out of Date    : {ood}
Maintainer     : {mnt}
Last Updated   : {upd}
First Submitted: {fsb}
Description    : {dsc}
""").format(
                cat = DS.categories[int(pkg['CategoryID'])],
                nme = pkg['Name'],
                url = pkg['URL'],
                ver = pkg['Version'],
                lic = pkg['License'],
                cmv = pkg['NumVotes'],
                ood = DS.colors['red']+_('yes')+DS.colors['all_off'] if (
                      pkg['OutOfDate'] == '1') else _('no'),
                mnt = pkg['Maintainer'],
                upd = datetime.datetime.fromtimestamp(float(pkg['Last\
Modified'])).strftime('%a %d %b %Y %H:%m:%S %p %Z'),
                fsb = datetime.datetime.fromtimestamp(float(pkg['First\
Submitted'])).strftime('%a %d %b %Y %H:%m:%S %p %Z'),
                dsc = pkg['Description']))

                exit(0)

        if args.search == True:
            searchstring = '+'.join(args.pkgs)
            if len(searchstring) < 3:
                # this would be too many entries.  The API is really
                # having this limitation, though.
                fancy_error(_('[ERR5002] search string too short, API \
limitation'))
                fancy_msg(_('Searching for exact match…'))
                search = [utils.info(searchstring)] # workaround
                if search == [None]:
                    fancy_error2(_('not found'))
                    exit(0)
                else:
                    utils.print_package(search[0], prefix=(
                                      DS.colors['blue']+'  ->'+
                                      DS.colors['all_off']+
                                      DS.colors['bold']))
                    print(DS.colors['all_off'], end='')
                    exit(0)
            else:
                search = utils.search(searchstring)
            for pkg in search:
                if args.pac != True:
                    utils.print_package(pkg, True)
                else:
                    utils.print_package(pkg, False)
            exit(0)

        if args.pac == True:
            # -S assumes being a wrapper and/or wanting to build in /tmp.
            uid = os.geteuid()
            path = '/tmp/pkgbuilder-{0}'.format(str(uid))
            if os.path.exists(path) == False:
                os.mkdir(path)
            os.chdir(path)

    except PBError as inst:
        fancy_error(str(inst))
        exit(0)

    if args.upgrade == True:
        # We finally made it!
        upgrade = Upgrade()
        upgrade.auto_upgrade()
        del(upgrade)
        exit(0)

    # If we didn't exit, we shall build the packages.
    pblog('Ran through all the addon features, building…')
    for pkgname in args.pkgs:
        pblog('Building {0}'.format(pkgname))
        build.auto_build(pkgname, DS.validate, DS.depcheck, DS.mkpginst)

    pblog('Quitting.')

# Over 900 lines!  Compare this to build.pl's 56 (including ~8 useless…)
# New features will be included when they will be added to the AUR RPC.
# RPC: <http://aur.archlinux.org/rpc.php> (search info msearch multiinfo)
# If something new will appear there, tell me through GH Issues or mail.
# They would be implemented later.
# Some other features might show up, too.
# NOTICE: If we manage to pass 1000, it is gonna be split up.
