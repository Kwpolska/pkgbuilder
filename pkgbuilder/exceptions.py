#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v3.0.1
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2013, Kwpolska.
# See /LICENSE for licensing information.

"""
    pkgbuilder.exceptions
    ~~~~~~~~~~~~~~~~~~~~~

    The exceptions for use in PKGBUILDer.

    :Copyright: © 2011-2013, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, _
__all__ = ['PBException', 'AURError', 'MakepkgError', 'NetworkError',
           'ConnectionError', 'HTTPError', 'PackageError',
           'PackageNotFoundError', 'SanityError']


class PBException(Exception):
    """Base exception for PKGBUILDer."""
    qualname = 'PBException'
    def __init__(self, msg, source, *args, **kwargs):
        """Throw an error to the log and take the arguments."""
        DS.log.error('({0:<20}) {1}'.format(self.qualname, msg))
        self.msg = msg
        self.source = source
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """You want to see error messages, don’t you?"""
        return self.msg


class AURError(PBException):
    """AUR-related errors."""
    qualname = 'AURError'
    def __init__(self, msg, *args, **kwargs):
        """Throw an error to the log and take the arguments."""
        DS.log.error('({0:<20}) {1}'.format(self.qualname, msg))
        self.msg = msg
        self.source = 'AUR'
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """Just so the user knows that it’s an AUR error."""
        return _('AUR Error: {0}').format(self.msg)


class MakepkgError(PBException):
    """makepkg errors (return codes)"""
    qualname = 'MakepkgError'
    def __init__(self, retcode, *args, **kwargs):
        """Throw an error to the log and take the arguments."""
        DS.log.error('({0:<20}) {1}'.format(self.qualname, retcode))
        self.retcode = retcode
        self.source = 'makepkg'
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """“1” isn’t too helpful for the human."""
        return _('makepkg returned {0}.').format(self.retcode)


class NetworkError(PBException):
    """Network-related errors."""
    qualname = 'NetworkError'
    def __init__(self, msg, source, *args, **kwargs):
        """Throw an error to the log and take the arguments."""
        DS.log.error('({0:<20}) {1} (via {2})'.format(self.qualname, msg,
                                                      source))
        self.msg = msg
        try:
            self.source = source.args[0].reason
        except:
            try:
                self.source = source.args[0]
            except:
                self.source = source
        self._source = source
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """The msg, wherever it may come from, isn’t helpful either."""
        return _('Network error: {0} (via {1})').format(self.msg, self.source)


class ConnectionError(NetworkError):
    """A connection error."""
    qualname = 'ConnectionError'
    def __str__(self):
        return _('Connection error: {0} (via {1})').format(self.msg,
                                                           self.source)


class HTTPError(NetworkError):
    """An HTTP error."""
    qualname = 'HTTPError'
    def __init__(self, source, origin, *args, **kwargs):
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
        self.args = args
        self.kwargs = kwargs
        self.code = source.status_code

    def __str__(self):
        """For human-friendliness."""
        return self.msg


class PackageError(PBException):
    """Package-related errors."""
    qualname = 'PackageError'
    def __init__(self, msg, source, *args, **kwargs):
        """Throw an error to the log and take the arguments."""
        DS.log.error('({0:<20}) {1} (from {2})'.format(self.qualname, msg,
                                                       source))
        self.msg = msg
        self.source = source
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """Would be helpful, but not enough."""
        return _('{0} (Package: {1})').format(self.msg, self.source)


class PackageNotFoundError(PackageError):
    qualname = 'PackageNotFoundError'
    def __init__(self, name, source, *args, **kwargs):
        """Throw an error to the log and take the arguments."""
        DS.log.error('({0:<20}) {1} (via {2})'.format(self.qualname, name,
                                                      source))
        self.name = name
        self.msg = _('Package {0} not found. (via {1})').format(name, source)
        self.source = source
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """This would be far, FAR away from being informative."""
        return self.msg


class SanityError(PBException):
    """Sometimes PKGBUILDer or one of its friends can go insane."""
    qualname = 'SanityError'
    def __init__(self, msg, source, *args, **kwargs):
        DS.log.error('({0:<20}) {1} (via {2})'.format(self.qualname, msg,
                                                      source))
        self.msg = msg
        self.source = source
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return _('Sanity error!  {0} (via {1})').format(self.msg, self.source)
