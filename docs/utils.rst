==========================
utils module (Utils class)
==========================

:Author: Kwpolska
:Copyright: © 2011-2012, Kwpolska.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2012-09-23
:Version: 2.1.4.6

.. module:: utils

Utils
=====

.. index:: Utils; Utilities
.. versionadded:: 2.1.0.0
.. class:: Utils

Common global utilities.  Provides useful data.  It defines three methods:


.. method:: info(pkgname)
.. index:: info

Returns information about a package.  Almost equivalent to
:meth:`AUR.request('info', pkgname)`, but returns **`None`** if the package
doesn't exist.

.. method:: search(pkgname)
.. index:: search

Searches for AUR packages and returns them as a list.  Almost equivalent
to :meth:`AUR.request('search', pkgname)`, but returns **`[]`** if no
packages were found.

.. method:: print_package_search(pkg[, use_categories][, cachemode][, prefix][, prefixp])
.. index:: print

Outputs/returns a package representation similar to ``pacman -Ss``.  Format specified above, in the Format field.

.. method:: print_package_info(pkg[, cachemode][, force_utc])
.. index:: print

Outputs/returns a package representation similar to ``pacman -Si``.

Outputs/returns a package representation similar to ``pacman -Si``.  Format (with en/C locale)::

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
