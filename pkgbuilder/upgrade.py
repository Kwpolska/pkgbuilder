# -*- encoding: utf-8 -*-
# PKGBUILDer v4.2.18
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2018, Chris Warrick.
# See /LICENSE for licensing information.

"""
Tools for performing upgrades of AUR packages.

:Copyright: © 2011-2018, Chris Warrick.
:License: BSD (see /LICENSE).
"""

from . import DS, _
import pkgbuilder.build
import pkgbuilder.ui
import pkgbuilder.utils
import pyalpm
import datetime

__all__ = ('gather_foreign_pkgs', 'list_upgradable', 'auto_upgrade')


def gather_foreign_pkgs():
    """Gather a list of all foreign packages."""
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


def list_upgradable(pkglist, vcsup=False, aurcache=None, ignorelist=None):
    """Compare package versions and returns upgradable ones.

    .. versionchanged:: 4.2.9
    """
    localdb = DS.pyc.get_localdb()
    if ignorelist is None:
        ignorelist = []
    if aurcache:
        aurlist = aurcache
    else:
        aurlist = pkgbuilder.utils.info(pkglist)
        # It’s THAT easy.  Oh, and by the way: it is much, MUCH faster than
        # others.  It makes only a handful of multiinfo requests (1-2 on most
        # systems) rather than len(installed_packages) info requests.

    upgradable = []
    downgradable = []
    ignored = []

    for rpkg in aurlist:
        lpkg = localdb.get_pkg(rpkg.name)
        if lpkg is not None:
            vc = pyalpm.vercmp(rpkg.version, lpkg.version)
            if vc > 0 and rpkg.name not in ignorelist:
                upgradable.append([rpkg.name, lpkg.version, rpkg.version])
            elif vc > 0 and rpkg.name in ignorelist:
                DS.log.warning("{0} ignored for upgrade.".format(rpkg.name))
                ignored.append([rpkg.name, lpkg.version, rpkg.version])
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
    return [upgradable, downgradable, ignored]


def auto_upgrade(downgrade=False, vcsup=False, fetchonly=False,
                 ignorelist=None):
    """
    Human friendly upgrade question and output.

    Returns packages — should be passed over to builder functions.
    """
    DS.log.info('Ran auto_upgrade.')
    print(':: ' + _('Synchronizing package databases...'))

    foreign = gather_foreign_pkgs()
    upgradable, downgradable, ignored = list_upgradable(
        foreign.keys(), vcsup, ignorelist=ignorelist)

    print(':: ' + _('Starting full system upgrade...'))

    for i in ignored:
        print(_("warning: {0}: ignoring package upgrade ({1} => {2})").format(
            *i))

    if downgradable:
        for i in downgradable:
            if downgrade:
                msg = _('warning: {0}: downgrading from version {1} '
                        'to version {2}').format(*i)
            else:
                msg = _('warning: {0}: local ({1}) is newer than aur '
                        '({2})').format(*i)
            print(msg)

        if downgrade:
            upgradable = upgradable + downgradable

    if not upgradable:
        print(' ' + _('there is nothing to do'))

        return []

    upgnames = [i[0] for i in upgradable]
    upgstrings = [i[0] + '-' + i[2] for i in upgradable]

    verbosepkglists = DS.config.getboolean('options', 'verbosepkglists')

    if upgradable:
        targetstring = _('Targets ({0}):').format(len(upgradable)) + ' '

        termwidth = pkgbuilder.ui.get_termwidth()

        if termwidth is None and verbosepkglists:
            # Pacman doesn’t allow tables if the terminal is too small.
            # And since we don’t know the size, better safe than sorry.
            verbosepkglists = False
            DS.log.warning('VerbosePkgLists disabled, cannot '
                           'determine terminal width')

        termwidth = termwidth or 9001

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
            print(pkgbuilder.ui.hanging_indent(
                '  '.join(upgstrings), targetstring, termwidth, True))

        print()
        if fetchonly:
            query = ':: ' + _('Fetch the packages? [Y/n] ')
        else:
            query = ':: ' + _('Proceed with installation? [Y/n] ')

        if DS.confirm:
            yesno = input(query)

            if yesno.lower().strip().startswith('y') or yesno.strip() == '':
                return upgnames
            else:
                return []
        else:
            # Print the query and then return immediately, pacman does that too
            print(query)
            return upgnames
