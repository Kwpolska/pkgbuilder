#!/usr/bin/python3
# PKGBUILDer (Python3 release)
# Part of KRU
# Copyright Kwpolska 2011. Licensed under GPLv3.
#USAGE: ./build.py pkg1 [pkg2] [pkg3] (and more)

import pyalpm               # pyalpm in [extra]
import pycman               # pyalpm in [extra]
import AUR                  # python3-aur in [xyne-any] or AUR
import argparse
import sys
import os
import re
import shlex
import json
import pprint
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
    sys.stderr.write(YELLOW+'==> WARNING:'+ALL_OFF+BOLD+' '+text+ALL_OFF+"\n")

def fancyError(text):
    sys.stderr.write(RED+'==> ERROR:'+ALL_OFF+BOLD+' '+text+ALL_OFF+"\n")
#That's it.
categories = ['ERR0R', 'ERR1R', 'daemons', 'devel', 'editors', 'emulators',
'games', 'gnome', 'i18n', 'kde', 'kernels', 'lib', 'modules', 'multimedia',
'network', 'office', 'science', 'system', 'x11', 'xfce']
#If you can see ERR0R or ERR1R in the output, something bad has happened.
def info(pkgname, quiet):
    try:
        aur = AUR.AUR(threads=10)
        aur_pkgs = aur.info(pkgname)
        if aur_pkgs == []:
            if quiet == False:
                return None
            else:
                raise Exception("Cannot find the package `"+pkgname+"'.")
                #oh well, it WOULD make sense in the only quiet=True place.
        else:
            return aur_pkgs
    except Exception as inst:
        fancyError(str(inst))
        exit(1)

def search(pkgname):
    aur = AUR.AUR(threads=10)
    aur_pkgs = aur.search(pkgname)
    return aur_pkgs

def showInfo(package):
    pycman.config.init_with_config('/etc/pacman.conf')
    db = pyalpm.get_localdb()
    pkg = db.get_pkg(package['Name'])

    category = package['CategoryID']
    outofdate = ''
    installed = ''
    if package['OutOfDate'] == 1:
        outofdate=', '+RED+'out of date'+ALL_OFF
    if pkg != None:
        installed = ' [installed]'

    print("{0}/{1} {2} ({4} votes{5}){6}\n    {3}".format(categories[category],
          package['Name'], package['Version'], package['Description'],
          package['NumVotes'], outofdate, installed))

    pyalpm.release()
def build(package):
    buildResult = buildSub(package)
    try:
        if buildResult == 0:
            fancyMsg("The build function reported a proper build.")
            if args.valid == True:
                #check if installed
                pycman.config.init_with_config('/etc/pacman.conf')
                db = pyalpm.get_localdb()
                pkg = db.get_pkg(package)
                pyalpm.release()
                if pkg is None:
                    fancyError("validation: NOT installed")
                else:
                    fancyMsg2("validation: installed")
            elif buildResult == 1:
                raise Exception("The build function returned 1 (error).");
                #I think that only makepkg can do that.  Others would raise
                #an exception.
            elif buildResult == 22:
                #I hope makepkg never returns 22.
                fancyMsg("Building more AUR packages is required.")
                for package2 in addonAUR:
                    build(package2)
                build(package)
    except Exception as inst:
        fancyError(str(inst))

def buildSub(package):
    try:
        #exists
        pkginfo = info(package, False)
        fancyMsg('Compiling package {0}...'.format(pkginfo[0]['Name']))
        showInfo(pkginfo[0])
        filename = pkginfo[0]['Name']+'.tar.gz'
        #okay, this package exists.

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
        depends = shlex.split(dep.group(0)[9:-1])
        if mkd != None:
            makedepends = shlex.split(mkd.group(0)[13:-1])
        else:
            makedepends = []
        bothdepends = depends + makedepends

        #depcheck
        fancyMsg('Checking dependencies...')
        pycman.config.init_with_config('/etc/pacman.conf')
        db = pyalpm.get_localdb()
        #These lines appear THREE times in this script.  For a reason.
        #pyalpm is really, REALLY unstable, so I think that it might
        #break if I would use a function.
        for dep in bothdepends:
            if re.search('[<=>]', dep):
                fancyMsg2('{0} must be in a specific version. Problems may \
occur if the package is from the AUR.'.format(dep))
                vP = '>=<|><=|=><|=<>|<>=|<=>|>=|=>|><|<>|=<|<=|>|=|<'
                verBase = re.split(vP, dep)
                dep = verBase[0]
                ver = verBase[1]
            pkg = db.get_pkg(dep)
            repos = dict((db.name,db) for db in pyalpm.get_syncdbs())
            addonAUR = []
            addonAURUse = False
            if pkg != None:
                fancyMsg2('{0}: found in system'.format(dep))
            elif pycman.action_sync.find_sync_package(dep, repos):
                fancyMsg2('{0}: found in repos'.format(dep))
            elif info(dep, True):
                fancyMsg2('{0}: found in the AUR, will build now'.format(dep))
                addonAUR.append('dep')
                addonAURUse = True
            else:
                raise Exception("depcheck: cannot find {0}\
                anywhere (system, repos, AUR)".format(dep))
        pyalpm.release()
        if addonAURUse == True:
            return 22

        #build
        return subprocess.call('/usr/bin/makepkg -si', shell=True)
        #Is that it?  The main function takes only ONE LINE?! Amazing.
    except urllib.error.URLError as inst:
        fancyError(str(inst))
    except urllib.error.HTTPError as inst:
        fancyError(str(inst))
    except IOError as inst:
        fancyError(str(inst))
    except Exception as inst:
        fancyError(str(inst))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="An AUR helper (sort of.)")
    parser.add_argument('-C', '--nocolor', action='store_false',
                        default=True, dest='color', help="don't use colors")
    parser.add_argument('-V', '--novalidation', action='store_false',
                        default=True, dest='valid', help="don't check if\
packages were installed after build")

    parser.add_argument('-i', '--info', action='store_true', default=False,
                        dest='info', help="show package info")
    parser.add_argument('-s', '--search', action='store_true', default=False,
                        dest='search', help="search for a package")
    parser.add_argument('pkgs', metavar="PACKAGE", action='store', nargs='*',
                        help="packages to build")
    args = parser.parse_args()
    if args.color == False:
        ALL_OFF=''
        BOLD=''
        BLUE=''
        GREEN=''
        RED=''
        YELLOW=''

    if args.search == True:
        pkgsearch = search(' '.join(args.pkgs))
        for package in pkgsearch:
            showInfo(package)
        exit(0)

    if args.info == True:
        for package in args.pkgs:
            pkg = info(package, True)
            category = pkg[0]['CategoryID']
            print("""
Name           : {0}
Version        : {1}
Category       : {2}
Description    : {3}
URL            : {4}
License        : {5}
Votes          : {6}
Out of Date    : {7}""".format(pkg[0]['Name'], pkg[0]['Version'],
categories[category], pkg[0]['Description'], pkg[0]['URL'],
pkg[0]['License'], pkg[0]['NumVotes'], pkg[0]['OutOfDate']))
            exit(0)

    #oh, no exit?  fine then.  We need to build it.
    for package in args.pkgs:
        build(package)
#250 lines!  Compare this to build.pl's 56 (including ~8 useless...)
