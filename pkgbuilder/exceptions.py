# -*- encoding: utf-8 -*-
# PKGBUILDer v4.2.18
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2018, Chris Warrick.
# See /LICENSE for licensing information.

"""
Defines PKGBUILDer exceptions.

:Copyright: © 2011-2018, Chris Warrick.
:License: BSD (see /LICENSE).
"""

from . import DS, _
__all__ = ('PBException', 'AURError', 'MakepkgError', 'NetworkError',
           'ConnectionError', 'HTTPError', 'PackageError',
           'PackageNotFoundError', 'SanityError', 'CloneError')


class PBException(Exception):
    """Base exception for PKGBUILDer."""

    qualname = 'PBException'

    def __init__(self, msg, source, exit=True, *args, **kwargs):
        """Initialize and log the error."""
        DS.log.error('({0:<20}) {1}'.format(self.qualname, msg))
        self.msg = msg
        self.source = source
        self.exit = exit
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """Return a friendly representation of the exception."""
        return self.msg


class AURError(PBException):
    """AUR-related errors."""

    qualname = 'AURError'

    def __init__(self, msg, exit=True, *args, **kwargs):
        """Initialize and log the error."""
        DS.log.error('({0:<20}) {1}'.format(self.qualname, msg))
        self.msg = msg
        self.source = 'AUR'
        self.exit = exit
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """Return a friendly representation of the exception."""
        return _('AUR Error: {0}').format(self.msg)


class MakepkgError(PBException):
    """makepkg return codes."""

    qualname = 'MakepkgError'

    def __init__(self, retcode, exit=True, *args, **kwargs):
        """Initialize and log the error."""
        DS.log.error('({0:<20}) {1}'.format(self.qualname, retcode))
        self.retcode = retcode
        self.source = 'makepkg'
        self.exit = exit
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """Return a friendly representation of the exception."""
        return _('makepkg returned {0}.').format(self.retcode)


class NetworkError(PBException):
    """Network-related errors."""

    qualname = 'NetworkError'

    def __init__(self, msg, source, exit=True, *args, **kwargs):
        """Initialize and log the error."""
        DS.log.error('({0:<20}) {1} (via {2})'.format(self.qualname, msg,
                                                      source))
        self.msg = msg
        try:
            self.source = source.args[0].reason
        except Exception:
            try:
                self.source = source.args[0]
            except Exception:
                self.source = source
        self._source = source
        self.exit = exit
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """Return a friendly representation of the exception."""
        return _('Network error: {0} (via {1})').format(self.msg, self.source)


class ConnectionError(NetworkError):
    """A connection error."""

    qualname = 'ConnectionError'

    def __str__(self):
        """Return a friendly representation of the exception."""
        return _('Connection error: {0} (via {1})').format(self.msg,
                                                           self.source)


class HTTPError(NetworkError):
    """An HTTP error."""

    qualname = 'HTTPError'

    def __init__(self, source, origin, exit=True, *args, **kwargs):
        """Initialize and log the error."""
        DS.log.error('({0:<20}) {1} (via {2})'.format(self.qualname,
                                                      source.status_code,
                                                      source))
        self.msg = _('HTTP Error {0} (via {1})').format(source.status_code,
                                                        source)
        self.source = source
        try:
            self.origin = origin.args[0].reason
        except:
            try:
                self.origin = origin.args[0]
            except:
                self.source = origin
        self._origin = origin
        self.exit = exit
        self.args = args
        self.kwargs = kwargs
        self.code = source.status_code


class PackageError(PBException):
    """Package-related errors."""

    qualname = 'PackageError'

    def __init__(self, msg, source, exit=True, *args, **kwargs):
        """Initialize and log the error."""
        DS.log.error('({0:<20}) {1} (from {2})'.format(self.qualname, msg,
                                                       source))
        self.msg = msg
        self.source = source
        self.exit = exit
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """Return a friendly representation of the exception."""
        return _('{0} (Package: {1})').format(self.msg, self.source)


class PackageNotFoundError(PackageError):
    """Errors raised when a package cannot be found."""

    qualname = 'PackageNotFoundError'

    def __init__(self, name, source, exit=True, *args, **kwargs):
        """Initialize and log the error."""
        DS.log.error('({0:<20}) {1} (via {2})'.format(self.qualname, name,
                                                      source))
        self.name = name
        self.msg = _('Package {0} not found. (via {1})').format(name, source)
        self.source = source
        self.exit = exit
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """Return a friendly representation of the exception."""
        return self.msg


class SanityError(PBException):
    """When PKGBUILDer or one of its friends goes insane."""

    qualname = 'SanityError'

    def __init__(self, msg, source, exit=True, *args, **kwargs):
        """Initialize and log the error."""
        DS.log.error('({0:<20}) {1} (via {2})'.format(self.qualname, msg,
                                                      source))
        self.msg = msg
        self.source = source
        self.exit = exit
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """Return a friendly representation of the exception."""
        return _('Sanity error!  {0} (via {1})').format(self.msg, self.source)


class CloneError(PBException):
    """A ``git clone`` failed."""

    qualname = 'CloneError'

    def __init__(self, returncode, exit=True, *args, **kwargs):
        """Initialize and log the error."""
        DS.log.error('({0:<20}) git clone returned {1}'.format(
            self.qualname, returncode))
        self.returncode = returncode
        self.msg = _('git clone returned {0}.').format(self.returncode)
        self.exit = exit
        self.args = args
        self.kwargs = kwargs


class ClonePathExists(CloneError):
    """The clone path exists and is not a git repository."""

    qualname = 'ClonePathExists'

    def __init__(self, pkgbase, exit=False, *args, **kwargs):
        DS.log.error('({0:<20}) directory {1} exists, but is not a git '
                     'repository'.format(self.qualname, pkgbase))
        self.pkgbase = pkgbase
        self.msg = _('Directory {0} exists, but is not a git '
                     'repository.').format(self.pkgbase)
        self.exit = exit
        self.args = args
        self.kwargs = kwargs


class EmptyRepoError(CloneError):
    """Git cloned an empty repository."""

    qualname = 'EmptyRepoError'

    def __init__(self, pkgbase, exit=False, *args, **kwargs):
        """Initialize and log the error."""
        DS.log.error('({0:<20}) repository {1} is empty'.format(
            self.qualname, pkgbase))
        self.pkgbase = pkgbase
        self.msg = _('Repository {0} is empty.').format(self.pkgbase)
        self.exit = exit
        self.args = args
        self.kwargs = kwargs
