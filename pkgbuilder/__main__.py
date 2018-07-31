# -*- encoding: utf-8 -*-
# PKGBUILDer v4.2.18
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2018, Chris Warrick.
# See /LICENSE for licensing information.

"""
Main routine of PKGBUILDer.

:Copyright: © 2011-2018, Chris Warrick.
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
            epilog=_('Also accepts repository packages to build from source.'))
        parser.add_argument(
            '-V', '--version', action='version', version=verstring,
            help=_('show version number and quit'))
        parser.add_argument(
            'pkgnames', metavar=_('PACKAGE'), action='store', nargs='*',
            help=_('AUR/repository packages to build'))

        argopr = parser.add_argument_group(_('operations'))
        argopr.add_argument(
            '-S', '--sync', action='store_true', dest='pac',
            help=_('build in /tmp'))
        argopr.add_argument(
            '-F', '--fetch', '-G', '--get', action='store_true', dest='fetch',
            help=_('fetch package files'))
        argopr.add_argument(
            '--userfetch', action='append', dest='userfetch',
            metavar=_('USER'), help=_('fetch all package files of an user'))
        argopr.add_argument('-i', '--info', action='store_true', dest='info',
                            help=_('view package information'))
        argopr.add_argument(
            '-s', '--search', action='store_true', dest='search',
            help=_('search the AUR for matching strings'))
        argopr.add_argument(
            '-u', '--sysupgrade', action='count', default=False,
            dest='upgrade', help=_('upgrade installed AUR packages'))
        argopr.add_argument(
            '-U', '--upgrade', action='store_true', dest='finst',
            help=_('move package files to pacman cache and install them'))
        argopr.add_argument(
            '-X', '--runtx', action='store_true', dest='runtx',
            help=_('run transactions from .tx files'))

        argopt = parser.add_argument_group(_('options'))

        argopt.add_argument(
            '-c', '--clean', action='store_true', dest='clean',
            help=_('clean up work files before and after build'))
        argopt.add_argument(
            '--noclean', action='store_true', dest='noclean',
            help=_('don\'t clean up work files before and after build '
                   '(default)'))

        argopt.add_argument(
            '--colors', action='store_true', dest='colors',
            help=_('use colors in output (default)'))
        argopt.add_argument(
            '-C', '--nocolors', action='store_true', dest='nocolors',
            help=_('don\'t use colors in output'))

        argopt.add_argument(
            '--debug', action='store_true', dest='debug',
            help=_('display debug messages'))
        argopt.add_argument(
            '--nodebug', action='store_true', dest='nodebug',
            help=_('don\'t display debug messages (default)'))

        argopt.add_argument(
            '--depcheck', action='store_true', dest='depcheck',
            help=_('check dependencies (default)'))
        argopt.add_argument(
            '-d', '--nodepcheck', action='store_true', dest='nodepcheck',
            help=_('don\'t check dependencies (may break makepkg)'))

        argopt.add_argument(
            '-D', '--vcsupgrade', action='store_true', dest='vcsupgrade',
            help=_('upgrade all the VCS/date-versioned packages'))
        argopt.add_argument(
            '--novcsupgrade', action='store_true', dest='novcsupgrade',
            help=_('don\'t upgrade all the VCS/date-versioned packages '
                   '(default)'))

        argopt.add_argument(
            '--validation', action='store_true', dest='validation',
            help=_('check if packages were installed after build (default)'))
        argopt.add_argument(
            '-v', '--novalidation', action='store_true', dest='novalidation',
            help=_('don\'t check if packages were installed after build'))

        argopt.add_argument(
            '--install', action='store_true', dest='pkginst',
            help=_('install packages after building (default)'))
        argopt.add_argument(
            '-w', '--buildonly', action='store_true', dest='nopkginst',
            help=_('don\'t install packages after building'))

        argopt.add_argument(
            '--pgpcheck', action='store_true', dest='pgpcheck',
            help=_('verify source files with PGP signatures (default)'))
        argopt.add_argument(
            '--skippgpcheck', action='store_true', dest='nopgpcheck',
            help=_('do not verify source files with PGP signatures'))

        argopt.add_argument(
            '--confirm', action='store_true', dest='confirm',
            help=_('ask for confirmation (default)'))
        argopt.add_argument(
            '--noconfirm', action='store_true', dest='noconfirm',
            help=_('do not ask for any confirmation'))

        argopt.add_argument(
            '--shallow', action='store_true', dest='shallowclone',
            help=_('use shallow git clones (default)'))
        argopt.add_argument(
            '--deep', action='store_true', dest='deepclone',
            help=_('use deep git clones'))

        argopt.add_argument(
            '--ignore', action='append', dest='ignorelist', metavar='PACKAGE',
            help=_('ignore a package upgrade (can be used more than once)'))

        argopt.add_argument(
            '-y', '--refresh', action='store_true', dest='pacupd',
            help=_('(dummy)'))

        argneg = parser.add_argument_group(_('configuration overrides'))
        argneg.add_argument(
            '--notmp', action='store_true', dest='nopac',
            help=_('don\'t build in /tmp'))
        argneg.add_argument(
            '--build', action='store_true', dest='nofetch',
            help=_('build (instead of fetching)'))

        if source != 'AUTO':
            args = parser.parse_args(source)
        else:
            args = parser.parse_args()

        DS.pacman = DS.get_setting('-S', 'operations', 'tmpbuild',
                                   args.pac, args.nopac)
        DS.fetch = DS.get_setting('-F', 'operations', 'fetch',
                                  args.fetch, args.nofetch)
        DS.clean = DS.get_setting('--clean', 'options', 'clean',
                                  args.clean, args.noclean)
        DS.depcheck = DS.get_setting('--depcheck', 'options', 'depcheck',
                                     args.depcheck, args.nodepcheck)
        DS.vcsupgrade = DS.get_setting('--vcsupgrade', 'options', 'vcsupgrade',
                                       args.vcsupgrade, args.novcsupgrade)
        DS.validation = DS.get_setting('--validation', 'options', 'validation',
                                       args.validation, args.novalidation)
        DS.pkginst = DS.get_setting('--install', 'options', 'install',
                                    args.pkginst, args.nopkginst)
        DS.pgpcheck = DS.get_setting('--pgpcheck', 'options', 'pgpcheck',
                                     args.pgpcheck, args.nopgpcheck)
        DS.confirm = DS.get_setting('--confirm', 'options', 'confirm',
                                    args.confirm, args.noconfirm)
        DS.deepclone = DS.get_setting('--deep', 'options', 'deepclone',
                                      args.deepclone, args.shallowclone)
        DS.colors_status = DS.get_setting('--colors', 'options', 'colors',
                                          args.colors, args.nocolors)
        pkgnames = args.pkgnames

        if DS.get_setting('--debug', 'options', 'debug',
                          args.debug, args.nodebug):
            DS.debugmode(nochange=True)
            DS.log.info('*** PKGBUILDer v{0}'.format(__version__))
            DS.log.debug('*** debug output on.')

        DS.log.info('Arguments parsed.  {0}'.format(args.__dict__))

        if 'VIRTUAL_ENV' in os.environ:
            DS.log.error("virtualenv detected, exiting.")
            DS.fancy_error(_("PKGBUILDer cannot work in a virtualenv, "
                             "exiting."))
            exit(83)

        if not DS.colors_status:
            DS.colorsoff()
            DS.log.debug('Colors turned off.')

        if args.info:
            DS.log.debug('Showing info...')

            pkgs = pkgbuilder.utils.info(pkgnames)
            foundnames = [i.name for i in pkgs]
            if pkgs:
                pkgbuilder.utils.print_package_info(pkgs)
                qs = 0
            elif not pkgnames:
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
                search_string = ' '.join(pkgnames)
                if len(search_string) < 2:
                    # this would be too many entries, but this is an actual API
                    # limitation and not an idea of yours truly.
                    DS.fancy_error(_('Search query too short'))
                    DS.fancy_msg(_('Searching for exact match...'))
                    search = pkgbuilder.utils.info([search_string])
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
                    search = pkgbuilder.utils.search(search_string)

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
                tx.delete = DS.clean
                tx.run()
                if quit and tx.exitcode != 0:
                    exit(tx.exitcode)
            if quit:
                exit(0)

        user_chdir = DS.config.get('extras', 'chdir').strip()

        if user_chdir:
            DS.log.debug('Changing directory to %s (via config)', user_chdir)
            os.makedirs(user_chdir, exist_ok=True)
            os.chdir(user_chdir)
        elif DS.pacman:
            DS.log.debug('-S passed, building in /tmp/.')
            path = '/tmp/pkgbuilder-{0}'.format(str(DS.uid))
            if not os.path.exists(path):
                os.mkdir(path)
            os.chdir(path)

        if args.upgrade:
            DS.root_crash()
            DS.log.info('Starting upgrade...')
            dodowngrade = args.upgrade > 1
            ignorelist = []
            for i in (args.ignorelist or []):
                # `pacman -Syu --ignore a,b --ignore c` → ignores a, b, c
                ignorelist.extend(i.split(','))
            upnames = pkgbuilder.upgrade.auto_upgrade(
                dodowngrade, DS.vcsupgrade, DS.fetch, ignorelist)
            pkgnames = upnames + pkgnames

        if DS.fetch and pkgnames:
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
                    out = pkgbuilder.build.auto_build(pkgname, DS.depcheck,
                                                      DS.pkginst, pkgnames)
                    if out:
                        toinstall += out[1][0]
                        sigs += out[1][1]
                except PBException as e:
                    DS.fancy_error(str(e))
                    if e.exit:
                        exit(1)
                    else:
                        DS.fancy_error2(_("skipping package {0}").format(
                            pkgname))

            if DS.pkginst:
                # If there is nothing to install, but the user asked to install
                # something, we will exit with the amount of packages that were
                # not installed; this behavior is similar to what transaction
                # validation would do.
                qs = len(tovalidate)
            else:
                # But otherwise (-w, --buildonly), we can just exit with zero.
                qs = 0

            if toinstall:
                tx = pkgbuilder.transaction.Transaction(
                    pkgnames=tovalidate,
                    pkgpaths=toinstall,
                    sigpaths=sigs,
                    asdeps=False,
                    filename=pkgbuilder.transaction.generate_filename(),
                    delete=True)
                tx.run(standalone=False, validate=DS.validation)
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
