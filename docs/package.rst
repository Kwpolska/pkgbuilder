========================================================
package module (Package, AURPackage, ABSPackage classes)
========================================================

:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2011-2018, Chris Warrick.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2018-03-18
:Version: 4.2.16

.. index:: Package
.. index:: AURPackage
.. index:: ABSPackage
.. versionadded:: 3.0.0

Added in 3.0.0, the Package family of classes is the core of PKGBUILDer.  They
are responsible for storing package data in a consistent way.  All class
entries are Pythonic.

**Historic note:** whenever *ABS* is used, it means *repository package*. The ABS tool was deprecated in 2017 and replaced by ASP; however, PKGBUILDer uses that abbreviation to refer to packages that are in Arch repositories.

.. automodule:: pkgbuilder.package

.. autoclass:: pkgbuilder.package.Package
   :members:

This is base class.  It shouldn’t be used directly.  It contains the following
attributes:

+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| Name              | Type   | Default | Description                                                                                 |
+===================+========+=========+=============================================================================================+
| is_abs            | bool   | None    | A boolean informing of the package type, to prevent ``isinstance(pkg, ABSPackage)`` checks. |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| name              | str    | None    | The name of the package.                                                                    |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| version           | str    | None    | Current package version.                                                                    |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| description       | str    | None    | Package description.                                                                        |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| repo              | str    | None    | The repo or category (AUR) of the package in question.                                      |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| url               | str    | None    | The upstream URL specified in the PKGBUILD.                                                 |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| licenses          | list   | []      | Licenses specified in the PKGBUILD.                                                         |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| human             | str    | None    | The packager (repo) or maintainer (AUR) of the package in question.                         |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+

.. autoclass:: pkgbuilder.package.AURPackage
   :members:

This class contains all the attributes of :class:`Package`, ``is_abs = False`` and the following attributes:

+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| Name              | Type   | Default | Description                                                                                 |
+===================+========+=========+=============================================================================================+
| id                | int    | None    | ID of the AUR package.                                                                      |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| is_outdated       | bool   | None    | Package OoD flag status in the AUR.                                                         |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| outdated_since    | date   | None    | A date (``datetime.datetime()``, aware UTC) of OoD flagging date OR ``None``.               |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| added             | date   | None    | A date (``datetime.datetime()``, aware UTC) representing package addition time.             |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| modified          | date   | None    | A date (``datetime.datetime()``, aware UTC) representing the last modification time.        |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| votes             | int    | None    | Count of AUR votes.                                                                         |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| urlpath           | str    | None    | The URL of the tarball, sans ``https://aur.archlinux.org``. Not used in AURv4.              |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+
| _category_id      | int    | None    | AUR Category ID, not supposed to be used by most people (hence the underscore).             |
+-------------------+--------+---------+---------------------------------------------------------------------------------------------+

.. autoclass:: pkgbuilder.package.AURPackage
   :members:

This class has a total of 29 attributes (21 if you exclude the :class:`Package` ones) and ``is_abs = True``.  For more information, consult either the attribute names or documentation for/code of libalpm and pyalpm.

..
    vim: tw=1000
