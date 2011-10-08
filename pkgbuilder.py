#!/usr/bin/python3
# PKGBUILDer Version 2.1.1.5
# A Python AUR helper/library.
# Copyright Kwpolska 2011. Licensed under GPLv3.
# USAGE: ./build.py pkg1 [pkg2] [pkg3] (and more)
"""PKGBUILDer.  An AUR helper (sort of.)"""
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

VERSION = '2.1.1.5'
T = gettext.translation('pkgbuilder', '/usr/share/locale', fallback='en')
_ = T.gettext

### PBDS            PB global data storage  ###
class PBDS:
    """PKGBUILDer Data Storage"""
    def __init__(self):
        """PBDS init"""
        # Fancy-schmancy messages stolen from makepkg.

        self.all_off = '\x1b[1;0m'
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
        self.categories = ['E', 'E', 'daemons', 'devel', 'editors',
                           'emulators', 'games', 'gnome', 'i18n', 'kde',
                           'lib', 'modules', 'multimedia', 'network',
                           'office', 'science', 'system', 'x11',
                           'xfce', 'kernels']

    def colorson(self):
        """colors on"""
        self.colors = {
                        'all_off':    '\x1b[1;0m',
                        'bold':       '\x1b[1;1m',
                        'blue':       '\x1b[1;1m\x1b[1;34m',
                        'green':      '\x1b[1;1m\x1b[1;32m',
                        'red':        '\x1b[1;1m\x1b[1;31m',
                        'yellow':     '\x1b[1;1m\x1b[1;33m'
                      }


    def colorsoff(self):
        """colors off"""
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
    """A log function.  Executed when requested and by fancy_*."""
    if tofile == True:
        open('pkgbuilder.log', 'a').write(msg)

    if tostderr == True:
        sys.stderr.write(msg)

DS = PBDS()

def fancy_msg(text):
    """makepkg's msg().  Use for main messages."""
    sys.stderr.write(DS.colors['green']+'==>'+DS.colors['all_off']+
                     DS.colors['bold']+' '+text+DS.colors['all_off']+'\n')
    pblog('(auto fancy_msg    ) '+text)

def fancy_msg2(text):
    """makepkg's msg2().  Use for sub-messages."""
    sys.stderr.write(DS.colors['blue']+'  ->'+DS.colors['all_off']+
                     DS.colors['bold']+' '+text+DS.colors['all_off']+'\n')
    pblog('(auto fancy_msg2   ) '+text)

def fancy_warning(text):
    """makepkg's warning().  Use when you have problems."""
    sys.stderr.write(DS.colors['yellow']+'==> '+_('WARNING:')+
                     DS.colors['all_off']+DS.colors['bold']+' '+text+
                     DS.colors['all_off']+'\n')
    pblog('(auto fancy_warning) '+text)

def fancy_error(text):
    """makepkg's error().  Use for errors.  Exitting is suggested."""
    sys.stderr.write(DS.colors['red']+'==> '+_('ERROR:')+
                     DS.colors['all_off']+DS.colors['bold']+
                     ' '+text+DS.colors['all_off']+'\n')
    pblog('(auto fancy_error  ) '+text)

def fancy_error2(text):
    """like fancy_error, but looks like a sub-message (fancy_msg2)."""
    sys.stderr.write(DS.colors['red']+'  ->'+DS.colors['all_off']+
                     DS.colors['bold']+' '+text+DS.colors['all_off']+'\n')
    pblog('(auto fancy_error2 ) '+text)

### PBError         errors raised here      ###
class PBError(Exception):
    """Exceptions raised by the PKGBUILDer."""

    def __init__(self, msg):
        """Initialization is mandatory."""
        self.msg = msg

    def __str__(self):
        """You want to see error messages, don't you?"""
        return self.msg

