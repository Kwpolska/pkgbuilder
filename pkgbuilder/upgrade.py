#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.1.4.3
# An AUR helper (and library) in Python 3.
# Copyright (C) 2011-2012, Kwpolska.
# See /LICENSE for licensing information.

# Names convention: pkg = a package object, pkgname = a package name.

"""
    pkgbuilder.Upgrade
    ~~~~~~~~~~~~~~~~~~
    Tools for performing upgrades of AUR packages.

    :Copyright: (C) 2011-2012, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, _, PBError
from .aur import AUR
from .build import Build
import pyalpm
import pycman


### Upgrade     upgrade AUR packages        ###
class Upgrade:
    """Tools for performing upgrades of AUR packages."""

    aur = AUR()
    build = Build()
    H = pycman.config.init_with_config('/etc/pacman.conf')
    localdb = H.get_localdb()

    def gather_foreign_pkgs(self):
        """Gathers a list of all foreign packages.

:Arguments: none.
:Input: none.
:Output: none.
:Returns: foreign packages.
:Exceptions: none.
:Message codes: none."""

        # Based on paconky.py.
        installed = set(p for p in self.localdb.pkgcache)

        syncdbs = self.H.get_syncdbs()
        for sdb in syncdbs:
            for pkg in list(installed):
                if sdb.get_pkg(pkg.name):
                    installed.remove(pkg)

        foreign = dict([(p.name, p) for p in installed])

        return foreign

    def list_upgradable(self, pkglist):
        """Compares package versions and returns upgradable ones.

:Arguments: a package list.
:Input:
    a list of packages to be compared.

    suggestion: self.gather_foreign_pkgs().keys()
:Output: none.
:Returns: [upgradable packages, downgradable packages].
:Exceptions: none.
:Message codes: none."""

        aurlist = self.aur.multiinfo(pkglist, DS.protocol)['results']
        # It's THAT easy.  Oh, and by the way: it is much, MUCH faster
        # than others.  It makes ONE multiinfo request rather than
        # len(installed_packages) info requests.
        upgradable = []
        downgradable = []

        for i in aurlist:
            pkg = self.localdb.get_pkg(i['Name'])
            vc = pyalpm.vercmp(i['Version'], pkg.version)
            if vc > 0:
                upgradable.append(i['Name'])
            elif vc < 0:
                downgradable.append(i['Name'])
        return [upgradable, downgradable]

    def auto_upgrade(self, downgrade=False):
        """Upgrades packages.  Simillar to Build.auto_build().

:Arguments: allow downgrade.
:Input: user interaction.
:Output: text.
:Returns: 0 or nothing.
:Exceptions: none.
:Message codes: none."""
        DS.log.info('Ran auto_upgrade.')
        if DS.pacman:
            print(':: ' + _('Gathering data about packages...'))
        else:
            DS.fancy_msg(_('Gathering data about packages...'))

        foreign = self.gather_foreign_pkgs()
        gradeable = self.list_upgradable(foreign.keys())
        upgradable = gradeable[0]
        downgradable = gradeable[1]
        upglen = len(upgradable)
        downlen = len(downgradable)
        if downlen > 0:
            if DS.pacman:
                print(_('WARNING:') + ' ' + _('{} downgradable packages'
                      ' found:').format(downlen))
                print('  '.join(downgradable))
                print(_('Run with -D to downgrade, and please check'
                        ' the AUR comments for those packages!'))
            else:
                DS.fancy_warning(_('{} downgradable packages found:'
                                  ).format(downlen))
                DS.fancy_warning2('  '.join(downgradable))

                DS.fancy_msg(_('Run with -D to downgrade, and please check'
                                ' the AUR comments for those packages!'))

            print()

            if downgrade:
                if DS.pacman:
                    print(_('Downgrading: adding to Targets list...'))
                else:
                    DS.fancy_msg(_('Downgrading: adding to Targets list...'))

                upglen = upglen + downlen

                for i in downgradable:
                    upgradable.append(i)

        if upglen == 0 and downlen == 0:
            if DS.pacman:
                print(' ' + _('there is nothing to do'))
            else:
                DS.fancy_msg2(_('there is nothing to do'))

            return 0

        if upglen > 0:
            if DS.pacman:
                print(_('Targets ({}): ').format(upglen), end='')
            else:
                DS.fancy_msg(_('Targets ({}): ').format(upglen))

        if DS.pacman:
            print('  '.join(upgradable))
            query = _('Proceed with installation? [Y/n] ')
        else:
            DS.fancy_msg2('  '.join(upgradable))
            query = (DS.colors['green'] + '==>' + DS.colors['all_off'] +
                     DS.colors['bold'] + ' ' + _('Proceed with '
                     'installation? [Y/n] ') + DS.colors['all_off'])

        yesno = input(query)
        yesno = yesno + ' '  # cheating...
        if yesno[0] == 'n' or yesno[0] == 'N':
            return 0
        for pkgname in upgradable:
            DS.log.info('Building {}'.format(pkgname))
            self.build.auto_build(pkgname, DS.validate, DS.depcheck,
                                  DS.mkpginst)
