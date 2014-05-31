#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v3.3.1
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2014, Kwpolska.
# See /LICENSE for licensing information.

"""
    pkgbuilder.upgrade
    ~~~~~~~~~~~~~~~~~~

    Tools for performing upgrades of AUR packages.

    :Copyright: © 2011-2014, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, _
from pkgbuilder.exceptions import SanityError
import pkgbuilder.build
import pkgbuilder.utils
import pyalpm
import datetime
import subprocess
import textwrap
import sys

__all__ = ['gather_foreign_pkgs', 'list_upgradable', 'auto_upgrade']


def gather_foreign_pkgs():
    """Gathers a list of all foreign packages."""
    localdb = DS.pyc.get_localdb()
    # Based on paconky.py.
    installed = [p for p in localdb.pkgcache]
    repo = []
    aur = []
    syncdbs = DS.pyc.get_syncdbs()
    for sdb in syncdbs:
        for ipkg in installed:
            if sdb.get_pkg(ipkg.name):
                repo.append(ipkg)

    aur = set(set(installed) - set(repo))
    # Return foreign packages.
    return dict([(p.name, p) for p in aur])


def list_upgradable(pkglist, vcsup=False, aurcache=None):
    """Compares package versions and returns upgradable ones."""
    localdb = DS.pyc.get_localdb()
    if aurcache:
        aurlist = aurcache
    else:
        aurlist = pkgbuilder.utils.info(pkglist)
        # It’s THAT easy.  Oh, and by the way: it is much, MUCH faster
        # than others.  It makes ONE multiinfo request rather than
        # len(installed_packages) info requests.

    upgradable = []
    downgradable = []

    for rpkg in aurlist:
        lpkg = localdb.get_pkg(rpkg.name)
        if lpkg is not None:
            vc = pyalpm.vercmp(rpkg.version, lpkg.version)
            if vc > 0:
                upgradable.append([rpkg.name, lpkg.version, rpkg.version])
            elif vc < 0:
                # If the package version is a date or the name ends in
                # -{git,hg,bzr,svn,cvs,darcs}, do not mark it as downgradable.
                # BTW: the above is yours truly’s list of VCS preference, if
                # you added big a gap between git and hg and then HUGE gaps
                # between everything else.

                try:
                    # For epoch packages.  Also, cheating here.
                    v = rpkg.version.split(':')[1]
                except IndexError:
                    v = rpkg.version

                try:
                    datetime.datetime.strptime(v.split('-')[0], '%Y%m%d')
                    datever = True
                except:
                    datever = False

                dt = datetime.date.today().strftime('%Y%m%d-1')

                if (rpkg.name.endswith(('git', 'hg', 'bzr', 'svn', 'cvs',
                                        'darcs'))):
                    if vcsup:
                        upgradable.append([rpkg.name, lpkg.version, dt])
                    else:
                        DS.log.warning('{0} is -[vcs], ignored for '
                                       'downgrade.'.format(rpkg.name))
                elif datever:
                    if vcsup:
                        upgradable.append([rpkg.name, lpkg.version, dt])
                    else:
                        DS.log.warning('{0} version is a date, ignored '
                                       'for downgrade.'.format(rpkg.name))
                else:
                    downgradable.append([rpkg.name, lpkg.version,
                                         rpkg.version])
    return [upgradable, downgradable]


def auto_upgrade(downgrade=False, vcsup=False):
    """
    Human friendly upgrade question and output.

    Returns packages — should be passed over to builder functions.
    """
    DS.log.info('Ran auto_upgrade.')
    if DS.pacman:
        print(':: ' + _('Synchronizing package databases...'))
    else:
        DS.fancy_msg(_('Synchronizing package databases...'))

    foreign = gather_foreign_pkgs()
    gradable = list_upgradable(foreign.keys(), vcsup)
    upgradable = gradable[0]
    downgradable = gradable[1]
    upglen = len(upgradable)
    downlen = len(downgradable)

    if DS.pacman:
        print(':: ' + _('Starting full system upgrade...'))
    else:
        DS.fancy_msg(_('Starting full system upgrade...'))

    if downlen > 0:
        for i in downgradable:
            if DS.pacman:
                if downgrade:
                    msg = _('warning: {0}: downgrading from version {1} '
                            'to version {2}').format(*i)
                else:
                    msg = _('warning: {0}: local ({1}) is newer than aur '
                            '({2})').format(*i)
                print(msg)
            else:
                if downgrade:
                    msg = _('{0}: downgrading from version {1} '
                            'to version {2}').format(*i)
                else:
                    msg = _('{0}: local ({1}) is newer than aur '
                            '({2})').format(*i)
                DS.fancy_warning(msg)

        if downgrade:
            upglen = upglen + downlen
            upgradable = upgradable + downgradable

    if upglen == 0:
        if DS.pacman:
            print(' ' + _('there is nothing to do'))
        else:
            DS.fancy_msg2(_('there is nothing to do'))

        return []

    upgnames = [i[0] for i in upgradable]
    upgstrings = [i[0] + '-' + i[2] for i in upgradable]

    verbosepkglists = False
    with open('/etc/pacman.conf') as fh:
        for i in fh.read().split('\n'):
            if i.strip() == 'VerbosePkgLists':
                verbosepkglists = True
                break

    if upglen > 0:
        if 'pkgbuilder' in upgnames or 'pkgbuilder-git' in upgnames:
            if 'pkgbuilder' in upgnames:
                pkgbname = 'pkgbuilder'
            elif 'pkgbuilder-git' in upgnames:
                pkgbname = 'pkgbuilder-git'

            if DS.pacman:
                print(':: ' + _('The following packages should be upgraded '
                                'first:'))
                print('    {0}'.format(pkgbname))
                print(':: ' + _('Do you want to cancel the current operation'))
                query = ':: ' + _('and upgrade these packages now? [Y/n] ')
            else:
                DS.fancy_warning(_('The following packages should be upgraded '
                                   'first:'))
                DS.fancy_msg2(pkgbname)
                query = (DS.colors['green'] + '==>' + DS.colors['all_off'] +
                         DS.colors['bold'] + ' ' +
                         _('Do you want to cancel the current operation and '
                           'upgrade these packages now? [Y/n] ') +
                         DS.colors['all_off'])

            yesno = input(query)

            if yesno.lower().strip().startswith('y') or yesno.strip() == '':
                status = pkgbuilder.build.safeupgrade(pkgbname)
                if status > 0:
                    DS.log.info('safe upgrade failed with {0}'.format(status))
                    sys.exit(status)
                else:
                    # The return causes PKGBUILDer.main() to quit and do
                    # nothing.  The else is unnecessary, as we drop to a
                    # regular upgrade if the luser says “no”.
                    return []

        if DS.pacman:
            targetstring = _('Targets ({0}): ').format(upglen)

            termwidth = pkgbuilder.utils.get_termwidth()
            if termwidth is None:
                termwidth = 9001  # Auto-wrap by terminal.

                if verbosepkglists:
                    # Pacman doesn’t allow tables if the terminal is too small.
                    # And since we don’t know the size, better safe than sorry.
                    verbosepkglists = False
                    DS.log.warning('VerbosePkgLists disabled, cannot '
                                   'determine terminal width')

            if verbosepkglists:
                headers = [_('Name'), _('Old Version'), _('New Version')]
                items = upgradable  # Magical.

                sizes = [len(i) for i in headers]

                for n, ov, nv in items:
                    if len(n) > sizes[0]:
                        sizes[0] = len(n)

                    if len(ov) > sizes[1]:
                        sizes[1] = len(ov)

                    if len(nv) > sizes[2]:
                        sizes[2] = len(nv)

                fstring = ('{{i[0]:<{s[0]}}}  {{i[1]:<{s[1]}}}  '
                           '{{i[2]:<{s[2]}}}').format(s=sizes)

                if len(fstring.format(i=4 * ['n'])) > termwidth:
                    verbosepkglists = False
                    DS.log.warning('VerbosePkgLists disabled, terminal is '
                                   'not wide enough')
                    # string stolen from pacman
                    print(_('warning: insufficient columns available for '
                            'table display'))
                else:
                    print('\n{0}\n'.format(targetstring.strip()))
                    print(fstring.format(i=headers))
                    print()

                    for i in items:
                        print(fstring.format(i=i))

            # Not using else because there is a fallback if the terminal
            # is too small.
            if not verbosepkglists:
                print(pkgbuilder.utils.hanging_indent('  '.join(upgstrings),
                                                      targetstring, termwidth, True))

            print()
            query = ':: ' + _('Proceed with installation? [Y/n] ')
        else:
            DS.fancy_msg(_('Targets ({0}): ').format(upglen))
            DS.fancy_msg2('  '.join(upgstrings))
            query = (DS.colors['green'] + '==>' + DS.colors['all_off'] +
                     DS.colors['bold'] + ' ' +
                     _('Proceed with installation? [Y/n] ') +
                     DS.colors['all_off'])

        yesno = input(query)

        if yesno.lower().strip().startswith('y') or yesno.strip() == '':
            return upgnames
        else:
            return []