### AUR             AUR RPC calls           ###
class AUR:
    """A class for calling the AUR API.  Basics only."""

    def __init__(self):
        """Stores the RPC URLs."""
        self.rpc = '{0}://aur.archlinux.org/rpc.php?type={1}&arg={2}'
        self.mrpc = '{0}://aur.archlinux.org/rpc.php?type=multiinfo{1}'

    def jsonreq(self, rtype, arg, prot = 'http'):
        """Makes a request, but returns plain JSON data."""
        rhandle = urllib.request.urlopen(self.rpc.format(prot, rtype, arg))
        return rhandle.read().decode()

    def jsonmultiinfo(self, pyargs, prot = 'http'):
        """Makes a multiinfo request, but returns plain JSON data."""
        urlargs = '&arg[]='+'&arg[]='.join(pyargs)
        rhandle = urllib.request.urlopen(self.mrpc.format(prot, urlargs))
        return rhandle.read().decode()

    def request(self, rtype, arg, prot = 'http'):
        """Makes a request.
Syntax: request(TYPE, ARGUMENT[, PROTOCOL])
where   TYPE is the request type from aur.archlinux.org/rpc.php,
        ARGUMENT is the request argument, e.g. search query,
        PROTOCOL is the protocol used, http or https."""
        return json.loads(self.jsonreq(rtype, arg, prot))

    def multiinfo(self, pyargs, prot = 'http'):
        """Makes a multiinfo request.  Simillar to AUR.request()."""
        return json.loads(self.jsonmultiinfo(pyargs, prot))

### Utils           common global utilities ###
class Utils:
    """Common global utilities.  Provides useful data."""

    def __init__(self):
        """The AUR class is mandatory."""
        self.aur = AUR()
    def info(self, pkgname):
        """
        Returns info about a package.

        Returns: aur_pkgs['results'], dict, not null OR False.

        Former data:
        2.0 Returns: aur_pkgs, list->dict, not null.
        2.0 Behavior: exception and quit when not found.
        """
        aur_pkgs = self.aur.request('info', pkgname)
        if aur_pkgs['results'] == 'No results found':
            return False
        else:
            return aur_pkgs['results']

    def search(self, pkgname):
        """
        Searches for AUR packages.

        Returns: aur_pkgs, list, null.
        """
        aur_pkgs = self.aur.request('search', pkgname)
        if aur_pkgs['results'] == 'No results found':
            return []
        else:
            return aur_pkgs['results']

    def print_package(self, pkg, use_categories = True, prefix=''):
        """
        Outputs info about package.

        Format: category/name version (num votes) [installed] [out of date]
        Out of date is displayed only when needed and in red.

        Former data:
        2.0 Name: showInfo
        """
        pycman.config.init_with_config('/etc/pacman.conf')
        localdb = pyalpm.get_localdb()
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
            base = prefix+'{0}/{1} {2} ({4} '+_('votes')+'{5}\n'+prefix+'\
    {3}'
        else:
            base = prefix+' {0}/{1} {2} ({4} '+_('votes')+'{5}\n'+prefix+'\
     {3}'

        print(base.format(category, pkg['Name'], pkg['Version'],
                          pkg['Description'], pkg['NumVotes'], installed))

        pyalpm.release()

