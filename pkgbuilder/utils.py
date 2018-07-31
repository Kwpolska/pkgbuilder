# -*- encoding: utf-8 -*-
# PKGBUILDer v4.2.18
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2018, Chris Warrick.
# See /LICENSE for licensing information.

"""
Common global utilities, used mainly for AUR data access.

:Copyright: © 2011-2018, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import os
from . import DS, _
from .aur import AUR
from .package import AURPackage
from .ui import get_termwidth, hanging_indent, mlist
from pkgbuilder.exceptions import SanityError, AURError
import pyalpm
import textwrap

__all__ = ('info', 'search', 'msearch', 'print_package_search',
           'print_package_info',)
RPC = AUR()


def info(pkgnames):
    """Return info about AUR packages.

    .. versionchanged:: 3.0.0

    """
    if isinstance(pkgnames, str):
        pkgnames = [pkgnames]

    aur_pkgs = RPC.multiinfo(pkgnames)
    if aur_pkgs['type'] == 'error':
        raise AURError(aur_pkgs['error'])
    else:
        return [AURPackage.from_aurdict(d) for d in aur_pkgs['results']]


def search(pkgname, search_by='name-desc'):
    """Search for AUR packages.

    .. versionchanged:: 3.0.0

    """
    aur_pkgs = RPC.search(search_by, pkgname)
    if aur_pkgs['type'] == 'error':
        raise AURError(aur_pkgs['error'])
    else:
        return [AURPackage.from_aurdict(d) for d in aur_pkgs['results']]


def msearch(maintainer):
    """Search for AUR packages maintained by a specified user.

    .. versionadded:: 3.0.0

    """
    aur_pkgs = RPC.search('maintainer', maintainer)
    if aur_pkgs['type'] == 'error':
        raise AURError(aur_pkgs['error'])
    else:
        return [AURPackage.from_aurdict(d) for d in aur_pkgs['results']]


def print_package_search(pkg, cachemode=False, prefix='', prefixp=''):
    """Output/return a package representation.

    Based on `pacman -Ss`.

    .. versionchanged:: 4.0.0

    """
    termwidth = get_termwidth(9001)

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
        pass  # for repository packages

    category = pkg.repo

    descl = textwrap.wrap(pkg.description, termwidth - len(prefixp2))

    desc2 = []
    for i in descl:
        desc2.append(prefix2 + i)
    desc = '\n'.join(desc2)
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
    """Output/return a package representation.

    Based on `pacman -Ss`.

    .. versionchanged:: 3.3.0

    """
    if pkgs == []:
        raise SanityError(_('Didn’t pass any packages.'),
                          source='utils.print_package_info')
    else:
        for i in pkgs:
            if not isinstance(i, AURPackage):
                raise SanityError(_('Trying to use utils.print_package_info '
                                    'with a repository package'),
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
Name           : {nme}
Package Base   : {bse}
Version        : {ver}
URL            : {url}
Licenses       : {lic}
Groups         : {grp}
Provides       : {prv}
Depends On     : {dep}
Make Deps      : {mkd}
Check Deps     : {ckd}
Optional Deps  : {opt}
Conflicts With : {cnf}
Replaces       : {rpl}
Votes          : {cmv}
Popularity     : {pop}
Out of Date    : {ood}
Maintainer     : {mnt}
First Submitted: {fsb}
Last Updated   : {upd}
Description    : {dsc}
Keywords       : {key}
""")

        to = []
        for pkg in pkgs:
            upd = pkg.modified.strftime(fmt)
            fsb = pkg.added.strftime(fmt)

            if pkg.is_outdated:
                ood = DS.colors['red'] + _('yes') + DS.colors['all_off']
            else:
                ood = _('no')
            termwidth = get_termwidth()
            if termwidth is None:
                termwidth = 9001  # Auto-wrap by terminal.

            to.append(t.format(nme=pkg.name,
                               bse=pkg.packagebase,
                               url=pkg.url,
                               ver=pkg.version,
                               lic=mlist(pkg.licenses, termwidth=termwidth),
                               grp=mlist(pkg.groups, termwidth=termwidth),
                               prv=mlist(pkg.provides, termwidth=termwidth),
                               dep=mlist(pkg.depends, termwidth=termwidth),
                               mkd=mlist(pkg.makedepends, termwidth=termwidth),
                               ckd=mlist(pkg.checkdepends,
                                         termwidth=termwidth),
                               opt=mlist(pkg.optdepends, sep='\n',
                                         change_spaces=False,
                                         termwidth=termwidth),
                               cnf=mlist(pkg.conflicts, termwidth=termwidth),
                               rpl=mlist(pkg.replaces, termwidth=termwidth),
                               cmv=pkg.votes,
                               pop=pkg.popularity,
                               ood=ood,
                               mnt=pkg.human,
                               upd=upd,
                               fsb=fsb,
                               dsc=hanging_indent(pkg.description, '',
                                                  termwidth, False, 17),
                               key=mlist(pkg.keywords, termwidth=termwidth)
                               )
                      )

    if cachemode:
        return '\n'.join(to)
    else:
        print('\n'.join(to))
