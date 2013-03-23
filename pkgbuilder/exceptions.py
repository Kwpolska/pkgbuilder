#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.99.4.0
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
           'PackageError', 'PackageNotFoundError', 'SanityError']


class PBException(Exception):
    """Base exception for PKGBUILDer."""
    def __init__(self, msg, *args, **kwargs):
        """Throw an error to the log and take the arguments."""
        DS.log.error('({0:<20}) {1}'.format(self.__qualname__, msg))
        self.msg = msg
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """You want to see error messages, don’t you?"""
        return self.msg


class AURError(PBException):
    """AUR-related errors."""
    def __init__(self, msg, *args, **kwargs):
        """Throw an error to the log and take the arguments."""
        DS.log.error('({0:<20}) {1}'.format(self.__qualname__, msg))
        self.msg = msg
        self.args = args
        self.kwargs = kwargs
    def __str__(self):
        """Just so the user knows that it’s an AUR error."""
        return '[AUR] ' + self.msg

class MakepkgError(PBException):
    """makepkg errors (return codes)"""
    def __init__(self, retcode, *args, **kwargs):
        """Throw an error to the log and take the arguments."""
        DS.log.error('({0:<20}) {1}'.format(self.__qualname__, retcode))
        self.retcode = retcode
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """“1” isn’t too helpful for the human."""
        return _('makepkg returned {0}.').format(self.retcode)

class NetworkError(PBException):
    """Network-related errors."""
    def __init__(self, msg, source, *args, **kwargs):
        """Throw an error to the log and take the arguments."""
        DS.log.error('({0:<20}) {1} (via {2})'.format(self.__qualname__, msg,
                                                      source))
        self.msg = msg
        self.source = source
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """The msg, wherever it may come from, isn’t helpful either."""
        return _('Network error: {0} (via {1})').format(self.msg, self.source)

class PackageError(PBException):
    """Package-related errors."""
    def __init__(self, msg, source, *args, **kwargs):
        """Throw an error to the log and take the arguments."""
        DS.log.error('({0:<20}) {1} (from {2})'.format(self.__qualname__, msg,
                                                       source))
        self.msg = msg
        self.source = source
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """Would be helpful, but not enough."""
        return _('{0} (Package: {1})').format(self.msg, self.source)

class PackageNotFoundError(PackageError):
    def __init__(self, name, *args, **kwargs):
        """Throw an error to the log and take the arguments."""
        DS.log.error('({0:<20}) {1}'.format(self.__qualname__, name))
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """This would be far, FAR away from being informative."""
        return _('Package {0} not found.').format(self.name)

class SanityError(PBException):
    """Sometimes PKGBUILDer or one of its friends can go insane."""
    def __init__(self, msg, *args, **kwargs):
        DS.log.error('({0:<20}) {1}'.format(self.__qualname__, msg))
        self.msg = msg
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return _('Sanity error!  {0}').format(self.msg)