### Build       build functions and helpers ###
class Build:
    """
    Functions for building packages.  Main functions are auto_build
    and build_runner.
    """

    def __init__(self):
        """
        Class init.
        """
        self.utils = Utils()
        self.aururl = '{0}://aur.archlinux.org{1}'

    def auto_build(self, package, validate):
        """
        NOT the actual build function.
        This function makes validation and building AUR deps possible.
        If you can, use it.

        Former data:
        2.0 Name: build
        """
        build_result = self.build_runner(package)
        try:
            if build_result[0] == 0:
                fancy_msg(_('The build function reported a proper build.'))
                os.chdir('../')
                if validate == True:
                    # check if installed
                    pycman.config.init_with_config('/etc/pacman.conf')
                    localdb = pyalpm.get_localdb()
                    pkg = localdb.get_pkg(package)
                    aurversion = self.utils.info(package)['Version']
                    if pkg is None:
                        fancy_error2(_('[ERR3451] validation: NOT \
installed'))
                        pyalpm.release()
                    else:
                        if pyalpm.vercmp(aurversion, pkg.version) > 0:
                            fancy_error2(_('[ERR3452] validation: \
outdated {0}').format(pkg.version))
                        else:
                            fancy_msg2(_('[INF3450] validation: \
installed {0}').format(pkg.version))
                        pyalpm.release()
            elif build_result[0] == 1:
                os.chdir('../')
                raise PBError(_('[ERR3301] makepkg returned 1.'))
                # I think that only makepkg can do that.  Others would
                # raise an exception.
            elif build_result[0] == 2:
                os.chdir('../')
                fancy_warning(_('[ERR3401] Building more AUR packages is \
required.'))
                for package2 in build_result:
                    self.auto_build(package2, True)
                self.auto_build(package, True)
        except PBError as inst:
            fancy_error(str(inst))

    def download(self, urlpath, filename, prot = 'http'):
        """
        Downloads an AUR tarball (http) to the current directory.

        Returns: bytes downloaded.
        Possible exceptions: PBError, IOError,
            urllib.error.URLError, urllib.error.HTTPError
        """
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
        """
        Extracts an AUR tarball.

        Returns: file count.
        Possible exceptions: PBError, IOError
        """
        thandle = tarfile.open(filename, 'r:gz')
        thandle.extractall()
        names = thandle.getnames()
        if names != []:
            return len(names)
        else:
            raise PBError(_('[ERR3151] extract: no files extracted'))

    def prepare_deps(self, pkgbuild):
        """
        Gets (make)depends from a PKGBUILD and returns them.

        Returns: a list, entries from PKGBUILD's depends
        and makedepends or [].
        """
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

    def depcheck(self, bothdepends):
        """
        Performs a dependency check.

        Returns: a dict:
            key  :  package name
            value:  -1, 0, 1 or 2 (nowhere, in system, repos, AUR)
        Possible exceptions: PBError
        Suggested way of handling:
        types = ['system', 'repos', 'aur']
        for pkg, pkgtype in depcheck([...]).items():
            print('{0}: found in {1}'.format(pkg, types[pkgtype])
            if pkgtype == 2: #AUR
                #build pkg here

        Former data:
        2.0 Returns: no -1
        """
        if bothdepends == []:
            # THANK YOU, MAINTAINER, FOR HAVING NO DEPS AND DESTROYING ME!
            return {}
        else:
            parseddeps = {}
            pycman.config.init_with_config('/etc/pacman.conf')
            localpkgs = pyalpm.get_localdb().pkgcache
            syncpkgs = []
            for j in [ i.pkgcache for i in pyalpm.get_syncdbs() ]:
                syncpkgs.append(j)
            for dep in bothdepends:
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
                elif self.utils.info(dep):
                    parseddeps[dep] = 2
                else:
                    parseddeps[dep] = -1
                    raise PBError(_('[ERR3201] depcheck: cannot find {0} \
anywhere').format(dep))
            pyalpm.release()
            return parseddeps

    def build_runner(self, package):
        """
        A build function, which actually links to others.  Do not use it
        unless you re-implement auto_build.
        Former data:
        2.0 Behavior: all functions inside
        2.0 Name: buildSub
        """
        try:
            # exists
            pkginfo = self.utils.info(package)
            if pkginfo == False:
                raise PBError(_('[ERR3001] Package {0} not found.').format(
                              package))
            pkgname = pkginfo['Name']
            fancy_msg(_('Building {0}...').format(pkgname))
            self.utils.print_package(pkginfo,
                                     prefix=DS.colors['blue']+'  ->'+
                                     DS.colors['all_off']+
                                     DS.colors['bold'])
            filename = pkgname+'.tar.gz'
            # Okay, this package exists, great then.  Thanks, user.

            fancy_msg(_('Downloading the tarball...'))
            downloadbytes = self.download(pkginfo['URLPath'], filename)
            kbytes = int(downloadbytes) / 1000
            fancy_msg2(_('{0} kB downloaded').format(kbytes))

            fancy_msg(_('Extracting...'))
            fancy_msg2(_('{0} files extracted').format(self.extract(
                                                       filename)))
            os.chdir('./'+pkgname+'/')

            fancy_msg(_('Checking dependencies...'))
            try:
                bothdepends = self.prepare_deps(open('./PKGBUILD',
                              'rb').read().decode('utf8', 'ignore'))
                deps = self.depcheck(bothdepends)
                pkgtypes = [_('found in system'), _('found in repos'),
                            _('found in the AUR')                     ]
                aurbuild = []
                if deps == {}:
                    fancy_msg2(_('none found'))

                for pkg, pkgtype in deps.items():
                    if pkgtype == -1:
                        raise PBError(_('[ERR3201] depcheck: cannot find \
{0} anywhere').format(dep))
                    if pkgtype == 2:
                        aurbuild.append(pkg)

                    fancy_msg2('{0}: {1}'.format(pkg,
                               pkgtypes[pkgtype]))
                if aurbuild != []:
                    return [2, aurbuild]
            except UnicodeDecodeError as inst:
                fancy_error2(_('[ERR3202] depcheck: UnicodeDecodeError.\
  The PKGBUILD cannot be read.  There are invalid UTF-8 characters (eg. \
in the Maintainer field.)  Error message: {0}').format(str(inst)))

            asroot = ''
            if os.geteuid() == 0:
                asroot = ' --asroot'
            return [subprocess.call('/usr/bin/makepkg -si'+asroot,
            shell=True), 'makepkg']
            # In version 2.0, this comment couldn't believe that
            # the main function takes only one line.  But, right now,
            # it doesn't think so.  Others look like it, too.
        except PBError as inst:
            fancy_error(str(inst))
            return [3]
        except urllib.error.URLError as inst:
            fancy_error(str(inst))
            return [3]
        except urllib.error.HTTPError as inst:
            fancy_error(str(inst))
            return [3]
        except IOError as inst:
            fancy_error(str(inst))
            return [3]

