==========================
utils module (Utils class)
==========================

:Author: Kwpolska
:Copyright: See Appendix B.
:Date: 2012-08-01
:Version: 2.1.3.0

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

.. method:: print_package(pkg[, use_categories][, cachemode][, prefix][, prefixp])
.. index:: print

:Arguments: package name, use categories, cache mode, line prefix, line prefix in plain form (no colors etc.)
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

Prints data about `pkg` (returns the data in cache mode).  Format specified above, in the Format field.
