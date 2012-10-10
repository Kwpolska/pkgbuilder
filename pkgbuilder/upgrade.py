#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.1.5.2
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2012, Kwpolska.
# See /LICENSE for licensing information.

# Names convention: pkg = a package object, pkgname = a package name.

"""
    pkgbuilder.Upgrade
    ~~~~~~~~~~~~~~~~~~
    Tools for performing upgrades of AUR packages.

    :Copyright: © 2011-2012, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, _, PBError
from .aur import AUR
from .build import Build
import pyalpm
import pycman
import datetime


### Upgrade     upgrade AUR packages        ###
class Upgrade:
    """Tools for performing upgrades of AUR packages."""

    aur = AUR()
    build = Build()
    H = pycman.config.init_with_config('/etc/pacman.conf')
    localdb = H.get_localdb()

    def gather_foreign_pkgs(self):
        """Gathers a list of all foreign packages."""
        # Based on paconky.py.
        installed = [p for p in self.localdb.pkgcache]
        repo = []
        aur = []
        syncdbs = self.H.get_syncdbs()
        for sdb in syncdbs:
            for pkg in installed:
                if sdb.get_pkg(pkg.name):
                    repo.append(pkg)

        aur = set(set(installed) - set(repo))
        # Return foreign packages.
        return dict([(p.name, p) for p in aur])

    def list_upgradable(self, pkglist, vcsup=False):
        """Compares package versions and returns upgradable ones."""
        aurlist = self.aur.multiinfo(pkglist, DS.protocol)['results']
        # It's THAT easy.  Oh, and by the way: it is much, MUCH faster
        # than others.  It makes ONE multiinfo request rather than
        # len(installed_packages) info requests.
        upgradable = []
        downgradable = []

        for i in aurlist:
            pkg = self.localdb.get_pkg(i['Name'])
            if pkg is not None:
                vc = pyalpm.vercmp(i['Version'], pkg.version)
                if vc > 0:
                    upgradable.append([i['Name'], pkg.version, i['Version']])
                elif vc < 0:
                    # If the package version is a date or the name ends in
                    # -{git,hg,bzr,svn,cvs,darcs}, do not mark it as
                    # downgradable.  BTW: the above is yours truly’s list of
                    # VCS preference, if you added a gap between git and hg and
                    # then HUGE gaps between everything else.

                    try:
                        # For epoch packages.  Also, cheating here.
                        v = i['Version'].split(':')[1]
                    except IndexError:
                        v = i['Version']

                    try:
                        d = datetime.datetime.strptime(v.split('-')[0],
                                                       '%Y%m%d')
                        datever = True
                    except:
                        datever = False

                    dt = datetime.date.today().strftime('%Y%m%d')

                    if (i['Name'].endswith(('git', 'hg', 'bzr', 'svn', 'cvs',
                                            'darcs'))):
                        if vcsup:
                            upgradable.append([i['Name'], pkg.version, dt])
                        else:
                            DS.log.warning('{} is -[vcs], ignored for '
                                           'downgrade.'.format(i['Name']))
                    elif datever:
                        if vcsup:
                            upgradable.append([i['Name'], pkg.version, dt])
                        else:
                            DS.log.warning('{} version is a date, ignored '
                                           'for downgrade.'.format(i['Name']))
                    else:
                        downgradable.append([i['Name'], pkg.version,
                                             i['Version']])
        return [upgradable, downgradable]

    def auto_upgrade(self, downgrade=False, vcsup=False):
        """Upgrades packages.  Simillar to Build.auto_build()."""
        DS.log.info('Ran auto_upgrade.')
        if DS.pacman:
            print(':: ' + _('Synchronizing package databases...'))
        else:
            DS.fancy_msg(_('Synchronizing package databases...'))

        foreign = self.gather_foreign_pkgs()
        gradable = self.list_upgradable(foreign.keys(), vcsup)
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
                    print(_('{}: local ({}) is newer than aur ({})').format(
                          i[0], i[1], i[2]))
                else:
                    DS.fancy_warning(_('{}: local ({}) is newer than aur '
                                     '({})').format(i[0], i[1], i[2]))

            if downgrade:
                upglen = upglen + downlen
                upgradable = upgradable + downgradable

        if upglen == 0:
            if DS.pacman:
                print(' ' + _('there is nothing to do'))
            else:
                DS.fancy_msg2(_('there is nothing to do'))

            return 0

        upgnames = [i[0] for i in upgradable]
        upgstrings = [i[0] + '-' + i[2] for i in upgradable]

        if upglen > 0:
            if DS.pacman:
                print()
                print(_('Targets ({}): ').format(upglen), end='')
                print('  '.join(upgstrings))
                print()
                query = _('Proceed with installation? [Y/n] ')
            else:
                DS.fancy_msg(_('Targets ({}): ').format(upglen))
                DS.fancy_msg2('  '.join(upgstrings))
                query = (DS.colors['green'] + '==>' + DS.colors['all_off'] +
                         DS.colors['bold'] + ' ' + _('Proceed with '
                         'installation? [Y/n] ') + DS.colors['all_off'])

            yesno = input(query)
            if yesno.lower().startswith('n'):
                return 0

            toinstall = []

            if DS.uid == 0:
                DS.log.warning('Running as root! (UID={})'.format(DS.uid))
                DS.fancy_warning(_('Running PKGBUILDer as root can break '
                                   'your system!'))
            for pkgname in upgnames:
                DS.log.info('Building {}'.format(pkgname))
                out = self.build.auto_build(pkgname, DS.depcheck,
                                            DS.pkginst)
                if out:
                    toinstall += out

            if toinstall:
                self.build.install(toinstall)

            if DS.validate:
                self.build.validate(upgnames)