### Upgrade     upgrade AUR packages        ###
class Upgrade:
    """Tools for performing an upgrade."""
    def __init__(self):
        """Class init."""
        self.aur = AUR()
        self.build = Build()
        pycman.config.init_with_config('/etc/pacman.conf')
        self.localdb = pyalpm.get_localdb()

    def __del__(self):
        try:
            pyalpm.release()
        except pyalpm.error:
            pass

    def gather_foreign_pkgs(self):
        """Gathers a list of all foreign packages."""

        # Based on paconky.py.
        installed = set(p for p in self.localdb.pkgcache)

        syncdbs = pyalpm.get_syncdbs()
        for sdb in syncdbs:
            for pkg in list(installed):
                if sdb.get_pkg(pkg.name):
                    installed.remove(pkg)

        foreign = dict([(p.name, p) for p in installed])

        return foreign

    def list_upgradeable(self, pkglist):
        """
        Compares package versions.
        Input: a list of packages to be compared.
               suggestion: self.gather_foreign_pkgs().keys()
        Returns: a list of packages with newer versions in the AUR.
        """

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
        """
        Upgrades packages.  Simillar to Build.auto_build().
        Notice: things break here A LOT.  Perform twice if you can.
        """
        pblog('Ran auto_upgrade.')
        fancy_msg(_('Gathering data about packages...'))

        foreign = self.gather_foreign_pkgs()
        upgradeable = self.list_upgradeable(foreign.keys())
        upglen = len(upgradeable)

        fancy_msg(_('{0} upgradeable packages found:').format(upglen))
        if upglen == 0:
            fancy_msg2(_('there is nothing to do'))
            return 0
        fancy_msg2('  '.join(upgradeable))
        query = (DS.colors['green']+'==>'+DS.colors['all_off']+
                DS.colors['bold']+' '+_('Proceed with installation? \
[Y/n] ')+DS.colors['all_off'])
        yesno = input(query)
        yesno = yesno + ' ' # cheating...
        if yesno[0] == 'n' or yesno[0] == 'N':
            return 0
        else:
            pyalpm.release()
        for package in upgradeable:
            pblog('Building {0}'.format(package))
            self.build.auto_build(package, DS.validate)

pblog('Initialized.')

