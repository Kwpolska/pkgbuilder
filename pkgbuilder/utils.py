#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v3.1.2
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2013, Kwpolska.
# See /LICENSE for licensing information.

"""
    pkgbuilder.utils
    ~~~~~~~~~~~~~~~~

    Common global utilities, used mainly for AUR data access.

    :Copyright: © 2011-2013, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, _
from .aur import AUR
from .package import AURPackage
from pkgbuilder.exceptions import SanityError, AURError
import pyalpm
import os
import subprocess
import textwrap

__all__ = ['info', 'search', 'msearch', 'print_package_search',
           'print_package_info']
RPC = AUR()


def info(pkgnames):
    """
    .. versionchanged:: 3.0.0

    Returns info about AUR packages.
    """
    if isinstance(pkgnames, str):
        pkgnames = [pkgnames]

    aur_pkgs = RPC.multiinfo(pkgnames)
    if aur_pkgs['type'] == 'error':
        raise AURError(aur_pkgs['results'])
    else:
        return [AURPackage.from_aurdict(d) for d in aur_pkgs['results']]


def search(pkgname):
    """
    .. versionchanged:: 3.0.0

    Searches for AUR packages."""
    aur_pkgs = RPC.request('search', pkgname)
    if aur_pkgs['type'] == 'error':
        raise AURError(aur_pkgs['results'])
    else:
        return [AURPackage.from_aurdict(d) for d in aur_pkgs['results']]


def msearch(maintainer):
    """
    .. versionadded:: 3.0.0

    Searches for AUR packages maintained by a specified user."""
    aur_pkgs = RPC.request('msearch', maintainer)
    if aur_pkgs['type'] == 'error':
        raise AURError(aur_pkgs['results'])
    else:
        return [AURPackage.from_aurdict(d) for d in aur_pkgs['results']]


def print_package_search(pkg, use_categories=True, cachemode=False, prefix='',
                         prefixp=''):
    """
    .. versionchanged:: 3.0.0

    Outputs/returns a package representation, which is close to the output
    of ``pacman -Ss``.
    """
    size = subprocess.check_output(['stty', 'size'])
    try:
        termwidth = int(size.split()[1])
    except IndexError:
        termwidth = 9001  # Auto-wrap by terminal.  A reference to an old
                          # meme and a cheat, too. Sorry.

    localdb = DS.pyc.get_localdb()
    lpkg = localdb.get_pkg(pkg.name)
    category = ''
    installed = ''
    prefix2 = prefix + '    '
    prefixp2 = prefixp + '    '
    if lpkg is not None:
        if pyalpm.vercmp(pkg.version, lpkg.version) != 0:
            installed = _(' [installed: {0}]').format(lpkg.version)
        else:
            installed = _(' [installed]')
    try:
        if pkg.is_outdated:
            installed = (installed + ' ' + DS.colors['red'] +
                         _('[out of date]') + DS.colors['all_off'])
    except AttributeError:
        pass  # for ABS packages

    if use_categories or pkg.is_abs:
        category = pkg.repo
    else:
        category = 'aur'

    descl = textwrap.wrap(pkg.description, termwidth - len(prefixp2))

    desc = []
    for i in descl:
        desc.append(prefix2 + i)
    desc = '\n'.join(desc)
    if pkg.is_abs:
        base = (prefix + '{0}/{1} {2}{3}\n{4}')
        entry = (base.format(category, pkg.name, pkg.version, installed, desc))
    else:
        base = (prefix + '{0}/{1} {2} ({3} {4}){5}\n{6}')
        entry = (base.format(category, pkg.name, pkg.version, pkg.votes,
                             _('votes'), installed, desc))

    if cachemode:
        return entry
    else:
        print(entry)


def print_package_info(pkgs, cachemode=False):
    """
    .. versionchanged:: 3.0.0

    Outputs/returns a package representation, which is close to the output
    of ``pacman -Si``.
    """
    if pkgs == []:
        raise SanityError(_('Didn’t pass any packages.'))
    else:
        for i in pkgs:
            if not isinstance(i, AURPackage):
                raise SanityError(_('Trying to use utils.print_package_info '
                                    'with an ABS package'),
                                  source='utils.print_package_info')
        loct = os.getenv('LC_TIME')
        loc = os.getenv('LC_ALL')

        if loc == '':
            loc = os.getenv('LANG')

        if loc == '':
            loc = 'en_US.UTF-8'

        if loct == '':
            loct = loc

        fmt = '%Y-%m-%dT%H:%M:%SZ'

        # TRANSLATORS: space it properly.  “yes/no” below are
        # for “out of date”.

        t = _("""Repository     : aur
Category       : {cat}
Name           : {nme}
Version        : {ver}
URL            : {url}
Licenses       : {lic}
Votes          : {cmv}
Out of Date    : {ood}
Maintainer     : {mnt}
First Submitted: {fsb}
Last Updated   : {upd}
Description    : {dsc}
""")

        to = []
        for pkg in pkgs:
            upd = pkg.modified.strftime(fmt)
            fsb = pkg.added.strftime(fmt)

            if pkg.is_outdated:
                ood = DS.colors['red'] + _('yes') + DS.colors['all_off']
            else:
                ood = _('no')
            to.append(t.format(cat=pkg.repo, nme=pkg.name, url=pkg.url,
                               ver=pkg.version, lic=', '.join(pkg.licenses),
                               cmv=pkg.votes, ood=ood, mnt=pkg.human, upd=upd,
                               fsb=fsb, dsc=pkg.description))

    if cachemode:
        return '\n'.join(to)
    else:
        print('\n'.join(to))
