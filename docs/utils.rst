==========================
utils module (Utils class)
==========================

:Author: Kwpolska
:Copyright: © 2011-2012, Kwpolska.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2012-10-06
:Version: 2.1.5.1

.. module:: utils

Utils
=====

.. index:: Utils; Utilities
.. versionadded:: 2.1.0.0
.. class:: Utils

Common global utilities.  Provides useful data.  It defines three methods:


.. method:: info(pkgname)
.. index:: info

.. versionchanged:: 2.1.4.8

Returns informations about packages.  Almost equivalent to
:meth:`AUR.multiinfo(pkgnames)`, but returns ``[]`` if no packages were found.

.. method:: search(pkgname)
.. index:: search

Searches for AUR packages and returns them as a list.  Almost equivalent
to :meth:`AUR.request('search', pkgname)`, but returns ``[]`` if no
packages were found.

.. method:: print_package_search(pkg[, use_categories][, cachemode][, prefix][, prefixp])
.. index:: print

Outputs/returns a package representation similar to ``pacman -Ss``.  Format::

    category/name version (count votes) [installed: version] [out of date]
        description

(``category`` becomes ``aur`` when running with ``-S``.  Installed version
displayed only if it is different than the one in the AUR.)

.. method:: print_package_info(pkg[, cachemode][, force_utc])
.. index:: print


.. versionchanged:: 2.1.4.8

Outputs/returns a package representation similar to ``pacman -Si``.  Format (with en/C locale)::

    Repository     : aur
    Category       : package category
    Name           : package name
    Version        : package version
    URL            : package URL (from PKGBUILD)
    Licenses       : package license
    Votes          : votes count
    Out of Date    : out of date (yes/no), red if yes
    Maintainer     : package maintainer
    First Submitted: date of package’s first submission
    Last Updated   : date of package’s last update
    Description    : package description
