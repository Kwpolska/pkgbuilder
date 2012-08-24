==========================
utils module (Utils class)
==========================

:Author: Kwpolska
:Copyright: See Appendix B.
:Date: 2012-08-24
:Version: 2.1.3.6

.. module:: utils

Utils
=====

.. index:: Utils; Utilities
.. versionadded:: 2.1.0.0
.. class:: Utils

Common global utilities.  Provides useful data.  It defines three methods:


.. method:: info(pkgname)
.. index:: info

:Arguments: package name.
:Input: none.
:Output: none.
:Returns: a dict with package data OR None.
:Exceptions: none.
:Message codes: none.
:Former data:
    2.1.2.1 Returns: a dict OR False.

    2.0 Returns: aur_pkgs, list->dict, not null.

    2.0 Behavior: exception and quit when not found."

Returns information about a package.  Almost equivalent to
:meth:`AUR.request('info', pkgname)`, but returns **`None`** if the package
doesn't exist.

.. method:: search(pkgname)
.. index:: search

:Arguments: package name.
:Input: none.
:Output: none.
:Returns: a list of packages.
:Exceptions: none.
:Message codes: none.

Searches for AUR packages and returns them as a list.  Almost equivalent
to :meth:`AUR.request('search', pkgname)`, but returns **`[]`** if no
packages were found.

.. method:: print_package_search(pkg[, use_categories][, cachemode][, prefix][, prefixp])
.. index:: print

:Arguments: package object, use categories, cache mode, line prefix, line prefix in plain form (no colors etc.)
:Input: none.
:Output: with cache mode **off**, package details as in the Format field, otherwise nothing.
:Retruns: with cache mode **on**, package details as in the Format field, otherwise nothing.
:Format: ::

    > prefix category/name version (num votes) [installed: version] [out of date]
    > prefix     description

:Exceptions: none.
:Message codes: none.
:Former data:
    2.0 Name: showInfo.

Outputs/returns a package representation similar to ``pacman -Ss``.  Format specified above, in the Format field.

.. method:: print_package_info(pkg[, cachemode][, force_utc])
.. index:: print

Outputs/returns a package representation similar to ``pacman -Si``.

:Arguments: package object, cache mode, force UTC.
:Input: none.
:Output: with cache mode off, package info, otherwise nothing.
:Returns: with cache mode on, package info, otherwise nothing.
:Exceptions: none.
:Message codes: none.
:Former data:
    2.1.3.0 Location: .main.main() (inaccessible to 3rd parties)

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
