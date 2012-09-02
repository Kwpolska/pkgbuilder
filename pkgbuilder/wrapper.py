#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PBWrapper v0.1.0
# PKGBUILDer v2.1.3.7
# An AUR helper (and library) in Python 3.
# Copyright (C) 2011-2012, Kwpolska.
# See /LICENSE for licensing information.

# Names convention: pkg = a package object, pkgname = a package name.

"""
    pkgbuilder.wrapper
    ~~~~~~~~~~~~~~~~~~
    A wrapper for pacman and PKGBUILDer.  (PBWrapper/pb)

    :Copyright: (C) 2011-2012, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, _, PBError, __version__
from .main import main
from .utils import Utils
import re
import logging
import pyalpm
import pycman
import argparse
import sys
import subprocess

__wrapperversion__ = '0.1.0'

### wrapper()       A wrapper for pacman/PB ###
def wrapper(source='AUTO'):
    """A wrapper for pacman and PKGBUILDer."""
    pyc = pycman.config.init_with_config('/etc/pacman.conf')
    localdb = pyc.get_localdb()
    # Because I need to work with -S and nothing else, I am going to use
    # regular expressions on the argument list.  Sorry.
    if source == 'AUTO':
        argst = sys.argv[1:]
    else:
        argst = source

    log = logging.getLogger('pbwrapper')
    if '--debug' in argst:
        DS.debugout()

    log.info('*** PBwrapper v{} (PKGBUILDer '
             '{})'.format(__wrapperversion__,  __version__))

    if (('-S' in argst) or ('--sync' in argst) or (re.search('-[a-zA-Z]*S',
                                                 ' '.join(argst))
                                                 is not None)):
        # The user has requested -S.
        pacmanshort = ['f', 'g', 'p', 'q']
        pacmanlong = ['asdeps', 'asexplicit', 'clean', 'dbonly',
                      'downloadonly', 'force', 'groups', 'needed',
                      'noconfirm', 'nodeps', 'noprogressbar', 'noscriptlet',
                      'print', 'quiet', 'verbose']
        pacmanshorta = ['b', 'l', 'r']
        pacmanlonga = ['arch', 'cachedir', 'config', 'dbpath', 'gpgdir',
                       'ignore', 'ignoregroup', 'list', 'logfile',
                       'print-format', 'root']
        pblong = ['nocolors', 'nodepcheck', 'novalidation', 'buildonly']
        commonshort = ['S', 'c', 'd', 'i', 's', 'u', 'v', 'w', 'y']
        commonlong = ['debug', 'info', 'refresh', 'search' ,'sync', 'sysupgrade']

        # This is a mess that needs to be cleaned up.
        allpacman = pacmanshort + pacmanlong + pacmanshorta + pacmanlonga
        allpb = pblong
        allcommon = commonshort + commonlong
        allcmd = allpacman + allpb + allcommon

        allshort = pacmanshort + commonshort
        alllong = pacmanlong + pblong + commonlong

        parser = argparse.ArgumentParser(add_help=False, usage='%(prog)s '
                                         '<operation> [...]',
                                         argument_default=argparse.SUPPRESS)
        parser.add_argument('-h', '--help', action='store_true',
                            default=False, dest='help')
        parser.add_argument('-V', '--version', action='store_true',
                            default=False, dest='ver')

        for i in allshort:
            parser.add_argument('-' + i, action='store_true', default=False,
                                dest=i)

        for i in alllong:
            parser.add_argument('--' + i, action='store_true', default=False,
                                dest=i)

        for i in pacmanshorta:
            parser.add_argument('-' + i, action='store', nargs=1,
                                default='NIL', dest=i)

        for i in pacmanlonga:
            parser.add_argument('--' + i, action='store', nargs=1,
                                default='NIL', dest=i)

        parser.add_argument('pkgnames', action='store', nargs='*')

        # Starting actual work.

        if source != 'AUTO':
            args = parser.parse_args(source)
        else:
            args = parser.parse_args()

        try:
            pkgnames = args.pkgnames
        except AttributeError:
            pkgnames = []

        execargs = []
        pacargs = []
        pbargs = []

        for i in args.__dict__.items():
            if i[1] is not False:
                # == This argument has been provided.
                if i[1] == True:
                    # == This argument doesn't have a value.
                    if i[0] in allshort:
                        execargs.append('-' + i[0])
                    elif i[0] in alllong:
                        execargs.append('--' + i[0])

        for i in execargs:
            if i[1:] in allshort:
                s = i[1:]
            elif i[2:] in alllong:
                s = i[2:]
            else:
                raise PBError('argparse broke')

            if s in allcommon:
                pacargs.append(i)
                pbargs.append(i)

            if s in allpacman:
                pacargs.append(i)
            elif s in allpb:
                pbargs.append(i)

        for i in args.__dict__.items():
            if i[1] is not False and i[1] != 'NIL':
                # == This argument can take values and has one.
                if i[0] in pacmanshorta:
                    pacargs.append('-' + i[0])
                    pacargs.append(i[1][0])
                elif i[0] in pacmanlonga:
                    pacargs.append('--' + i[0])
                    pacargs.append(i[1][0])

        if args.u or args.sysupgrade or args.search or args.s:
            subprocess.call(['pacman'] + pacargs + pkgnames)
            main(pbargs)
        elif args.y or args.refresh or args.l != 'NIL' or args.list != 'NIL':
            subprocess.call(['pacman'] + pacargs + pkgnames)
        else:
            pacmanpkgnames = []
            pbpkgnames = []
            utils = Utils()
            for i in pkgnames:
                if utils.info(i) is None:
                    pacmanpkgnames.append(i)
                else:
                    pbpkgnames.append(i)

            if pacmanpkgnames != []:
                subprocess.call(['pacman'] + pacargs + pacmanpkgnames)

            if pbpkgnames != []:
                main(pbargs + pbpkgnames)

    elif ('-h' in argst) or ('--help' in argst):
        # TRANSLATORS: see pacman’s localizations
        print(_('usage:  {} <operation> [...]').format(sys.argv[0]))
        print('\n' + _('{}, a wrapper for pacman and '
              'PKGBUILDer.').format('pb'))
        print(_('Pacman and PKGBUILDer syntaxes apply.  Consult their ' \
                'manpages/help commands for details.'))


    elif ('-V' in argst) or ('--version' in argst):
        pacpkg = localdb.get_pkg('pacman')
        print("""PBWrapper   v{}
PKGBUILDer  v{}
pacman      v{}
pyalpm      v{}""".format(__wrapperversion__, __version__,
                          pacpkg.version.split('-', 1)[0],
                          pyalpm.version()))
    else:
        subprocess.call(['pacman'] + argst)
