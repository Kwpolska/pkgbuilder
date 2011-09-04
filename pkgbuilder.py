#!/usr/bin/python3
# PKGBUILDer Version 2.1.0-prerelease
# A python3 AUR helper (sort of.) Wrapper friendly (pacman-like output.)
# Copyright Kwpolska 2011. Licensed under GPLv3.
# USAGE: ./build.py pkg1 [pkg2] [pkg3] (and more)
"""PKGBUILDer.  An AUR helper (sort of.)"""
from pyparsing import OneOrMore, Word   # python-pyparsing from [community]
import pyalpm                           # pyalpm in [extra]
import pycman                           # pyalpm in [extra]
import AUR                              # python3-aur in [xyne-any] or AUR
import argparse
import sys
import os
import re
import urllib.request
import urllib.error
import tarfile
import subprocess

# This is a prerelease version.  Some features planned aren't implemented
# yet.  Planned features include AUR package upgrade (based on paconky.py)
# and unit tests.

### n/a                top-level base utils ###

# Fancy-schmancy messages stolen from makepkg.
ALL_OFF = "\x1b[1;0m"
BOLD = "\x1b[1;1m"
BLUE = BOLD+"\x1b[1;34m"
GREEN = BOLD+"\x1b[1;32m"
RED = BOLD+"\x1b[1;31m"
YELLOW = BOLD+"\x1b[1;33m"
def fancy_msg(text):
    """
    makepkg's msg().  Use for main messages.
    """
    sys.stderr.write(GREEN+'==>'+ALL_OFF+BOLD+' '+text+ALL_OFF+"\n")

def fancy_msg2(text):
    """
    makepkg's msg2().  Use for sub-messages.
    """
    sys.stderr.write(BLUE+'  ->'+ALL_OFF+BOLD+' '+text+ALL_OFF+"\n")

def fancy_warning(text):
    """
    makepkg's warning().  Use when you have problems.
    """
    sys.stderr.write(YELLOW+'==> WARNING:'+ALL_OFF+BOLD+' '+text+ALL_OFF+
                     "\n")
def fancy_error(text):
    """
    makepkg's error().  Use for errors.  Exitting is suggested.
    """
    sys.stderr.write(RED+'==> ERROR:'+ALL_OFF+BOLD+' '+text+ALL_OFF+"\n")
# That's it.
categories = ['ERR0R', 'ERR1R', 'daemons', 'devel', 'editors', 'emulators',
              'games', 'gnome', 'i18n', 'kde', 'kernels', 'lib', 'modules',
              'multimedia', 'network', 'office', 'science', 'system',
              'x11', 'xfce']
# If you can see ERR0R or ERR1R in the output, something bad has happened.

# Do you want to see `deleted X rows from Y'?  No?  That's why I set this up.
def pblog(msg, tofile = False, tostderr = False):
    """
    A log function.  Workaround.
    """
    if tofile == True:
        open('pkgbuilder.log', 'a').write(msg)

    if tostderr == True:
        sys.stderr.write(msg)

AUR.log = pblog

### PBError         errors raised here      ###
class PBError(Exception):
    """Exceptions raised by the PKGBUILDer."""

    def __init__(self, msg, error=None):
        """Initialization is mandatory."""
        self.msg = msg
        self.error = error

