#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v3.3.2
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2015, Chris Warrick.
# See /LICENSE for licensing information.

"""
    pkgbuilder.package
    ~~~~~~~~~~~~~~~~~~

    The Package class, the most important class in PKGBUILDer.

    :Copyright: © 2011-2015, Chris Warrick.
    :License: BSD (see /LICENSE).
"""

from . import UTC, DS
from .exceptions import SanityError
import datetime

__all__ = ['CATEGORIES', 'Package', 'AURPackage', 'ABSPackage']

CATEGORIES = ['none', 'none', 'daemons', 'devel', 'editors',
              'emulators', 'games', 'gnome', 'i18n', 'kde',
              'lib', 'modules', 'multimedia', 'network',
              'office', 'science', 'system', 'x11',
              'xfce', 'kernels', 'fonts', 'wayland']


def mktime(ts):
    return datetime.datetime.utcfromtimestamp(ts).replace(tzinfo=UTC)


class Package(object):
    """The base class for packages."""
    is_abs = None
    name = None
    version = None
    description = None
    repo = None
    url = None
    licenses = []
    human = None
    depends = []
    optdepends = []
    conflicts = []
    provides = []
    replaces = []
    groups = []

    def __init__(self, **kwargs):
        """Initialize the class."""
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        """Return something nice for people wanting a string."""
        return '-'.join((self.name, self.version))

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
    packagebase = None
    packagebaseid = None
    makedepends = []
    checkdepends = []
    is_abs = False
    is_outdated = None
    outdated_since = None
    added = None
    modified = None
    votes = None
    urlpath = None
    _categoryid = None

    @classmethod
    def from_aurdict(cls, aurdict):
        """
        Creates an instance of AURPackage using a dictionary from the AUR RPC.
        """
        bindings = {'CategoryID': '_categoryid',
                    'Description': 'description',
                    'ID': 'id',
                    'Maintainer': 'human',
                    'Name': 'name',
                    'NumVotes': 'votes',
                    'URL': 'url',
                    'URLPath': 'urlpath',
                    'Version': 'version',
                    'PackageBase': 'packagebase',
                    'PackageBaseID': 'packagebaseid',
                    'Depends': 'depends',
                    'MakeDepends': 'makedepends',
                    'CheckDepends': 'checkdepends',
                    'OptDepends': 'optdepends',
                    'Conflicts': 'conflicts',
                    'Provides': 'provides',
                    'Replaces': 'replaces',
                    'Groups': 'groups',
                    'License': 'licenses',
                    }
        ignore = ['OutOfDate', 'FirstSubmitted', 'LastModified']

        p = cls()
        for k, v in aurdict.items():
            try:
                setattr(p, bindings[k], v)
            except KeyError:
                if k not in ignore:
                    DS.log.warn('AURDict has an unknown {0} key: {1}'.format(
                        k, aurdict))
        # Manual overrides.
        p.is_outdated = aurdict['OutOfDate'] > 0
        p.repo = CATEGORIES[aurdict['CategoryID']]

        if p.is_outdated:
            p.outdated_since = mktime(aurdict['OutOfDate'])
        else:
            p.outdated_since = None
        p.added = mktime(aurdict['FirstSubmitted'])
        p.modified = mktime(aurdict['LastModified'])

        return p


class ABSPackage(Package):
    """An ABS package."""
    is_abs = True
    # Most of those aren’t necessary, but I am copying them over because I can.
    arch = None
    backup = []
    base64_sig = None
    builddate = None
    deltas = []
    download_size = None
    filename = None
    files = []
    has_scriptlet = None
    installdate = None
    isize = None
    md5sum = None
    reason = []
    sha256sum = None
    size = None

    @classmethod
    def from_pyalpm(cls, abspkg):
        """Transforms a pyalpm.Package into a pkgbuilder.package.ABSPackage."""
        copy = ['arch', 'backup', 'base64_sig', 'conflicts', 'deltas',
                'depends', 'download_size', 'filename', 'files', 'groups',
                'has_scriptlet', 'isize', 'licenses', 'md5sum', 'name',
                'optdepends', 'provides', 'reason', 'replaces', 'sha256sum',
                'size', 'url', 'version']
        p = cls()

        for i in copy:
            setattr(p, i, getattr(abspkg, i))

        p.repo = abspkg.db.name
        p.description = abspkg.desc
        p.human = abspkg.packager
        p.builddate = mktime(abspkg.builddate)
        p.installdate = mktime(abspkg.installdate)

        return p
