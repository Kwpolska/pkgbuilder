#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v3.1.5
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2014, Kwpolska.
# See /LICENSE for licensing information.

"""
    pkgbuilder.main
    ~~~~~~~~~~~~~~~

    Main routine of PKGBUILDer.

    :Copyright: © 2011-2014, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, _, __version__
from pkgbuilder.exceptions import NetworkError, PBException
import pkgbuilder.build
import pkgbuilder.exceptions
import pkgbuilder.utils
import pkgbuilder.upgrade
import argparse
import os
import sys

__all__ = ['main']


def main(source='AUTO', quit=True):
    """Main routine of PKGBUILDer."""
    try:
        verstring = 'PKGBUILDer v' + __version__
        # TRANSLATORS: translate the whole sentence.
        # Alternatively, use translation instead of locale.
        locale = _('LANG locale by AUTHOR <MAIL@IF.YOU.WANT>')
        if locale != 'LANG locale by AUTHOR <MAIL@IF.YOU.WANT>':
            verstring = ' — '.join([verstring, locale])
        DS.log.info('Initialized, parsing arguments.')
        parser = argparse.ArgumentParser(
            description=_('An AUR helper (and library) in Python 3.'),
            epilog=_('Also accepting ABS packages.'))
        parser.add_argument(
            '-V', '--version', action='version', version=verstring,
            help=_('show version number and quit'))
        parser.add_argument(
            'pkgnames', metavar=_('PACKAGE'), action='store', nargs='*',
            help=_('AUR/ABS packages to build'))

        argopr = parser.add_argument_group(_('operations'))
        argopr.add_argument(
            '-F', '--fetch', action='store_true', default=False, dest='fetch',
            help=_('fetch package files'))
        argopr.add_argument(
            '--userfetch', action='append', dest='userfetch',
            metavar=_('USER'), help=_('fetch all package files of an user'))
        argopr.add_argument('-i', '--info', action='store_true', default=False,
                            dest='info', help=_('view package information'))
        argopr.add_argument(
            '-s', '--search', action='store_true',
            default=False, dest='search', help=_('search the AUR for '
                                                 'matching strings'))
        argopr.add_argument(
            '-u', '--sysupgrade', action='count', default=False,
            dest='upgrade', help=_('upgrade installed AUR packages'))

        argopt = parser.add_argument_group(_('options'))
        argopt.add_argument(
            '-c', '--clean', action='store_true',
            default=False, dest='cleanup', help=_('clean up work files after '
                                                  'build'))
        argopt.add_argument(
            '-C', '--nocolors', action='store_false',
            default=True, dest='color', help=_('don\'t use colors in output'))
        argopt.add_argument(
            '--debug', action='store_true', default=False,
            dest='debug', help=_('display debug messages'))
        argopt.add_argument(
            '-d', '--nodepcheck', action='store_false',
            default=True, dest='depcheck', help=_('don\'t check dependencies '
                                                  '(may break makepkg)'))
        argopt.add_argument(
            '-D', '--vcsupgrade', action='store_true',
            default=False, dest='vcsup', help=_('upgrade all the VCS/'
                                                'date-versioned packages'))
        argopt.add_argument(
            '-v', '--novalidation', action='store_false',
            default=True, dest='validate',
            help=_('don\'t check if packages were installed after build'))
        argopt.add_argument(
            '-w', '--buildonly', action='store_false',
            default=True, dest='pkginst', help=_('don\'t  install packages '
                                                 'after building'))
        argopt.add_argument(
            '-S', '--sync', action='store_true', default=False, dest='pac',
            help=_('pacman-like mode'))
        argopt.add_argument(
            '--safeupgrade', action='store_true', default=False,
            dest='safeupgrade', help=_('perform a failsafe upgrade of '
                                       'PKGBUILDer'))
        argopt.add_argument(
            '-y', '--refresh', action='store_true', default=False,
            dest='pacupd', help=_('(dummy)'))

        if source != 'AUTO':
            args = parser.parse_args(source)
        else:
            args = parser.parse_args()

        DS.pacman = args.pac
        DS.cleanup = args.cleanup
        pkgnames = args.pkgnames

        if args.debug:
            DS.debugmode(nochange=True)
            DS.log.info('*** PKGBUILDer v{0}'.format(__version__))
            DS.log.debug('*** debug output on.')

        DS.log.info('Arguments parsed.  {0}'.format(args.__dict__))

        if not args.color:
            DS.colorsoff()
            DS.log.debug('Colors turned off.')

        if args.info:
            DS.log.debug('Showing info...')

            pkgs = pkgbuilder.utils.info(pkgnames)
            foundnames = [i.name for i in pkgs]
            if pkgs:
                pkgbuilder.utils.print_package_info(pkgs)
                qs = 0
            else:
            for i in pkgnames:
                if i not in foundnames:
                    print(_("error: package '{0}' was not found").format(i))
                    qs = 1
            if quit:
                exit(qs)

        if args.search:
            if not pkgnames:
                if quit:
                    exit(1)
            else:
                DS.log.debug('Searching...')
                searchstring = '+'.join(pkgnames)
                if len(searchstring) < 2:
                    # this would be too many entries, but this is an actual API
                    # limitation and not an idea of yours truly.
                    DS.fancy_error(_('Search query too short'))
                    DS.fancy_msg(_('Searching for exact match...'))
                    search = pkgbuilder.utils.info([searchstring])
                    if search == []:
                        DS.fancy_error2(_('not found'))
                        if quit:
                            exit(0)
                    else:
                        pkgbuilder.utils.print_package_search(
                            search[0], prefix=(DS.colors['blue'] + '  ->' +
                                               DS.colors['all_off'] +
                                               DS.colors['bold'] + ' '),
                            prefixp='  -> ')
                        sys.stdout.write(DS.colors['all_off'])
                        if quit:
                            exit(0)
                else:
                    search = pkgbuilder.utils.search(searchstring)

            output = ''
            for pkg in search:
                if args.pac:
                    output = output + pkgbuilder.utils.print_package_search(
                        pkg, False, True) + '\n'
                else:
                    output = output + pkgbuilder.utils.print_package_search(
                        pkg, True, True) + '\n'
            if output != '':
                print(output.rstrip())
            if quit:
                exit(0)

        if args.pac:
            DS.log.debug('-S passed, building in /tmp/.')
            uid = os.geteuid()
            path = '/tmp/pkgbuilder-{0}'.format(str(uid))
            if not os.path.exists(path):
                os.mkdir(path)
            os.chdir(path)

        if args.safeupgrade:
            DS.fancy_msg(_('PKGBUILDer Failsafe Upgrade'))
            query = (DS.colors['green'] + '==>' +
                     DS.colors['all_off'] + DS.colors['bold'] + ' ' +
                     _('Build the git version? [y/N] ') +
                     DS.colors['all_off'])

            yesno = input(query)

            if yesno.lower().strip().startswith('y'):
                pkgname = 'pkgbuilder-git'
            else:
                pkgname = 'pkgbuilder'

            mpstatus = pkgbuilder.build.safeupgrade(pkgname)

            exit(mpstatus)

        if args.upgrade > 0:
            DS.log.info('Starting upgrade...')
            dodowngrade = args.upgrade > 1
            upnames = pkgbuilder.upgrade.auto_upgrade(dodowngrade, args.vcsup)
            pkgnames = upnames + pkgnames

        if args.fetch:
            pkgbuilder.build.fetch_runner(pkgnames)
            exit(0)

        if args.userfetch:
            tofetch = []
            print(':: ' + _('Fetching package information...'))
            for u in args.userfetch:
                try:
                    tofetch += pkgbuilder.utils.msearch(u)
                except pkgbuilder.exceptions.AURError as e:
                    print(_('Error while processing {0}: {1}').format(u, e))

            pkgbuilder.build.fetch_runner(tofetch, preprocessed=True)
            exit(0)

        # If we didn't quit, we should build the packages.
        if pkgnames:
            if DS.uid == 0:
                DS.log.warning('Running as root! (UID={0})'.format(DS.uid))
                DS.fancy_warning(_('Running PKGBUILDer as root can break your '
                                   'system!'))

            DS.log.info('Starting build...')
            toinstall = []
            sigs = []
            tovalidate = set(pkgnames)

            for pkgname in pkgnames:
                DS.log.info('Building {0}'.format(pkgname))
                out = pkgbuilder.build.auto_build(pkgname, args.depcheck,
                                                  args.pkginst, pkgnames)
                if out:
                    toinstall += out[1][0]
                    sigs += out[1][1]

            if toinstall:
                pkgbuilder.build.install(toinstall, sigs, asdeps=False)

            if args.validate and tovalidate:
                DS.log.info('Quitting peacefully.')
                exit(pkgbuilder.build.validate(tovalidate))
    except NetworkError as e:
        DS.fancy_error(str(e))
        # TRANSLATORS: do not translate the word 'requests'.
        DS.fancy_error(_('PKGBUILDer (or the requests library) had '
                         'problems with fulfilling an HTTP request.'))
        exit(1)
    except PBException as e:
        DS.fancy_error(str(e))
        exit(1)

    DS.log.info('Quitting peacefully.')
