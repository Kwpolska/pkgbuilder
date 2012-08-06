#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.1.3.1
# An AUR helper/library.
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

from . import DS, T, _, PBError
from .aur import AUR
from .build import Build
import pyalpm
import pycman


### Upgrade     upgrade AUR packages        ###
class Upgrade:
    """Tools for performing upgrades of AUR packages."""
    def __init__(self):
        """Upgrade init."""
        self.aur = AUR()
        self.build = Build()
        self.H = pycman.config.init_with_config('/etc/pacman.conf')
        self.localdb = self.H.get_localdb()

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

    def list_upgradeable(self, pkglist):
        """Compares package versions and returns upgradeable ones.

:Arguments: a package list.
:Input:
    a list of packages to be compared.

    suggestion: self.gather_foreign_pkgs().keys()
:Output: none.
:Returns: upgradeable packages.
:Exceptions: none.
:Message codes: none."""

        aurlist = self.aur.multiinfo(pkglist, DS.protocol)['results']
        # It's THAT easy.  Oh, and by the way: it is much, MUCH faster
        # than others.  It makes ONE multiinfo request rather than
        # len(installed_packages) info requests.
        upgradeable = []

        for i in aurlist:
            pkg = self.localdb.get_pkg(i['Name'])
            if pyalpm.vercmp(i['Version'], pkg.version) > 0:
                upgradeable.append(i['Name'])
        return upgradeable

    def auto_upgrade(self):
        """Upgrades packages.  Simillar to Build.auto_build().

:Arguments: none.
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
        upgradeable = self.list_upgradeable(foreign.keys())
        upglen = len(upgradeable)
        if upglen > 0:
            if DS.pacman:
                print(_('Targets ({0}): ').format(upglen), end='')
            else:
                DS.fancy_msg(_('{0} upgradeable packages found:').format(
                    upglen))

        if upglen == 0:
            if DS.pacman:
                print(_(' there is nothing to do'))
            else:
                DS.fancy_msg2(_('there is nothing to do'))

            return 0
        if DS.pacman:
            print('  '.join(upgradeable))
            query = _('Proceed with installation? [Y/n] ')
        else:
            DS.fancy_msg2('  '.join(upgradeable))
            query = (DS.colors['green'] + '==>' + DS.colors['all_off'] +
                     DS.colors['bold'] + ' ' + _('Proceed with \
installation? [Y/n] ') + DS.colors['all_off'])

        yesno = input(query)
        yesno = yesno + ' '  # cheating...
        if yesno[0] == 'n' or yesno[0] == 'N':
            return 0
        for pkgname in upgradeable:
            DS.log.info('Building {0}'.format(pkgname))
            self.build.auto_build(pkgname, DS.validate, DS.depcheck,
                                  DS.mkpginst)
