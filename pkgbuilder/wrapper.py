# -*- encoding: utf-8 -*-
# PBWrapper v0.5.0
# PKGBUILDer v4.3.1
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2021, Chris Warrick.
# See /LICENSE for licensing information.

"""
A wrapper for pacman and PKGBUILDer, also known as PBWrapper or pb.

:Copyright: © 2011-2021, Chris Warrick.
:License: BSD (see /LICENSE).
"""

from . import DS, _, __version__
from .__main__ import main as pbmain
from .exceptions import SanityError
import pkgbuilder.utils
import re
import logging
import subprocess
import pyalpm
import argparse
import sys
import os

__all__ = ('main', 'wrapper')
__wrapperversion__ = '0.5.6'


def main():
    """Run the PBWrapper main function."""
    try:
        pkgbuilder.wrapper.wrapper()
    except KeyboardInterrupt:
        print(pkgbuilder.DS.wrapperinttext + '\n')
        exit(130)


def show_help():
    """Show help for PBWrapper."""
    pacdoc = subprocess.check_output('pacman --help || true',
                                     shell=True).decode('utf-8')
    pacdoc = '\n'.join(pacdoc.split('\n\n')[0].split('\n')[1:])
    pacdoc = pacdoc.replace('pacman', 'pb')

    # TRANSLATORS: see pacman’s localizations
    print(_("""usage:  {0} <operation> [...]

PBWrapper, a wrapper for pacman and PKGBUILDer.

{1}

Pacman and PKGBUILDer syntaxes apply.  Consult their manpages/help
commands for more details.

Additional options:
  -L, --unlock         unlock the pacman database""").format(
          os.path.basename(sys.argv[0]), pacdoc))


def show_version():
    """Show PBWrapper, PKGBUILDer, pacman and pyalpm versions."""
    localdb = DS.pyc.get_localdb()
    pacpkg = localdb.get_pkg('pacman')

    print("""PBWrapper   v{0}
PKGBUILDer  v{1}
pacman      v{2}
pyalpm      v{3}""".format(__wrapperversion__, __version__,
                           pacpkg.version.split('-', 1)[0],
                           pyalpm.version()))


