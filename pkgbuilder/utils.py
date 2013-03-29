#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.99.5.0
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
from pkgbuilder.exceptions import SanityError, AURError
import pyalpm
import os
import subprocess
import textwrap
import datetime

__all__ = ['info', 'search', 'print_package_search', 'print_package_info']
RPC = AUR()


def info(pkgnames):
    """
    .. versionchanged:: 2.1.4.8

    Returns info about packages.
    """
    aur_pkgs = RPC.multiinfo(pkgnames, DS.protocol)
    if aur_pkgs == []:
        return []
    elif aur_pkgs['type'] == 'error':
        # There are other cases where the "results" element is a string;
        # type = error seems to cover at least one case
        raise AURError(aur_pkgs['results'])
    else:
        return aur_pkgs['results']


def search(pkgname):
    """Searches for AUR packages."""
    aur_pkgs = RPC.request('search', pkgname, DS.protocol)
    if aur_pkgs == []:
        return []
    else:
        return aur_pkgs['results']


def print_package_search(pkg, use_categories=True, cachemode=False, prefix='',
                         prefixp=''):
    """
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
    if pkg['OutOfDate'] > 0:
        installed = (installed + ' ' + DS.colors['red'] + _(
                     '[out of date]') + DS.colors['all_off'])

    if pkg['CategoryID'] != 0:
        if use_categories:
            category = DS.categories[pkg['CategoryID']]
        else:
            category = 'aur'
    else:
        category = pkg['Category']  # ABS build cheat.

    descl = textwrap.wrap(pkg['Description'], termwidth - len(prefixp2))

    desc = []
    for i in descl:
        desc.append(prefix2 + i)
    desc = '\n'.join(desc)
    base = (prefix + '{0}/{1} {2} ({4} ' + _('votes') + '){5}\n' + '{3}')
    entry = (base.format(category, pkg['Name'], pkg['Version'], desc,
                         pkg['NumVotes'], installed))

    if cachemode:
        return entry
    else:
        print(entry)


def print_package_info(pkgs, cachemode=False, force_utc=False):
    """
    .. versionchanged:: 2.1.4.8

    Outputs/returns a package representation, which is close to the output
    of ``pacman -Si``.
    """
    if pkgs == []:
        raise SanityError('Didn’t pass any packages.')
    else:
        loct = os.getenv('LC_TIME')
        loc = os.getenv('LC_ALL')

        if loc == '':
            loc = os.getenv('LANG')

        if loc == '':
            loc = 'en_US.UTF-8'

        if loct == '':
            loct = loc

        fmt = '%Y-%m-%dT%H:%M:%S%Z'

        class UTC(datetime.tzinfo):
            """Universal Time, Coordinated."""

            def utcoffset(dt):
                return datetime.timedelta(0)

            def tzname(dt):
                return "Z"

            def dst(dt):
                return datetime.timedelta(0)

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
            if force_utc:
                upd = datetime.datetime.fromtimestamp(
                    float(pkg['LastModified']),
                    tz=UTC()).strftime(fmt)
                fsb = datetime.datetime.fromtimestamp(
                    float(pkg['FirstSubmitted']),
                    tz=UTC()).strftime(fmt)
            else:
                upd = datetime.datetime.fromtimestamp(
                    float(pkg['LastModified'])).strftime(fmt)
                fsb = datetime.datetime.fromtimestamp(
                    float(pkg['FirstSubmitted'])).strftime(fmt)

            if pkg['OutOfDate'] > 0:
                ood = DS.colors['red'] + _('yes') + DS.colors['all_off']
            else:
                ood = _('no')

            to.append(t.format(cat=DS.categories[pkg['CategoryID']],
                               nme=pkg['Name'], url=pkg['URL'],
                               ver=pkg['Version'], lic=pkg['License'],
                               cmv=pkg['NumVotes'], ood=ood,
                               mnt=pkg['Maintainer'], upd=upd, fsb=fsb,
                               dsc=pkg['Description']))

    if cachemode:
        return '\n'.join(to)
    else:
        print('\n'.join(to))
