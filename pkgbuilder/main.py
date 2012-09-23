#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.5
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2012, Kwpolska.
# See /LICENSE for licensing information.

# Names convention: pkg = a package object, pkgname = a package name.

"""
    pkgbuilder.main()
    ~~~~~~~~~~~~~~~~
    Main routine of PKGBUILDer.

    :Copyright: © 2011-2012, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, _, PBError, __version__
from .build import Build
from .utils import Utils
from .upgrade import Upgrade
import argparse
import os
import subprocess


### main()          The main routine        ###
def main(source='AUTO', noquit=False):
    """Main routine of PKGBUILDer."""
    try:
        verstring = 'PKGBUILDer v'+__version__
        # TRANSLATORS: translate the whole sentence.
        # Alternatively, use translation instead of locale.
        locale = _('LANG locale by AUTHOR <MAIL@IF.YOU.WANT>')
        if locale != 'LANG locale by AUTHOR <MAIL@IF.YOU.WANT>':
            verstring = '\n'.join([verstring, locale])
        DS.log.info('Initialized, parsing arguments.')
        parser = argparse.ArgumentParser(description=_('An AUR helper'
            ' (and library) in Python 3.'),
            formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument('-V', '--version', action='version',
                            version=verstring,
                            help=_('show version number and quit'))
        parser.add_argument('pkgs', metavar='PACKAGE', action='store',
                            nargs='*', help=_('packages to build'))

        argopt = parser.add_argument_group(_('options'))
        argopr = parser.add_argument_group(_('operations'))
        argopt.add_argument('-c', '--clean', action='store_true',
                            default=True, dest='cleanup', help=_('clean up '
                            'work files after build'))
        argopt.add_argument('-C', '--nocolors', action='store_false',
                            default=True, dest='color', help=_('don\'t use '
                            'colors in output'))
        argopt.add_argument('--debug', action='store_true', default=False,
                            dest='debug', help=_('display debug messages'))
        argopt.add_argument('-d', '--nodepcheck', action='store_false',
                            default=True, dest='depcheck', help=_('don\'t '
                            'check dependencies (may break makepkg)'))
        argopt.add_argument('-D', '--vcsupgrade', action='store_true',
                            default=False, dest='vcsup', help=_('upgrade '
                            'all the VCS/date-versioned packages'))
        argopt.add_argument('-v', '--novalidation', action='store_false',
                            default=True, dest='valid', help=_('don\'t check '
                            'if packages were installed after build'))
        argopt.add_argument('-w', '--buildonly', action='store_false',
                            default=True, dest='pkginst', help=_('don\'t '
                            'install packages after building'))
        argopt.add_argument('-P', '--protocol', action='store',
                            default='http', dest='protocol',
                            metavar=_('PROTOCOL'), help=_('choose '
                            'protocol (default: http)'))
        argopt.add_argument('-S', '--sync', action='store_true', default=False,
                            dest='pac', help=_('pacman-like mode'))
        argopt.add_argument('-y', '--refresh', action='store_true',
                            default=False, dest='pacupd', help=_('(dummy)'))
        argopr.add_argument('-i', '--info', action='store_true', default=False,
                            dest='info', help=_('view package information'))
        argopr.add_argument('-s', '--search', action='store_true',
                            default=False, dest='search', help=_('search the '
                            'AUR for matching strings'))
        argopr.add_argument('-u', '--sysupgrade', action='count',
                            default=False, dest='upgrade',
                            help=_('upgrade installed AUR packages'))

        if source != 'AUTO':
            args = parser.parse_args(source)
        else:
            args = parser.parse_args()

        DS.validate = args.valid
        DS.depcheck = args.depcheck
        DS.pacman = args.pac
        DS.pkginst = args.pkginst
        DS.protocol = args.protocol
        DS.cleanup = args.cleanup
        utils = Utils()
        build = Build()
        upgrade = Upgrade()

        if args.debug:
            DS.debugmode(nochange=True)
            DS.log.info('*** PKGBUILDer v{}'.format(__version__))
            DS.log.debug('*** debug output on.')

        DS.log.info('Arguments parsed.  {}'.format(args.__dict__))

        if not args.color:
            DS.colorsoff()
            DS.log.debug('Colors turned off.')

        if args.info:
            DS.log.debug('Showing info...')
            for pkgname in args.pkgs:
                utils.print_package_info(utils.info(pkgname))

                exit(0)

        if args.search:
            DS.log.debug('Searching...')
            searchstring = '+'.join(args.pkgs)
            if len(searchstring) < 3:
                # this would be too many entries, but this is an actual API
                # limitation and not an idea of yours truly.
                DS.fancy_error(_('Search query too short, API limitation'))
                DS.fancy_msg(_('Searching for exact match...'))
                search = [utils.info(searchstring)]
                if search == [None]:
                    DS.fancy_error2(_('not found'))
                    exit(0)
                else:
                    utils.print_package_search(search[0], prefix=(
                                               DS.colors['blue'] + '  ->' +
                                               DS.colors['all_off'] +
                                               DS.colors['bold'] + ' '),
                                               prefixp='  -> ')
                    print(DS.colors['all_off'], end='')
                    exit(0)
            else:
                search = utils.search(searchstring)

            output = ''
            for pkg in search:
                if args.pac:
                    output = output + utils.print_package_search(pkg, False,
                                                                 True) + '\n'
                else:
                    output = output + utils.print_package_search(pkg, True,
                                                                 True) + '\n'
            if output != '':
                print(output.rstrip())
            exit(0)

        if args.pac:
            DS.log.debug('-S passed, building in /tmp/.')
            uid = os.geteuid()
            path = '/tmp/pkgbuilder-{}'.format(str(uid))
            if not os.path.exists(path):
                os.mkdir(path)
            os.chdir(path)

    except PBError as inst:
        DS.fancy_error(str(inst))
        exit(0)

    if args.upgrade > 0:
        DS.log.info('Starting upgrade...')
        dodowngrade = args.upgrade > 1
        upgrade.auto_upgrade(dodowngrade, args.vcsup)

        if not noquit:
            exit(0)

    # If we didn't quit, we should build the packages.
    if args.pkgs:
        DS.log.info('Starting build...')
        toinstall = []
        for pkgname in args.pkgs:
            DS.log.info('Building {}'.format(pkgname))
            toinstall += build.auto_build(pkgname, DS.depcheck, DS.pkginst)

        if toinstall:
            build.install(toinstall)

        if DS.validate:
            build.validate(args.pkgs)

    DS.log.info('Quitting.')
