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
    # Because I need only -S, I am going to only use regexps on the list.
    # Sorry.
    if source == 'AUTO':
        source = sys.argv
        args = source[1:]  # Temporary!
    else:
        args = source

    log = logging.getLogger('pbwrapper')
    if '--debug' in args:
        DS.debugout()

    log.info('*** PBwrapper v{} (PKGBUILDer '
             '{})'.format(__wrapperversion__,  __version__))

    if (('-S' in args) or ('--sync' in args) or (re.search('-[a-zA-Z]*S',
                                                 ' '.join(args))
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

        parser = argparse.ArgumentParser(add_help=False, usage='usage:  %(prog)s '
                                         '<operation> [...]',
                                         argument_default=argparse.SUPPRESS)
        parser.add_argument('-h', '--help', action='store_true',
                            default=False, dest='help')
        parser.add_argument('-V', '--version', action='store_true',
                            default=False, dest='ver')
        parser.add_argument('pkgnames', nargs=argparse.REMAINDER)


        for i in allshort:
            parser.add_argument('-' + i, action='store_true', default=False,
                                dest=i)

        for i in alllong:
            parser.add_argument('--' + i, action='store_true', default=False,
                                dest=i)

        for i in pacmanshorta:
            parser.add_argument('-' + i, action='store', nargs='?',
                                default='NIL', dest=i)

        for i in pacmanlonga:
            parser.add_argument('--' + i, action='store', nargs='?',
                                default='NIL', dest=i)

        # Starting actual work.

        if source != 'AUTO':
            args = parser.parse_args(source)
        else:
            args = parser.parse_args()

    #args.pkgnames; args.__dict__

        execargs = []
        for i in args.__dict__.items():
            if i[1] is not False:
                # == This argument has been provided.
                if i[1] == True:
                    # == This argument doesn't have a value.
                    if i[0] in allshort:
                        execargs.append('-' + i[0])
                    elif i[0] in alllong:
                        execargs.append('--' + i[0])

        pacargs = [i for i in execargs if i in allpacman]
        pbargs = [i for i in execargs if i in allpb]

        for i in args.__dict__.items():
            if i[1] is not False and i[1] != 'NIL':
                # == This argument can take values and has one.
                if i[0] in pacmanlonga:
                    pacargs.append('-' + i[0])
                    pacargs.append(i[1])
                elif i[0] in pacmanshorta:
                    pacargs.append('--' + i[0])
                    pacargs.append(i[1])

        if args.u or args.sysupgrade or args.search or args.s:
            subprocess.call(['pacman'] + pacargs)
            main(pbargs)
        else:
            pacmanpkgnames = []
            pbpkgnames = []
            utils = Utils()
            for i in args.pkgnames:
                if utils.info(i) is None:
                    pacmanpkgnames.append(i)
                else:
                    pbpkgnames.append(i)

            if pacmanpkgnames != []:
                subprocess.call(['pacman'] + pacargs + pacmanpkgnames)

            if pbpkgnames != []:
                main(pbargs + pacmanpkgnames)

    elif ('-h' in args) or ('--help' in args):
        # TRANSLATORS: see pacman’s localizations
        print(_('usage:  {} <operation> [...]').format(sys.argv[0]))
        print('\n' + _('{}, a wrapper for pacman and '
              'PKGBUILDer.').format('pb'))
        print(_('Pacman and PKGBUILDer syntaxes apply.  Consult their ' \
                'manpages/help commands for details.'))


    elif ('-V' in args) or ('--version' in args):
        pacpkg = localdb.get_pkg('pacman')
        print("""PBWrapper   v{}
PKGBUILDer  v{}
pacman      v{}
pyalpm      v{}""".format(__wrapperversion__, __version__,
                          pacpkg.version.split('-', 1)[0],
                          pyalpm.version()))
    else:
        subprocess.call(['pacman'] + args)
