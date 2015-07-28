#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v4.0.3
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2015, Chris Warrick.
# See /LICENSE for licensing information.

"""
Main routine of PKGBUILDer.

:Copyright: © 2011-2015, Chris Warrick.
:License: BSD (see /LICENSE).
"""

from . import DS, _, __version__
from pkgbuilder.exceptions import NetworkError, PBException
import pkgbuilder.aur
import pkgbuilder.build
import pkgbuilder.exceptions
import pkgbuilder.transaction
import pkgbuilder.utils
import pkgbuilder.upgrade
import argparse
import os
import sys

__all__ = ('main',)


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
            prog='pkgbuilder',
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
            '-S', '--sync', action='store_true', default=False, dest='pac',
            help=_('build in /tmp'))
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
        argopr.add_argument(
            '-U', '--upgrade', action='store_true', default=False,
            dest='finst',
            help=_('move package files to pacman cache and install them'))
        argopr.add_argument(
            '-X', '--runtx', action='store_true', default=False, dest='runtx',
            help=_('run transactions from .tx files'))

        argopt = parser.add_argument_group(_('options'))
        argopt.add_argument(
            '-c', '--clean', action='store_true',
            default=False, dest='cleanup', help=_('clean up work files before '
                                                  'and after build'))
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
            '--skippgpcheck', action='store_true', default=False, dest='nopgp',
            help=_('do not verify source files with PGP signatures'))
        argopt.add_argument(
            '--noconfirm', action='store_true', default=False,
            dest='noconfirm', help=_('do not ask for any confirmation'))
        argopt.add_argument(
            '--deep', action='store_true', default=False, dest='deepclone',
            help=_('perform deep git clones'))
        argopt.add_argument(
            '-y', '--refresh', action='store_true', default=False,
            dest='pacupd', help=_('(dummy)'))

        if source != 'AUTO':
            args = parser.parse_args(source)
        else:
            args = parser.parse_args()

        DS.pacman = args.pac
        DS.cleanup = args.cleanup
        DS.nopgp = args.nopgp
        DS.noconfirm = args.noconfirm
        DS.deepclone = args.deepclone
        DS.validate = args.validate
        pkgnames = args.pkgnames

        if args.debug:
            DS.debugmode(nochange=True)
            DS.log.info('*** PKGBUILDer v{0}'.format(__version__))
            DS.log.debug('*** debug output on.')

        DS.log.info('Arguments parsed.  {0}'.format(args.__dict__))

        if 'VIRTUAL_ENV' in os.environ:
            DS.log.error("virtualenv detected, exiting.")
            DS.fancy_error(_("PKGBUILDer cannot work in a virtualenv, "
                             "exiting."))
            exit(83)

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
                        print(_("error: package '{0}' was not "
                                "found").format(i))
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
                output = output + pkgbuilder.utils.print_package_search(
                    pkg, True) + '\n'
            if output != '':
                print(output.rstrip())
            if quit:
                exit(0)

        if args.finst:
            # We do not know package names, and are unaware of signature files
            # Also, file names are where package names would usually be
            tx = pkgbuilder.transaction.Transaction(
                pkgnames=[],
                pkgpaths=pkgnames,
                sigpaths=[],
                filename=pkgbuilder.transaction.generate_filename(),
                delete=True)
            tx.run(standalone=False, validate=False)
            if quit:
                exit(tx.exitcode)

        if args.runtx:
            for fname in pkgnames:
                fname = os.path.abspath(fname)
                tx = pkgbuilder.transaction.Transaction.load(fname)
                tx.delete = DS.cleanup
                tx.run()
                if quit and tx.exitcode != 0:
                    exit(tx.exitcode)
            if quit:
                exit(0)

        if args.pac:
            DS.log.debug('-S passed, building in /tmp/.')
            path = '/tmp/pkgbuilder-{0}'.format(str(DS.uid))
            if not os.path.exists(path):
                os.mkdir(path)
            os.chdir(path)

        if args.upgrade > 0:
            DS.root_crash()
            DS.log.info('Starting upgrade...')
            dodowngrade = args.upgrade > 1
            upnames = pkgbuilder.upgrade.auto_upgrade(
                dodowngrade, args.vcsup, args.fetch)
            pkgnames = upnames + pkgnames

        if args.fetch and pkgnames:
            pkgbuilder.build.fetch_runner(pkgnames)
            if quit:
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
            if quit:
                exit(0)

        # If we didn't quit, we should build the packages.
        if pkgnames:
            DS.root_crash()

            DS.log.info('Starting build...')
            toinstall = []
            sigs = []
            tovalidate = set(pkgnames)

            for pkgname in pkgnames:
                try:
                    DS.log.info('Building {0}'.format(pkgname))
                    out = pkgbuilder.build.auto_build(pkgname, args.depcheck,
                                                      args.pkginst, pkgnames)
                    if out:
                        toinstall += out[1][0]
                        sigs += out[1][1]
                except PBException as e:
                    DS.fancy_error(str(e))
                    if e.exit:
                        exit(1)

            qs = len(tovalidate)

            if toinstall:
                tx = pkgbuilder.transaction.Transaction(
                    pkgnames=tovalidate,
                    pkgpaths=toinstall,
                    sigpaths=sigs,
                    asdeps=False,
                    filename=pkgbuilder.transaction.generate_filename(),
                    delete=True)
                tx.run(standalone=False, validate=DS.validate)
                qs = tx.exitcode
            if quit:
                DS.log.info('Quitting peacefully.')
                exit(qs)

    except NetworkError as e:
        DS.fancy_error(str(e))
        # TRANSLATORS: do not translate the word 'requests'.
        DS.fancy_error(_('PKGBUILDer (or the requests library) had '
                         'problems with fulfilling an HTTP request.'))
        if e.exit:
            exit(1)
    except PBException as e:
        DS.fancy_error(str(e))
        if e.exit:
            exit(1)
    except KeyboardInterrupt:
        pkgbuilder.DS.fancy_error(pkgbuilder.DS.inttext)
        exit(130)

    DS.log.info('Quitting peacefully.')

if __name__ == '__main__':
    main()
