#!/usr/bin/python3
# PKGBUILDer Version 2
# A python3 AUR helper (sort of.) Wrapper friendly (pacman-like output.)
# Part of KRU
# Copyright Kwpolska 2011. Licensed under GPLv3.
# USAGE: ./build.py pkg1 [pkg2] [pkg3] (and more)

import pyalpm               # pyalpm in [extra]
import pycman               # pyalpm in [extra]
import AUR                  # python3-aur in [xyne-any] or AUR
import argparse
import sys
import os
import re
import shlex
import urllib.request
import urllib.error
import tarfile
import subprocess

#Fancy-schmancy messages stolen from makepkg.
ALL_OFF="\x1b[1;0m"
BOLD="\x1b[1;1m"
BLUE=BOLD+"\x1b[1;34m"
GREEN=BOLD+"\x1b[1;32m"
RED=BOLD+"\x1b[1;31m"
YELLOW=BOLD+"\x1b[1;33m"
def fancyMsg(text):
    sys.stderr.write(GREEN+'==>'+ALL_OFF+BOLD+' '+text+ALL_OFF+"\n")

def fancyMsg2(text):
    sys.stderr.write(BLUE+'  ->'+ALL_OFF+BOLD+' '+text+ALL_OFF+"\n")

def fancyWarning(text):
    sys.stderr.write(YELLOW+'==> WARNING:'+ALL_OFF+BOLD+' '+text+ALL_OFF+
                     "\n")
def fancyError(text):
    sys.stderr.write(RED+'==> ERROR:'+ALL_OFF+BOLD+' '+text+ALL_OFF+"\n")
#That's it.
categories = ['ERR0R', 'ERR1R', 'daemons', 'devel', 'editors', 'emulators',
              'games', 'gnome', 'i18n', 'kde', 'kernels', 'lib', 'modules',
              'multimedia', 'network', 'office', 'science', 'system',
              'x11', 'xfce']
#If you can see ERR0R or ERR1R in the output, something bad has happened.

#Do you want to see `deleted X rows from Y'?  No?  That's why I set this up.
def pblog(msg, tofile = False, tostderr = False):
    """
    A log function.  Workaround.
    """
    if tofile == True:
        open('pkgbuilder.log', 'a').write(msg)

    if tostderr == True:
        sys.stderr.write(msg)

AUR.log = pblog

def info(pkgname):
    """
    Returns info about a package.
    """
    try:
        aur = AUR.AUR(threads=10)
        aur_pkgs = aur.info(pkgname)
        if aur_pkgs == []:
            raise Exception("Cannot find the package \
`{0}'.".format(pkgname))
        else:
            return aur_pkgs
    except Exception as inst:
        fancyError(str(inst))
        exit(1)

def search(pkgname):
    """
    Searches for AUR packages.
    """
    aur = AUR.AUR(threads=10)
    aur_pkgs = aur.search(pkgname)
    return aur_pkgs

def showInfo(package, useCategories = True):
    """
    Outputs info about package.

    Format: category/name version (num votes, out of date) [installed]
    Out of date is displayed only when needed and in red.
    """
    pycman.config.init_with_config('/etc/pacman.conf')
    db = pyalpm.get_localdb()
    pkg = db.get_pkg(package['Name'])

    category = ''
    outofdate = ''
    installed = ''
    if package['OutOfDate'] == 1:
        outofdate=', '+RED+'out of date'+ALL_OFF
    if pkg != None:
        installed = ' [installed]'
    if useCategories == True:
        category = categories[package['CategoryID']]
    else:
        category = 'aur'

    print("{0}/{1} {2} ({4} votes{5}){6}\n    {3}".format(category,
          package['Name'], package['Version'], package['Description'],
          package['NumVotes'], outofdate, installed))

    pyalpm.release()
def build(package, validate):
    """
    NOT the actual build function.
    This function makes validation and building AUR deps possible.
    If you can, use it.
    """
    buildResult = buildSub(package)
    try:
        if buildResult == 0:
            fancyMsg("The build function reported a proper build.")
            os.chdir('../')
            if validate == True:
                #check if installed
                pycman.config.init_with_config('/etc/pacman.conf')
                db = pyalpm.get_localdb()
                pkg = db.get_pkg(package)
                if pkg is None:
                    fancyError("validation: NOT installed")
                    pyalpm.release()
                else:
                    if info(package)[0]['Version'] != pkg.version:
                        fancyError("validation: out-of-date, "+pkg.version)
                    else:
                        fancyMsg2("validation: installed "+pkg.version)
                    pyalpm.relase()
        elif buildResult == 1:
            os.chdir('../')
            raise Exception("The build function returned 1 (error).")
            #I think that only makepkg can do that.  Others would raise
            #an exception.
        else:
            os.chdir('../')
            fancyMsg("Building more AUR packages is required.")
            for package2 in buildResult:
                build(package2, True)
            build(package, True)
    except Exception as inst:
        fancyError(str(inst))

def syncCheck(dep, repos):
    #modded pycman.action_sync.find_sync_package()
    for db in repos.values():
        pkg = db.get_pkg(dep)
        if pkg is not None:
            return True, pkg
    return False

