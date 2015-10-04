# -*- encoding: utf-8 -*-
# PKGBUILDer v4.2.4
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2015, Chris Warrick.
# See /LICENSE for licensing information.

"""
The Package class, the most important class in PKGBUILDer.

:Copyright: © 2011-2015, Chris Warrick.
:License: BSD (see /LICENSE).
"""

from . import UTC, DS
from .exceptions import SanityError
import datetime

__all__ = ('Package', 'AURPackage', 'ABSPackage')


def mktime(ts):
    return datetime.datetime.utcfromtimestamp(ts).replace(tzinfo=UTC)


class Package(object):

    """The base class for packages."""

    is_abs = None
    name = ''
    version = ''
    description = ''
    repo = ''
    url = ''
    licenses = []
    human = ''
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

    repo = 'aur'
    id = None
    packagebase = ''
    packagebaseid = None
    makedepends = []
    checkdepends = []
    is_abs = False
    is_outdated = None
    outdated_since = None
    added = None
    modified = None
    votes = None
    urlpath = ''
    popularity = None

    @classmethod
    def from_aurdict(cls, aurdict):
        """Create an instance of AURPackage from AUR RPC data."""
        bindings = {'Description': 'description',
                    'ID': 'id',
                    'Maintainer': 'human',
                    'Name': 'name',
                    'NumVotes': 'votes',
                    'URL': 'url',
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
                    'URLPath': 'urlpath',
                    'Popularity': 'popularity',
                    }
        ignore = ['OutOfDate', 'FirstSubmitted', 'LastModified']

        p = cls()
        for k, v in aurdict.items():
            try:
                if v is not None:
                    setattr(p, bindings[k], v)
            except KeyError:
                if k not in ignore:
                    DS.log.warn('AURDict has an unknown {0} key: {1}'.format(
                        k, aurdict))

        # Manual overrides.
        p.is_outdated = aurdict['OutOfDate'] is not None

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
    arch = ''
    backup = []
    base64_sig = None
    builddate = None
    deltas = []
    download_size = None
    filename = ''
    files = []
    has_scriptlet = None
    installdate = None
    isize = None
    md5sum = ''
    reason = []
    sha256sum = ''
    size = None

    @classmethod
    def from_pyalpm(cls, abspkg):
        """Transform a pyalpm.Package into a pkgbuilder.package.ABSPackage."""
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
