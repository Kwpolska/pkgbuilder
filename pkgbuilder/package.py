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

__all__ = ['Package', 'AURPackage', 'ABSPackage']


class Package(object):
    """A package, one of many."""
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


class AURPackage(Package):
    """An AUR package."""
    id = None
    is_outdated = None
    added = None
    modified = None
    votes = None
    urlpath = None

    @classmethod
    def from_aurdict(cls, aurdict):
        #a = cls()
        raise NotImplementedError


class ABSPackage(Package):
    """An ABS package."""
    architecture = None