#### AUR             AUR RPC calls           ###
#class AUR:
#    """AUR RPC calls.  Currently doesn't work."""
# TODO: this.  I plan a re-implementation of python3-aur basics.
# Benefits: no crappy stuff of py3k-aur, no need to get it first
# planned methods: request -OR- info, search, msearch, multiinfo
# --Kwpolska 9/3/11
### Utils           common global utilities ###
class Utils:
    """Common global utilities.  Provides useful data."""
    def info(self, pkgname):
        """
        Returns info about a package.

        Returns: aur_pkgs[0], dict, not null OR False.

        Former data:
        2.0 Returns: aur_pkgs, list, not null.
        2.0 Behavior: exception and quit when not found.
        """
        aur = AUR.AUR(threads=10)
        aur_pkgs = aur.info(pkgname)
        if aur_pkgs == []:
            return False
        else:
            return aur_pkgs[0]

    def search(self, pkgname):
        """
        Searches for AUR packages.

        Returns: aur_pkgs, list, null.
        """
        aur = AUR.AUR(threads=10)
        aur_pkgs = aur.search(pkgname)
        return aur_pkgs

    def print_package(self, package, useCategories = True):
        """
        Outputs info about package.

        Format: category/name version (num votes) [installed] [out of date]
        Out of date is displayed only when needed and in red.

        Former data:
        2.0 Name: showInfo
        """
        pycman.config.init_with_config('/etc/pacman.conf')
        db = pyalpm.get_localdb()
        pkg = db.get_pkg(package['Name'])

        category = ''
        installed = ''
        if pkg != None:
            installed = ' [installed]'
        if package['OutOfDate'] == 1:
            installed = installed + ' '+RED+'[out of date]'+ALL_OFF
        if useCategories == True:
            category = categories[package['CategoryID']]
        else:
            category = 'aur'

        print("{0}/{1} {2} ({4} votes){5}\n    {3}".format(category,
              package['Name'], package['Version'], package['Description'],
              package['NumVotes'], installed))

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
            if build_result == 0:
                fancy_msg("The build function reported a proper build.")
                os.chdir('../')
                if validate == True:
                    # check if installed
                    pycman.config.init_with_config('/etc/pacman.conf')
                    db = pyalpm.get_localdb()
                    pkg = db.get_pkg(package)
                    if pkg is None:
                        fancy_error("validation: NOT installed")
                        pyalpm.release()
                    else:
                        if self.utils.info(package)['Version'] != pkg.version:
                            fancy_error("validation: outdated "+pkg.version)
                        else:
                            fancy_msg2("validation: installed "+pkg.version)
                        pyalpm.release()
            elif build_result == 1:
                os.chdir('../')
                raise Exception("The build function returned 1 (error).")
                # I think that only makepkg can do that.  Others would
                # raise an exception.
            else:
                os.chdir('../')
                fancy_warning("Building more AUR packages is required.")
                for package2 in build_result:
                    self.auto_build(package2, True)
                self.auto_build(package, True)
        except Exception as inst:
            fancy_error(str(inst))

    def download(self, urlpath, filename, prot = 'http'):
        """
        Downloads an AUR tarball (http) to the current directory.

        Returns: bytes downloaded.
        Possible exceptions: PBError, IOError,
            urllib.error.URLError, urllib.error.HTTPError
        """
        rhandle = urllib.request.urlopen(prot+'://aur.archlinux.org'+urlpath)
        headers = rhandle.info()
        fhandle = open(filename, 'wb')
        fhandle.write(rhandle.read())
        fhandle.close()
        if headers['Content-Length'] != 0:
            return headers['Content-Length']
        else:
            raise PBError('download: 0 bytes downloaded')

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
            raise PBError('extract: no files extracted')

    def prepare_deps(self, pkgbuild):
        """
        Gets (make)depends from a PKGBUILD and returns them.

        Returns: a list, entries from PKGBUILD's depends
        and makedepends or [].
        """
        # This code is bad.  If you want to, fix it.
        fixedp = """0123456789abcdefghijklmnopqrstuvwxyz\
ABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&*+,-./:;<=>?@[]^_`{|}~"'"""
        pattern1 = "depends=(" + OneOrMore(Word(fixedp)) + ")"
        pattern2 = "makedepends=(" + OneOrMore(Word(fixedp)) + ")"

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
            depends = [ s.rstrip()[1:-1] for s in bashdepends[0][1:-1] ]
        if bmdepends != []:
            makedepends = [ s.rstrip()[1:-1] for s in bmdepends[0][1:-1] ]
        return depends + makedepends

    def depcheck(self, bothdepends):
        """
        Performs a dependency check.

        Returns: a dict:
            key  :  package name
            value:  0, 1 or 2 (in system, repos, AUR)
        Possible exceptions: PBError
        Suggested way of handling:
        types = ['system', 'repos', 'aur']
        for pkg, pkgtype in depcheck([...]).items():
            print("{0}: found in {1}".format(pkg, types[pkgtype])
            if pkgtype == 2: #AUR
                #build pkg here
        """
        if bothdepends == []:
            # THANK YOU, MAINTAINER, FOR HAVING NO DEPS AND DESTROYING ME!
            return {}
        else:
            parseddeps = {}
            pycman.config.init_with_config('/etc/pacman.conf')
            db = pyalpm.get_localdb()
            for dep in bothdepends:
                if re.search('[<=>]', dep):
                    vpat = '>=<|><=|=><|=<>|<>=|<=>|>=|=>|><|<>|=<|\
<=|>|=|<'
                    ver_base = re.split(vpat, dep)
                    dep = ver_base[0]
                    #ver = ver_base[1]
                pkg = db.get_pkg(dep)
                repos = dict((db.name, db) for db in pyalpm.get_syncdbs())
                if pkg != None:
                    parseddeps[dep] = 0
                elif pycman.action_sync.find_sync_package(dep, repos):
                    parseddeps[dep] = 1
                elif self.utils.info(dep):
                    parseddeps[dep] = 2
                else:
                    raise PBError("depcheck: cannot find {0} \
anywhere".format(dep))
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
            pkgname = pkginfo['Name']
            fancy_msg('Compiling package {0}...'.format(pkgname))
            self.utils.print_package(pkginfo)
            filename = pkgname+'.tar.gz'
            # Okay, this package exists, great then.  Thanks, user.

            fancy_msg('Downloading the tarball...')
            downloadbytes = self.download(pkginfo['URLPath'], filename)
            kbytes = int(downloadbytes) / 1000 #`K' means thousand.
            fancy_msg2('{0}K bytes downloaded'.format(kbytes))

            fancy_msg('Extracting...')
            extractfiles = self.extract(filename)
            fancy_msg2('{0} files extracted'.format(extractfiles))
            os.chdir('./'+pkgname+'/')

            fancy_msg('Checking dependencies...')
            bothdepends = self.prepare_deps(open('./PKGBUILD', 'r').read())
            deps = self.depcheck(bothdepends)
            pkgtypes = ['system', 'repos', 'the AUR']
            aurbuild = []
            if deps == {}:
                fancy_msg2('none found')

            for pkg, pkgtype in deps.items():
                fancy_msg2("{0}: found in {1}".format(pkg, pkgtypes[pkgtype]))
                if pkgtype == 2:
                    aurbuild.append(pkg)
            if aurbuild != []:
                return aurbuild

            asroot = ''
            if os.geteuid() == 0:
                asroot = ' --asroot'
            return subprocess.call('/usr/bin/makepkg -si'+asroot,
            shell=True)
            # In version 2.0, this comment couldn't believe that
            # the main function takes only one line.  But, right now,
            # it doesn't think so.  Others look like it, too.
        except PBError as inst:
            fancy_error(str(inst))
        except urllib.error.URLError as inst:
            fancy_error(str(inst))
        except urllib.error.HTTPError as inst:
            fancy_error(str(inst))
        except IOError as inst:
            fancy_error(str(inst))
        except KeyboardInterrupt as inst:
            fancy_error('KeyboardInterrupt (^C) caught.')
            exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A python3 AUR helper \
