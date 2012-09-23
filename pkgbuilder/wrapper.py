#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PBWrapper v0.1.2
# PKGBUILDer v2.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.5
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2012, Kwpolska.
# See /LICENSE for licensing information.

# Names convention: pkg = a package object, pkgname = a package name.

"""
    pkgbuilder.wrapper
    ~~~~~~~~~~~~~~~~~~
    A wrapper for pacman and PKGBUILDer.  (PBWrapper/pb)

    :Copyright: © 2011-2012, Kwpolska.
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
import os
import subprocess

__wrapperversion__ = '0.1.3'

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
        DS.debugmode()

    log.info('*** PBwrapper v{} (PKGBUILDer '
             '{})'.format(__wrapperversion__, __version__))

    if (('-S' in argst) or ('--sync' in argst) or (re.search('-[a-zA-Z]*S',
                                                             ' '.join(argst))
                                                   is not None)):
        # The user has requested -S.
        # -l/--list is in not in *a because it takes over the whole package
        # list, and that is a workaround.
        log.debug('Got -S, preparing to parse arguments...')
        pacmanshort = ['f', 'g', 'l', 'p', 'q']
        pacmanlong = ['asdeps', 'asexplicit', 'dbonly', 'downloadonly',
                      'force', 'groups', 'list',  'needed', 'noconfirm',
                      'nodeps', 'noprogressbar', 'noscriptlet', 'print',
                      'quiet', 'verbose']
        pacmanshorta = ['b', 'r']
        pacmanlonga = ['arch', 'cachedir', 'config', 'dbpath', 'gpgdir',
                       'ignore', 'ignoregroup', 'logfile', 'print-format',
                       'root']

        pbshort = ['D', 'C']
        pblong = ['vcsupgrade', 'nocolors', 'nodepcheck', 'novalidation',
                  'buildonly']
        pbshorta = ['P']
        pblonga = ['protocol']

        commonshort = ['S', 'd', 'i', 's', 'v', 'w']
        commonlong = ['debug', 'info', 'search', 'sync']
        commonshortc = ['c', 'y', 'u']
        commonlongc = ['clean', 'refresh', 'sysupgrade']

        allpacman = pacmanshort + pacmanlong + pacmanshorta + pacmanlonga
        allpb = pbshort + pblong + pbshorta + pblonga
        allcommon = commonshort + commonlong + commonshortc + commonlongc
        allcmd = allpacman + allpb + allcommon

        allshort = pacmanshort + pbshort + commonshort
        alllong = pacmanlong + pblong + commonlong

        allshortc = commonshortc
        alllongc = commonlongc
        allcountable = allshortc + alllongc

        parser = argparse.ArgumentParser(add_help=False, usage=_('%(prog)s'
                                         ' <operation> [...]'),
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

        for i in allshortc:
            parser.add_argument('-' + i, action='count', dest=i)

        for i in alllongc:
            parser.add_argument('--' + i, action='count', dest=i)

        for i in pacmanshorta:
            parser.add_argument('-' + i, action='store', nargs=1,
                                default='NIL', dest=i)

        for i in pacmanlonga:
            parser.add_argument('--' + i, action='store', nargs=1,
                                default='NIL', dest=i)

        parser.add_argument('-P', '--protocol', action='store',
                            default='http', dest='protocol')

        parser.add_argument('pkgnames', action='store', nargs='*')

        # Starting actual work.

        if source != 'AUTO':
            args = parser.parse_args(source)
        else:
            args = parser.parse_args()

        log.debug('Arguments parsed.  {}'.format(args.__dict__))

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
                if i[0] in allcountable:
                    # == This is a countable argument.
                    if i[0] in allshortc:
                        for x in range(i[1]):
                            execargs.append('-' + i[0])
                    elif i[0] in alllongc:
                        for x in range(i[1]):
                            execargs.append('--' + i[0])
                elif i[1]:
                    # == This argument doesn't have a value.
                    if i[0] in allshort:
                        execargs.append('-' + i[0])
                    elif i[0] in alllong:
                        execargs.append('--' + i[0])

        for i in execargs:
            if i[1:] in allshort + allshortc:
                s = i[1:]
            elif i[2:] in alllong + alllongc:
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

        pbargs.append('--protocol')
        pbargs.append(args.protocol)

        log.debug('Preparing to run pacman and/or PKGBUILDer...')

        if args.search or args.s:
            log.debug('Got -s.')
            log.info('Running pacman.')
            subprocess.call([DS.paccommand] + pacargs + pkgnames)
            log.info('Running pkgbuilder (pkgbuilder.main.main()).')
            main(pbargs + pkgnames)
            exit()
        elif args.l or args.list:
            log.debug('Got -l.')
            log.info('Running pacman.')
            subprocess.call([DS.paccommand] + pacargs + pkgnames)
            exit()
        elif args.u or args.sysupgrade:
            log.debug('Got -u.')
            log.info('Running pacman.')
            if DS.hassudo:
                subprocess.call(['sudo', DS.paccommand] + pacargs)
            else:
                subprocess.call('su -c "{} {}"'.format(DS.paccommand,
                                                       ''.join(pacargs)))
            log.info('Running pkgbuilder (pkgbuilder.main.main()).')
            main(pbargs, noquit=True)
        elif args.y or args.refresh:
            log.debug('Got -y.')
            log.info('Running pacman.')
            if DS.hassudo:
                subprocess.call(['sudo', DS.paccommand] + pacargs)
            else:
                subprocess.call('su -c "{} {}"'.format(DS.paccommand,
                                                       ''.join(pacargs)))

        log.debug('Generating AUR packages list...')
        pacmanpkgnames = []
        pbpkgnames = []
        utils = Utils()
        for i in pkgnames:
            if utils.info(i) is None:
                pacmanpkgnames.append(i)
            else:
                pbpkgnames.append(i)

        droppable = ['-u', '-y', '--sysupgrade', '--refresh']

        pacargs = [i for i in pacargs if i not in droppable]
        pbargs = [i for i in pbargs if i not in droppable]

        log.debug('Generated.')

        if pacmanpkgnames != []:
            log.info('Running pacman.')
            if DS.hassudo:
                subprocess.call(['sudo', DS.paccommand] + pacargs +
                                pacmanpkgnames)
            else:
                subprocess.call('su -c "{} {} {}"'.format(DS.paccommand,
                                                          ''.join(pacargs),
                                                          pacmanpkgnames))
        else:
            log.info('No repo packages in the list.')

        if pbpkgnames != []:
            log.info('Running pkgbuilder (pkgbuilder.main.main()).')
            main(pbargs + pbpkgnames)
        else:
            log.info('No AUR packages in the list.')

        sanitycheck = set(pacmanpkgnames + pbpkgnames)
        if sanitycheck != set(pkgnames):
            log.info('Running pacman due to failed sanity check.')
            sanityargs = [item for item in pkgnames if (item not in
                          sanitycheck)]
            if DS.hassudo:
                subprocess.call(['sudo', DS.paccommand] + pacargs +
                                pacmanpkgnames)
            else:
                subprocess.call('su -c "{} {} {}"'.format(DS.paccommand,
                                                          ''.join(pacargs),
                                                          sanityargs))
    elif ('-h' in argst) or ('--help' in argst):
        # TRANSLATORS: see pacman’s localizations
        print(_('usage: {} <operation> [...]').format(
            os.path.basename(sys.argv[0])))
        print('\n' + _('{}, a wrapper for pacman and '
              'PKGBUILDer.').format('pb'))
        print(_('Pacman and PKGBUILDer syntaxes apply.  Consult their '
                'manpages/help commands for details.'))

    elif ('-V' in argst) or ('--version' in argst):
        pacpkg = localdb.get_pkg('pacman')
        print("""PBWrapper   v{}
PKGBUILDer  v{}
pacman      v{}
pyalpm      v{}""".format(__wrapperversion__, __version__,
                          pacpkg.version.split('-', 1)[0],
                          pyalpm.version()))
    elif 'UTshibboleet' in argst:
        if argst[0] == 'unittests' and argst[1] == 'UTshibboleet':
            # http://xkcd.com/806/
            pass
        else:
            print('Please don’t use the reserved UTshibboleet argument.')
    else:
        if DS.hassudo:
            subprocess.call(['sudo', DS.paccommand] + argst)
        else:
            subprocess.call('su -c "{} {}"'.format(DS.paccommand,
                                                   ''.join(argst)))