def wrapper(source='AUTO'):
    """A wrapper for pacman and PKGBUILDer."""
    # Because I need to work with -S and nothing else, I am going to use
    # regular expressions on the argument list.  Sorry.
    if source == 'AUTO':
        argst = sys.argv[1:]
    else:
        argst = source

    log = logging.getLogger('pbwrapper')
    if '--debug' in argst:
        DS.debugmode()
    elif '--debugpb' in argst:
        DS.debugmode()
        argst.remove("--debugpb")
        sys.argv.remove("--debugpb")

    log.info('*** PBwrapper v{0} (PKGBUILDer '
             '{1})'.format(__wrapperversion__, __version__))

    if (('-L' in argst) or ('--unlock' in argst) or (re.search('-[a-zA-Z]*L',
                                                               ' '.join(argst))
                                                     is not None)):
        try:
            os.remove('/var/lib/pacman/db.lck')
            exit(0)
        except OSError as e:
            DS.fancy_error('[-L --unlock] ' + e.strerror)
            exit(1)

    if (('-S' in argst) or ('--sync' in argst) or (re.search('-[a-zA-Z]*S',
                                                             ' '.join(argst))
                                                   is not None)):
        # The user has requested -S.
        # -l/--list is in not in *a because it takes over the whole package
        # list, and that is a workaround.
        log.debug('Got -S, preparing to parse arguments...')
        pacmanshort = ['f', 'g', 'l', 'p', 'q']
        pacmanlong = ['asdeps', 'asexplicit', 'dbonly', 'downloadonly',
                      'groups', 'list', 'needed', 'nodeps',
                      'noprogressbar', 'noscriptlet', 'print', 'quiet',
                      'verbose', 'files', 'disable-download-timeout']
        pacmanshorta = ['b', 'r']
        pacmanlonga = ['arch', 'cachedir', 'config', 'dbpath', 'gpgdir',
                       'hookdir', 'ignoregroup', 'logfile', 'overwrite',
                       'print-format', 'root', 'assume-installed']

        pbshort = ['D', 'C', 'G']
        pblong = ['fetch', 'get', 'userfetch', 'vcsupgrade', 'novcsupgrade', 'colors',
                  'nocolors', 'depcheck', 'nodepcheck', 'validation',
                  'novalidation', 'install', 'buildonly', 'pgpcheck',
                  'skippgpcheck', 'deep', 'shallow', 'noclean', 'nodebug',
                  'noedit-pkgbuild', 'edit-pkgbuild']

        commonshort = ['S', 'd', 'i', 's', 'v', 'w']
        commonlong = ['debug', 'info', 'search', 'sync', 'confirm',
                      'noconfirm']
        commonlongl = ['ignore']
        commonshortc = ['c', 'y', 'u']
        commonlongc = ['clean', 'refresh', 'sysupgrade']

        ignoredshort = ['L']
        ignoredlong = ['unlock']

        allpacman = pacmanshort + pacmanlong + pacmanshorta + pacmanlonga
        allpb = pbshort + pblong  # + pbshorta + pblonga
        allcommon = (commonshort + commonlong + commonlongl + commonshortc +
                     commonlongc)

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
                            default=False, dest='version')

        for i in allshort + ignoredshort:
            parser.add_argument('-' + i, action='store_true', default=False,
                                dest=i)

        for i in alllong + ignoredlong:
            parser.add_argument('--' + i, action='store_true', default=False,
                                dest=i)

        for i in allshortc:
            parser.add_argument('-' + i, action='count', default=0, dest=i)

        for i in alllongc:
            parser.add_argument('--' + i, action='count', default=0, dest=i)

        for i in pacmanshorta:
            parser.add_argument('-' + i, action='store', nargs=1,
                                default='NIL', dest=i)

        for i in pacmanlonga:
            parser.add_argument('--' + i, action='store', nargs=1,
                                default='NIL', dest=i)

        for i in commonlongl:
            parser.add_argument('--' + i, action='append', dest=i)

        parser.add_argument('pkgnames', action='store', nargs='*')

        # Starting actual work.

        if source != 'AUTO':
            args = parser.parse_args(source)
        else:
            args = parser.parse_args()

        log.debug('Arguments parsed.  {0}'.format(args.__dict__))

        try:
            pkgnames = args.pkgnames
        except AttributeError:
            pkgnames = []

        execargs = []
        pacargs = []
        pbargs = []

        for k, v in args.__dict__.items():
            if v is not False:
                # == This argument has been provided.
                if k in allcountable:
                    # == This is a countable argument.
                    if k in allshortc:
                        for _i in range(v):
                            execargs.append('-' + k)
                    elif k in alllongc:
                        for _i in range(v):
                            execargs.append('--' + k)
                elif v:
                    # == This argument doesn't have a value.
                    if k in allshort:
                        execargs.append('-' + k)
                    elif k in alllong:
                        execargs.append('--' + k)

        for i in execargs:
            if i[1:] in allshort + allshortc:
                s = i[1:]
            elif i[2:] in alllong + alllongc:
                s = i[2:]
            else:
                raise SanityError('argparse broke', 'argparse')

            if s in allcommon:
                pacargs.append(i)
                pbargs.append(i)

            if s in allpacman:
                pacargs.append(i)
            elif s in allpb:
                pbargs.append(i)

        for k, v in args.__dict__.items():
            if v is not False and v != 'NIL':
                # == This argument can take values and has one.
                if k in pacmanshorta:
                    pacargs.append('-' + k)
                    pacargs.extend(v)
                elif k in pacmanlonga:
                    pacargs.append('--' + k)
                    pacargs.extend(v)
                elif k in commonlongl:
                    for vi in v:
                        pacargs.append('--' + k)
                        pacargs.append(vi)
                        pbargs.append('--' + k)
                        pbargs.append(vi)

        log.debug('Preparing to run pacman and/or PKGBUILDer...')

        if args.search or args.s:
            log.debug('Got -s.')
            if args.pkgnames:
                log.info('Running pacman.')
                DS.run_command([DS.paccommand] + pacargs + pkgnames)
                log.info('Running pkgbuilder (pkgbuilder.__main__.main()).')
                pbmain(pbargs + pkgnames)
            else:
                log.info('Nothing to do — args.pkgnames is empty.')

            exit()
        elif args.l or args.list:
            log.debug('Got -l.')
            log.info('Running pacman.')
            DS.run_command([DS.paccommand] + pacargs + pkgnames)
            exit()
        elif args.u or args.sysupgrade:
            log.debug('Got -u.')
            log.info('Running pacman.')
            DS.sudo([DS.paccommand] + pacargs)
            log.info('Running pkgbuilder (pkgbuilder.__main__.main()).')
            pbmain(pbargs, quit=False)
        elif args.y or args.refresh:
            log.debug('Got -y.')
            log.info('Running pacman.')
            DS.sudo([DS.paccommand] + pacargs)
        elif args.help:
            show_help()
            exit()
        elif args.version:
            show_version()
            exit()

        log.debug('Generating AUR packages list...')
        pbpkgnames = []
        info = pkgbuilder.utils.info(pkgnames)

        names = [i.name for i in info]
        pbpkgnames = [n for n in pkgnames if n in names]
        pacmanpkgnames = [i for i in pkgnames if i not in pbpkgnames]

        droppable = ['-u', '-y', '--sysupgrade', '--refresh']

        pacargs = [i for i in pacargs if i not in droppable]
        pbargs = [i for i in pbargs if i not in droppable]
        log.debug('Generated.')

        if pacmanpkgnames != []:
            log.info('Running pacman.')
            DS.sudo([DS.paccommand] + pacargs + pacmanpkgnames)
        else:
            log.info('No repo packages in the list.')

        if pbpkgnames != []:
            log.info('Running pkgbuilder (pkgbuilder.main.main()).')
            pbmain(pbargs + pbpkgnames)
        else:
            log.info('No AUR packages in the list.')

        sanitycheck = pacmanpkgnames + pbpkgnames
        if len(sanitycheck) != len(pkgnames):
            log.info('Running pacman due to failed sanity check.')
            sanityargs = [item for item in pkgnames if (item not in
                          sanitycheck)]
            DS.sudo([DS.paccommand] + pacargs + sanityargs)
    elif (('-G' in argst) or ('--get' in argst) or ('--fetch' in argst) or
          ('--userfetch' in argst) or ('-X' in argst) or ('--runtx' in argst) or
          (re.search('-[a-zA-Z]*G', ' '.join(argst)) is not None) or
          (re.search('-[a-zA-Z]*X', ' '.join(argst)) is not None)):
        # pkgbuilder -G, --get, --fetch / --userfetch / -X, --runtx.
        log.info("Running pkgbuilder command")
        pbmain(argst)
    elif ('-h' in argst) or ('--help' in argst):
        show_help()
    elif ('-V' in argst) or ('--version' in argst):
        show_version()
    elif 'UTshibboleet' in argst:
        if argst[0] == 'unittests' and argst[1] == 'UTshibboleet':
            # http://xkcd.com/806/
            pass
        else:
            print('Please don’t use the reserved UTshibboleet argument.')

    elif (('-Q' in argst) or ('--query' in argst) or (re.search(
            '-[a-zA-Z]*Q', ''.join(argst)) is not None) or
            ('-F' in argst) or ('--files' in argst) or (re.search(
            '-[a-zA-Z]*F', ''.join(argst)) is not None)):
        log.info("Running rootless pacman command")
        DS.run_command([DS.paccommand] + argst)
    else:
        log.info("Running root pacman command")
        DS.sudo([DS.paccommand] + argst)
