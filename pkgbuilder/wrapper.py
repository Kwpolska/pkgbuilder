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
from .utils import Utils
import logging
import pyalpm
import pycman
import argparse
import sys

__wrapperversion__ = '0.1.0'

### wrapper()       A wrapper for pacman/PB ###
def wrapper(source='AUTO'):
    """A wrapper for pacman and PKGBUILDer."""
    # A very tricky way of getting all the pacman arguments.  Not for humans.
    pacmancommands = [['D', 'database'], ['Q', 'query'], ['R', 'remove'],
                     ['T', 'deptest'], ['U', 'upgrade']]
    pbcommands = [[None, 'nocolors'], [None, 'nodepcheck'], [None,
                   'novalidation'], [None, 'buildonly']]
    commoncommands = [['S', 'sync'], ['w', None], ['c', None], ['d', None],
                     ['v', None]]
    specialcommands = [['p', 'protocol']]

    pacmanshort = ['e', 'f', 'g', 'i', 'k', 'm', 'n', 'q', 't',
                   'u']
    pacmanlong = ['asdeps', 'asexplicit', 'cascade', 'changelog', 'check',
                  'clean', 'dbonly', 'debug', 'deps', 'downloadonly',
                  'explicit', 'force', 'foreign', 'groups', 'info',
                  'needed', 'noconfirm', 'nodeps', 'noprogressbar', 'nosave',
                  'noscriptlet', 'print', 'quiet', 'recursive', 'refresh',
                  'sysupgrade', 'unneeded', 'unrequired', 'upgrades',
                  'verbose']
    pacmanshorta = ['b', 'l', 'o', 'p', 'r', 's']
    pacmanlonga = ['arch', 'cachedir', 'config', 'dbpath', 'file', 'gpgdir',
                   'ignore', 'ignoregroup', 'list', 'logfile', 'owns',
                   'print-format', 'root', 'search']

    #TODO `list` and `protocol` SPECIAL PARSING; ALSO FOR CONFLICTING SHORTA

    parser = argparse.ArgumentParser(add_help=False, usage='usage:  %(prog)s \
<operation> [...]', argument_default=argparse.SUPPRESS)
    parser.add_argument('-h', '--help', action='store_true', default=False, dest='halp')
    parser.add_argument('-V', '--version', action='store_true', default=False, dest='ver')
    prog = parser.prog
    commands = pacmancommands + pbcommands + commoncommands

    parser.add_argument('pkgnames', nargs=argparse.REMAINDER)

    for i in commands:
        if i[0] is None:
            parser.add_argument('--'+i[1], action='store_true', default=False)
        elif i[1] is None:
            parser.add_argument('-'+i[0], action='store_true', default=False)
        else:
            parser.add_argument('-'+i[0], '--'+i[1], action='store_true',
                                default=False, dest=i[1])

    pacmann = pacmanshort + pacmanlong
    pacmana = pacmanshorta + pacmanlonga

    for i in pacmann:
        parser.add_argument('-'+i, action='store_true', default=False,
                            dest=i)

    # This is where shit gets real.
    for i in pacmana:
        parser.add_argument('-'+i, action='store', nargs='?', default='NIL',
                            dest=i)

    # Starting actual work.

    log = logging.getLogger('pbwrapper')
    log.info('*** PBwrapper v' + __version__)

    if source != 'AUTO':
        args = parser.parse_args(source)
    else:
        args = parser.parse_args()

    pyc = pycman.config.init_with_config('/etc/pacman.conf')
    localdb = pyc.get_localdb()

    if args.halp:
        # see pacman’s localizations
        print(_('usage:  {} <operation> [...]').format(sys.argv[0]))
        print('\n'+_('{}, a wrapper for pacman and PKGBUILDer.').format(prog))
        print(_('Pacman and PKGBUILDer syntaxes apply.  Consult their \
manpages/help commands for details.'))

    if args.ver:
        pacpkg = localdb.get_pkg('pacman')
        print("""PBWrapper v{}
{}
PKGBUILDer v{}
pacman v{}
pyalpm v{}""".format(__wrapperversion__, _('using:'), __version__,
                     pacpkg.version.split('-', 1)[0], pyalpm.version()))

    #args.pkgnames; args.__dict__

    if args.sync:
        print('We’re not done yet! --Billy Mays, may he rest in peace.')
