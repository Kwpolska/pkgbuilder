==========================
build module (Build class)
==========================
:Author: Kwpolska
:Copyright: © 2011-2012, Kwpolska.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2012-09-30
:Version: 2.1.4.8

.. module:: build

Build
=====

.. index:: Build
.. versionadded:: 2.1.0.0
.. class:: Build

This is the class for building packages.  It defines two base methods and
four additional ones.

.. method:: auto_build(pkgname[, performdepcheck][, pkginstall])
.. index:: makepkg; build

This is a function that handles building packages automatically.  This is
the recommended way of building packages through PKGBUILDer.

.. note::

    This function returns a list of packages to install with pacman -U.  Please
    take care of it.  Running PKGBUILDer/PBWrapper standalone or .main.main()
    will do that.

.. method:: build_runner(pkgname[, performdepcheck][, pkginstall])
.. index:: makepkg; build; validate

This is the function running building.  It is not supposed to be used
standalone, because it is embedded by :meth:`auto_build()`.

.. note::

    Data returned by this function may not be helpful.  Using :meth:`auto_build()`
    eliminates this problem.

.. method:: validate(pkgnames)

Check if packages were installed.

.. method:: install(pkgpaths)

Install packages through ``pacman -U``.

.. method:: download(urlpath, filename[, prot])

Downloads an AUR tarball.  Data normally provided by :meth:`build_runner()`.

.. method:: extract(filename)

Extracts an AUR tarball.  Data normally provided by :meth:`build_runner()`.

.. method:: prepare_deps(pkgbuild)
.. index:: depcheck, dependency

.. versionchanged:: 2.1.3.7

Gets (make)depends from a PKGBUILD and returns them.

..note:: due to a radical change of the algorithm, please provide the **absolute** path to the PKGBUILD (``os.path.abspath``).  Handles are not supported.  Strings are not supported since 2.1.4.0.

.. method:: depcheck(depends)
.. index:: depcheck, dependency

Performs a dependency check.  Data normally provided by
:meth:`prepare_deps()`.