def buildSub(package):
    """
    This is the actual build function.  You shall not use it unless you
    will re-implement build().
    """

    try:
        #exists
        pkginfo = info(package)
        fancyMsg('Compiling package {0}...'.format(pkginfo[0]['Name']))
        showInfo(pkginfo[0])
        filename = pkginfo[0]['Name']+'.tar.gz'
        #Okay, this package exists, great.  Thanks, user.

        #download
        fancyMsg("Downloading: {0}".format(filename))
        rhandle = urllib.request.urlopen('http://aur.archlinux.org'+
                                         pkginfo[0]['URLPath'])
        size=''
        headers = rhandle.info()
        fhandle = open(filename, 'wb')
        fhandle.write(rhandle.read())
        fhandle.close()
        fancyMsg2(headers['Content-Length']+' bytes downloaded')

        #extracting
        fancyMsg("Extracting: {0}".format(filename))
        thandle = tarfile.open(filename, 'r:gz')
        thandle.extractall()
        names = thandle.getnames()
        fancyMsg2("extracted {0} files".format(len(names)))
        os.chdir('./'+pkginfo[0]['Name'])

        #predepcheck
        #Unlike the crappy perl version, we need to do some sanity checks.
        #Trust me: this would be a pain in the ass.  But hey, I was annoyed
        #when pacman said that there is no such package in the repos!
        phandle = open('PKGBUILD', 'r')
        pkgbuild = phandle.read()
        dep = re.search('^depends=.*', pkgbuild, re.MULTILINE)
        mkd = re.search('^makedepends=.*', pkgbuild, re.MULTILINE)
        phandle.close()
        if dep != None:
            depends = shlex.split(dep.group(0)[9:-1])
        else:
            depends = []
        if mkd != None:
            makedepends = shlex.split(mkd.group(0)[13:-1])
        else:
            makedepends = []
        bothdepends = depends + makedepends
        addonAUR = []
        addonAURUse = False

        #depcheck
        fancyMsg('Checking dependencies...')
        if bothdepends == []:
            #THANK YOU, DEVELOPER, FOR HAVING NO DEPS AND DESTROYING ME!
            fancyMsg2('none found')
        else:
            pycman.config.init_with_config('/etc/pacman.conf')
            db = pyalpm.get_localdb()
            #These lines appear THREE times in this script.  For a reason.
            #pyalpm is really, REALLY unstable, so I think that it might
            #break if I would use a function.       (of course it wouldn't.)
            for dep in bothdepends:
                if re.search('[<=>]', dep):
                    fancyMsg2('{0} must be in a specific version. Problems \
may occur if the package is from the AUR.'.format(dep))
                    vP = '>=<|><=|=><|=<>|<>=|<=>|>=|=>|><|<>|=<|<=|>|=|<'
                    verBase = re.split(vP, dep)
                    dep = verBase[0]
                    ver = verBase[1]
                pkg = db.get_pkg(dep)
                repos = dict((db.name,db) for db in pyalpm.get_syncdbs())
                if pkg != None:
                    fancyMsg2('{0}: found in system'.format(dep))
                elif syncCheck(dep, repos):
                    fancyMsg2('{0}: found in repos'.format(dep))
                elif info(dep):
                    fancyMsg2('{0}: found in the AUR, will build \
now'.format(dep))
                    addonAUR.append(dep)
                    addonAURUse = True
                else:
                    raise Exception("depcheck: cannot find {0} \
anywhere (system, repos, AUR)".format(dep))
            pyalpm.release()
            if addonAURUse == True:
                return addonAUR
        #build
        asroot = ''
        if os.geteuid() == 0:
            asroot = ' --asroot'
        return subprocess.call('/usr/bin/makepkg -si'+asroot, shell=True)
        #Is that it?  The main function takes only ONE LINE?!
        #Amazing.  I don't believe it.
    except urllib.error.URLError as inst:
        fancyError(str(inst))
    except urllib.error.HTTPError as inst:
        fancyError(str(inst))
    except IOError as inst:
        fancyError(str(inst))
    except Exception as inst:
        fancyError(str(inst))
    except KeyboardInterrupt as inst:
        fancyError('KeyboardInterrupt caught.')
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
    if args.upgrade == True:
        fancyError("Sorry, but this feature is not implemented yet...")

    if args.color == False:
        #That's awesome in variables AND this version.
        ALL_OFF=''
        BOLD=''
        BLUE=''
        GREEN=''
        RED=''
        YELLOW=''

    if args.info == True:
        for package in args.pkgs:
            pkg = info(package)
            category = pkg[0]['CategoryID']
            print("""Name           : {0}
Version        : {1}
URL            : {2}
Licenses       : {3}
Category       : {4}
Votes          : {5}
Out of Date    : {6}
Description    : {7}""".format(pkg[0]['Name'], pkg[0]['Version'],
                               pkg[0]['URL'], pkg[0]['License'],
                               categories[category], pkg[0]['NumVotes'],
                               pkg[0]['OutOfDate'],

                               pkg[0]['Description']))
            #pkg[0]['Maintainer'], pkg[0]['FirstSubmitted'].strftime(
            #'%Y-%m-%dT%H:%m:%SZ'), pkg[0]['LastModified'].strftime(
            #'%Y-%m-%dT%H:%m:%SZ'),
            #Xyne, hardcoding stuff is evil.

            #I tried to be simillar to pacman, so you can make a wrapper.
        exit(0)

    if args.search == True:
        pkgsearch = search(' '.join(args.pkgs)) #pacman-like behavior.
        for package in pkgsearch:
            if args.pac != True:
                showInfo(package, True)
            else:
                showInfo(package, False)
        exit(0)

    if args.pac == True:
        uid = os.geteuid()
        path = '/tmp/pkgbuilder-{0}'.format(str(uid))
        if os.path.exists(path) == False:
            os.mkdir(path)
        os.chdir(path)

    #If we didn't exit, we shall build the packages.
    for package in args.pkgs:
        build(package, args.valid)
        #This one is amazing, too.  See lines #225-#227.
#over 300 lines!  Compare this to build.pl's 56 (including ~8 useless...)
#New features will be included when they will be added to the AUR RPC.
# <http://aur.archlinux.org/rpc.php> (current: search info msearch)
#If something new will appear there, tell me through GH Issues or mail.
#Some other features might show up, too.
