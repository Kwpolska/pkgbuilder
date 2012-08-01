#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.1.3.0
# An AUR helper/library.
# Copyright (C) 2011-2012, Kwpolska.
# See /LICENSE for licensing information.

# Names convention: pkg = a package object, pkgname = a package name.

"""
    pkgbuilder.Utils
    ~~~~~~~~~~~~~~~~
    Common global utilities.  Provides useful data.

    :Copyright: (C) 2011-2012, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, T, _, PBError
from .aur import AUR
import pyalpm
import pycman
import os
import textwrap


### Utils           common global utilities ###
class Utils:
    """Common global utilities.  Provides useful data."""

    def __init__(self):
        """Utils init.

:Arguments: none.
:Input: none.
:Output: none.
:Returns: a Utils object."""
        self.aur = AUR()

    def info(self, pkgname):
        """Returns info about a package.

:Arguments: package name.
:Input: none.
:Output: none.
:Returns: a dict with package data OR None.
:Exceptions: none.
:Message codes: none.
:Former data:
    2.1.2.1 Returns: a dict OR False.

    2.0 Returns: aur_pkgs, list->dict, not null.

    2.0 Behavior: exception and quit when not found."""
        aur_pkgs = self.aur.request('info', pkgname, DS.protocol)
        if aur_pkgs['results'] == 'No results found':
            return None
        else:
            return aur_pkgs['results']

    def search(self, pkgname):
        """Searches for AUR packages.

:Arguments: package name.
:Input: none.
:Output: none.
:Returns: a list of packages.
:Exceptions: none.
:Message codes: none."""
        aur_pkgs = self.aur.request('search', pkgname, DS.protocol)
        if aur_pkgs['results'] == 'No results found':
            return []
        else:
            return aur_pkgs['results']

    def print_package(self, pkg, use_categories=True,
                      cachemode=False, prefix='', prefixp=''):
        """Outputs info about a package.

:Arguments: package name, use categories, cache mode,
    line prefix, line prefix in plain form (no colors etc.)
:Input: none.
:Output: (with cache mode off, otherwise nothing)

    ::
    prefix category/name version (num votes) [installed: version] [out of date]
    prefix     description

:Returns: (with cache mode on, otherwise nothing)

    ::
    prefix category/name version (num votes) [installed: version] [out of date]
    prefix     description

:Exceptions: none.
:Message codes: none.
:Former data:
    2.0 Name: showInfo.
"""
        termwidth = int(os.popen('stty size', 'r').read().split()[1])
        H = pycman.config.init_with_config('/etc/pacman.conf')
        localdb = H.get_localdb()
        lpkg = localdb.get_pkg(pkg['Name'])
        category = ''
        installed = ''
        prefix2 = prefix + '    '
        prefixp2 = prefixp + '    '
        if lpkg is not None:
            if pyalpm.vercmp(pkg['Version'], lpkg.version) != 0:
                installed = _(' [installed: {0}]').format(lpkg.version)
            else:
                installed = _(' [installed]')
        if pkg['OutOfDate'] == '1':
            installed = (installed + ' ' + DS.colors['red'] + _(
                         '[out of date]') + DS.colors['all_off'])
        if use_categories:
            category = DS.categories[int(pkg['CategoryID'])]
        else:
            category = 'aur'

        descl = textwrap.wrap(pkg['Description'], termwidth - len(prefixp2))

        desc = []
        for i in descl:
            desc.append(prefix2 + i)
        desc = '\n'.join(desc)
        base = (prefix + '{0}/{1} {2} ({4} ' + _('votes') +
                '){5}\n' + '{3}')
        entry = (base.format(category, pkg['Name'], pkg['Version'],
                             desc, pkg['NumVotes'], installed))

        if cachemode:
            return entry
        else:
            print(entry)