(sort of.)  Wrapper-friendly (pacman-like output.)", epilog="You can use \
pacman syntax if you want to.")
    parser.add_argument('-C', '--nocolor', action='store_false',
                        default=True, dest='color', help="don't use colors")
    parser.add_argument('-V', '--novalidation', action='store_false',
                        default=True, dest='valid', help="don't check if \
                        packages were installed after build")

    parser.add_argument('-i', '--info', action='store_true', default=False,
                        dest='info', help="show package info")
    parser.add_argument('-s', '--search', action='store_true',
                        default=False, dest='search', help="search for a \
                        package")
    parser.add_argument('-u', '--sysupgrade', action='store_true',
                        default=False, dest='upgrade',
                        help="[NOT IMPLEMENTED] upgrade installed AUR \
packages")

    parser.add_argument('-S', '--sync', action='store_true', default=False,
                        dest='pac', help="pacman syntax compatiblity")
    parser.add_argument('-y', '--refresh', action='store_true',
                        default=False, dest='pacupd', help="pacman \
syntax compatiblity")
    parser.add_argument('pkgs', metavar="PACKAGE", action='store',
                        nargs='*', help="packages to build")
    args = parser.parse_args()

    u = Utils()
    b = Build()

    if args.upgrade == True:
        fancy_error("Sorry, but this feature is not implemented yet...")

    if args.color == False:
        #That's awesome in variables AND this version.
        ALL_OFF = ''
        BOLD = ''
        BLUE = ''
        GREEN = ''
        RED = ''
        YELLOW = ''

    if args.info == True:
        for package in args.pkgs:
            pkg = u.info(package)
            category = pkg['CategoryID']
            print("""Name           : {0}
Version        : {1}
URL            : {2}
Licenses       : {3}
Category       : {4}
Votes          : {5}
Out of Date    : {6}
Description    : {7}""".format(pkg['Name'], pkg['Version'],
                               pkg['URL'], pkg['License'],
                               categories[category], pkg['NumVotes'],
                               pkg['OutOfDate'],

                               pkg['Description']))
            #pkg['Maintainer'], pkg['FirstSubmitted'].strftime(
            #'%Y-%m-%dT%H:%m:%SZ'), pkg['LastModified'].strftime(
            #'%Y-%m-%dT%H:%m:%SZ'),
            #Xyne, hardcoding stuff is evil.        (rpc upd 8/20/11)

            #I tried to be simillar to pacman, so you can make a wrapper.
        exit(0)

    if args.search == True:
        pkgsearch = u.search(' '.join(args.pkgs)) #pacman-like behavior.
        for package in pkgsearch:
            if args.pac != True:
                u.print_package(package, True)
            else:
                u.print_package(package, False)
        exit(0)

    if args.pac == True:
        uid = os.geteuid()
        path = '/tmp/pkgbuilder-{0}'.format(str(uid))
        if os.path.exists(path) == False:
            os.mkdir(path)
        os.chdir(path)

    #If we didn't exit, we shall build the packages.
    for package in args.pkgs:
        b.auto_build(package, args.valid)
        #This one is amazing, too.  See lines #225-#227.
# Over 450 lines!  Compare this to build.pl's 56 (including ~8 useless...)
# New features will be included when they will be added to the AUR RPC
# and python3-aur.       (note to Xyne: hardcoding stuff is evil.)
# RPC: <http://aur.archlinux.org/rpc.php> (search info msearch multiinfo)
# If something new will appear there, tell me through GH Issues or mail.
# They would be implemented later.
# Some other features might show up, too.  (hint hint: line #395)
