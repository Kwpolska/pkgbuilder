==========================
build module (Build class)
==========================
:Author: Kwpolska
:Copyright: See Appendix B.
:Date: 2012-08-08
:Version: 2.1.3.2

.. module:: build

Build
=====

.. index:: Build
.. versionadded:: 2.1.0.0
.. class:: Build

This is the class for building packages.  It defines two base methods and
four additional ones.

.. method:: auto_build(pkgname[, validate][, depcheck])
.. index:: makepkg; build

:Arguments: package name, validate installation, perform dependency checks.
:Input: none.
:Output: text.
:Returns: nothing.
:Exceptions: PBError.
:Message codes:
    WRN3401, ERR3402, INF3450, ERR3451, ERR3452.
:Former data:
    2.0 Name: build.

This is a function that handles building packages automatically.  This is
the recommended way of building packages through PKGBUILDer.

.. method:: build_runner(pkgname[, depcheck])
.. index:: makepkg; build; validate

:Arguments: pkgname, perform dependency checks.
:Input: none.
:Output: text.
:Returns: ::

    [makepkg's/auto_build's retcode OR 16 if an AUR dep is needed, [AUR deps or retcode source]]

:Exceptions: PBError.
:Message codes: ERR3001, ERR3201, ERR3202.
:Former data:
    2.0 Behavior: all functions inside

    2.0 Name: buildSub

This is the function running building.  It is not supposed to be used
standalone, because it is embedded by :meth:`auto_build()`.

.. note::

    The return codes of this function work bad.  Using :meth:`auto_build()`
    eliminates this problem.

.. method:: download(urlpath, filename[, prot])

:Arguments: URL, filename for saving, protocol.
:Input: none.
:Output: none.
:Returns: bytes downloaded.
:Exceptions:
    PBError, IOError, requests.exceptions.*
:Message codes: ERR3101, ERR3102.

Downloads an AUR tarball.  Data normally provided by :meth:`build_runner()`.

.. method:: extract(filename)

:Arguments: filename.
:Input: none.
:Output: none.
:Returns: file count.
:Exceptions: PBError, IOError.
:Message codes: ERR3151.

Extracts an AUR tarball.  Data normally provided by :meth:`build_runner()`.

.. method:: prepare_deps(pkgbuild)
.. index:: depcheck, dependency

:Arguments: PKGBUILD contents
:Input: none.
:Output: none.
:Returns:
    a list with entries from PKGBUILD's depends and makedepends
    (can be empty.)
:Exceptions: IOError.
:Message codes: none.

Gets (make)depends from a PKGBUILD and returns them.

.. note::
    `pkgbuild` is a string, not a file handle.

.. method:: depcheck(depends)
.. index:: depcheck, dependency

:Arguments: a python dependency list.
:Input: none.
:Output: none.
:Returns:
    a dict, key is the package name, and value is: -1 = nowhere, 0 = system,
    1 = repos, 2 = AUR.
:Exceptions: PBError.
:Message codes: ERR3201.

:Former data:
    2.0 Returns: no -1

Performs a dependency check.  Data normally provided by
:meth:`prepare_deps()`.
