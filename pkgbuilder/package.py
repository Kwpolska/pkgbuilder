#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.99.5.0
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2013, Kwpolska.
# See /LICENSE for licensing information.

"""
    pkgbuilder.package
    ~~~~~~~~~~~~~~~~~~

    The Package class, the most important class in PKGBUILDer.

    :Copyright: © 2011-2013, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import UTC
from .exceptions import PackageError, SanityError
import datetime

__all__ = ['CATEGORIES', 'Package', 'AURPackage', 'ABSPackage']

CATEGORIES = ['ERROR', 'none', 'daemons', 'devel', 'editors',
              'emulators', 'games', 'gnome', 'i18n', 'kde',
              'lib', 'modules', 'multimedia', 'network',
              'office', 'science', 'system', 'x11',
              'xfce', 'kernels']


class Package(object):
    """A package, one of many."""
    is_abs = None
    name = None
    version = None
    description = None
    repo = None
    url = None
    licenses = None
    human = None

    def __init__(self, **kwargs):
        """Initialize the class."""
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        """Return something nice for people wanting a string."""
        return '-'.join(self.name, self.version)

    def __repr__(self):
        """Return something nice for people wanting a repr."""
        if self.is_abs:
            return '<ABS Package {0}-{1}>'.format(self.name, self.version)
        elif not self.is_abs:
            return '<AUR Package {0}-{1}>'.format(self.name, self.version)
        elif self.is_abs is None:
            return '<??? Package {0}-{1}>'.format(self.name, self.version)
        else:
            return SanityError('is_abs is invalid ({0})'.format(self.is_abs),
                               'Package.__repr__()', is_abs=self.is_abs)

class AURPackage(Package):
    """An AUR package."""
    id = None
    is_abs = False
    is_outdated = None
    added = None
    modified = None
    votes = None
    urlpath = None

    @classmethod
    def from_aurdict(cls, aurdict):
        bindings = {'Maintainer': 'human', 'ID': 'id', 'Name': 'name',
                    'Version': 'version', 'Description': 'description',
                    'URL': 'url', 'License': 'licenses', 'NumVotes': 'votes',
                    'URLPath': 'urlpath'}
        ignore = ['OutOfDate', 'CategoryID', 'FirstSubmitted', 'LastModified']

        p = cls()
        for k, v in aurdict.items():
            try:
                setattr(p, bindings[k], v)
            except KeyError:
                if k not in ignore:
                    raise PackageError('AURDict has an unknown {0} '
                                       'value'.format(k),
                                       'AURPackage.from_aurdict()',
                                       aurdict=aurdict)
        # Manual overrides.
        p.is_outdated = aurdict['OutOfDate'] == 1
        p.repo = CATEGORIES[aurdict['CategoryID']]

        utc = UTC()

        p.added = datetime.datetime.utcfromtimestamp(
            aurdict['FirstSubmitted']).replace(tzinfo=utc)
        p.modified = datetime.datetime.utcfromtimestamp(
            aurdict['LastModified']).replace(tzinfo=utc)

        return p


class ABSPackage(Package):
    """An ABS package."""
    is_abs = True
    architecture = None