def main_routine():
    """Main routine.  Usage: main_routine(sys.argv)"""
    pblog('Running argparse.')
    parser = argparse.ArgumentParser(description=_('A python3 AUR helper \
(sort of.)  Wrapper-friendly (pacman-like output.)'), epilog=_('You can \
use pacman syntax if you want to.'))

    parser.add_argument('-v', '--version', action='version',
                        version='PKGBUILDer '+VERSION)
    parser.add_argument('pkgs', metavar='PACKAGE', action='store',
                        nargs='*', help=_('packages to build'))

    argopt = parser.add_argument_group('options')
    argopr = parser.add_argument_group('operations')
    argopt.add_argument('-C', '--nocolor', action='store_false',
                        default=True, dest='color', help=_('don\'t use \
                        colors in output'))
    argopt.add_argument('-S', '--sync', action='store_true', default=False,
                        dest='pac', help=_('pacman syntax compatiblity'))
    argopt.add_argument('-V', '--novalidation', action='store_false',
                        default=True, dest='valid', help=_('don\'t check \
                        if packages were installed after build'))
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
    DS.pacman = args.pac
    try:
        utils = Utils()
        build = Build()
        pblog('Arguments parsed.')

        if args.color == False:
            # That's awesome in variables AND 2.x series.
            # ...and it was moved to PBDS.
            DS.colorsoff()

        if args.info == True:
            for ipackage in args.pkgs:
                ipkg = utils.info(ipackage)
                if ipkg == False:
                    raise PBError(_('Package {0} not found.').format(
                          ipackage))
                ### TRANSLATORS: space it properly.  `yes/no' below are
                ### for `out of date'.
                print(_("""Category       : {0}
Name           : {1}
URL            : {3}
Licenses       : {4}
Votes          : {5}
Out of Date    : {6}
Maintainer     : {7}
Last Updated   : {8}
First Submitted: {9}
Description    : {10}
""").format(DS.categories[int(ipkg['CategoryID'])], ipkg['Name'],
            ipkg['Version'], ipkg['URL'], ipkg['License'], ipkg['NumVotes'],
            DS.colors['red']+_('yes')+DS.colors['all_off'] if (
            ipkg['OutOfDate'] == '1') else _('no'), ipkg['Maintainer'],
            datetime.datetime.fromtimestamp(float(
            ipkg['LastModified'])).strftime('%a %d %b %Y %H:%m:%S %p %Z'),
            datetime.datetime.fromtimestamp(float(
            ipkg['FirstSubmitted'])).strftime('%a %d %b %Y %H:%m:%S %p \
%Z'), ipkg['Description']))
                exit(0)

        if args.search == True:
            searchstring = '+'.join(args.pkgs)
            if len(searchstring) < 3:
                # this would be too many entries.  The API is really
                # having this limitation, though.
                fancy_error(_('[ERR5002] search string too short, API \
limitation'))
                fancy_msg(_('Searching for exact match...'))
                pkgsearch = [utils.info(searchstring)] # workaround
                if pkgsearch == [False]:
                    fancy_msg2(_('not found'))
                    exit(0)
                else:
                    fancy_msg2(_('found'))
            else:
                pkgsearch = utils.search(searchstring) # pacman behavior
            for spackage in pkgsearch:
                if args.pac != True:
                    utils.print_package(spackage, True)
                else:
                    utils.print_package(spackage, False)
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

    if args.upgrade == True:
        # We finally made it!
        upgrade = Upgrade()
        upgrade.auto_upgrade()
        del(upgrade)
        exit(0)

    # If we didn't exit, we shall build the packages.
    pblog('Ran through all the addon features, building...')
    for bpackage in args.pkgs:
        pblog('Building {0}'.format(bpackage))
        build.auto_build(bpackage, args.valid)

    pblog('Quitting.')

# Over 650 lines!  Compare this to build.pl's 56 (including ~8 useless...)
# New features will be included when they will be added to the AUR RPC.
# RPC: <http://aur.archlinux.org/rpc.php> (search info msearch multiinfo)
# If something new will appear there, tell me through GH Issues or mail.
# They would be implemented later.
# Some other features might show up, too.
