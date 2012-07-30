*********************
Classes in PKGBUILDer
*********************

:Author: Kwpolska
:Copyright: See Appendix B.
:Date: #{date}
:Version: 2.1.2.32

.. index:: classes
.. module:: PKGBUILDer
   :synopsis: a Python AUR helper/library

PKGBUILDer uses some classes.  Here they are:

PBDS
====

.. index:: PBDS; DS; Data Storage
.. versionadded:: 2.1.0.0
.. class:: PBDS

This is the class used for storing data.  Currently, it stores this
information:

+-----------+---------------------------------------+-------------------+
| variable  | contents/usage                        | default           |
+===========+=======================================+===================+
| colors    | colors currently used in the script   | [colors]_         |
+-----------+---------------------------------------+-------------------+
| pacman    | using wrapper-friendly behavior[beh]? | False             |
+-----------+---------------------------------------+-------------------+
| validate  | validating package installation?      | True              |
+-----------+---------------------------------------+-------------------+
| depcheck  | checking if deps are installed?       | True              |
+-----------+---------------------------------------+-------------------+
| mkpkginst | if makepkg should install packages    | True              |
+-----------+---------------------------------------+-------------------+
| protocol  | protocol used to connect to the AUR   | http              |
+-----------+---------------------------------------+-------------------+
| categories| AUR categories list                   | [categories]_     |
+-----------+---------------------------------------+-------------------+
| inttext   | text shown while interrupting (^C)    | [inttext]_        |
+-----------+---------------------------------------+-------------------+
| confdir   | configuration directory               | [confdir]_        |
+-----------+---------------------------------------+-------------------+
| log       | logger object (eg. PBDS.log.info)     | logger object     |
+-----------+---------------------------------------+-------------------+

.. [beh] *wrapper-friendly behavior* (-S): building in /tmp;
    :meth:`Utils.print_package` says aur/name

.. [colors] Code below.

::

    self.colors = {
        'all_off':    '\x1b[1;0m',
        'bold':       '\x1b[1;1m',
        'blue':       '\x1b[1;1m\x1b[1;34m',
        'green':      '\x1b[1;1m\x1b[1;32m',
        'red':        '\x1b[1;1m\x1b[1;31m',
        'yellow':     '\x1b[1;1m\x1b[1;33m'
    }

.. [categories] The categories come from `aurweb <https://aur.archlinux.org>`_, and are as follows:

::

    self.categories = ['ERROR', 'none', 'daemons', 'devel', 'editors',
                       'emulators', 'games', 'gnome', 'i18n', 'kde',
                       'lib', 'modules', 'multimedia', 'network',
                       'office', 'science', 'system', 'x11',
                       'xfce', 'kernels']

.. [inttext] Used by /scripts/pkgbuilder, internationalized, looks like this: ``[ERR5001] Aborted by user! Exiting…``

.. [confdir] Config directory.  Usually ``~/.config/kwpolska/pkgbuilder``

It also has two methods:

.. method:: colorson()

:Arguments: none.
:Input: none.
:Output: none.
:Returns: nothing.
:Exceptions: none.
:Message codes: none.

Turns colors on.

.. method:: colorsoff().

:Arguments: none.
:Input: none.
:Output: none.
:Returns: nothing.
:Exceptions: none.
:Message codes: none.

Turns colors off.


AUR
===

.. index:: AUR; API; RPC
.. versionadded:: 2.1.0.0
.. class:: AUR

This is the class used for calling the AUR API.  It defines four methods:

.. method:: request(rtype, arg[, prot])
.. index:: request

:Arguments: request type, argument (package name), protocol.
:Input: none.
:Output: none.
:Returns: Data from the API.
:Exceptions: requests.exceptions.*, PBError.
:Message codes: ERR1001.

Makes a request and returns data.  Valid types of requests are listed on
the `AUR API's page`_.  Currently tested and working ones are:

+-------------+-----------------------------------+
+ name        | purpose                           |
+=============+===================================+
| info        | get info about `arg`              |
+-------------+-----------------------------------+
| search      | search for `arg` in the AUR       |
+-------------+-----------------------------------+
| maintsearch | show packages maintained by `arg` |
+-------------+-----------------------------------+

multiinfo is implemented in another function, :meth:`multiinfo()`.

.. _`AUR API's page`: http://aur.archlinux.org/rpc.php

.. method:: multiinfo(args[, prot])
.. index:: multiinfo

:Arguments: a list of packages, protocol.
:Input: none.
:Output: none.
:Returns: Data from the API.
:Exceptions: requests.exceptions.*, PBError.
:Message codes: ERR1001.

Makes a multiinfo request.  A multiinfo request can retrieve information
for multiple packages.

.. method:: jsonreq(rtype, arg[, prot])

:Arguments: request type, argument (package name), protocol.
:Input: none.
:Output: none.
:Returns: JSON data from the API.
:Exceptions: requests.exceptions.*, PBError.
:Message codes: ERR1001.


Makes a :meth:`request()`, but returns plain JSON data.  Valid values of
`rtype` are listed in :meth:`request()`'s documentation.

.. method:: jsonmultiinfo(args[, prot])

:Arguments: a list of packages, protocol.
:Input: none.
:Output: none.
:Returns: JSON data from the API.
:Exceptions: requests.exceptions.*, PBError.
:Message codes: ERR1001.

Makes a :meth:`multiinfo()` request, but returns plain JSON data.

Utils
=====

.. index:: Utils; Utilities
.. versionadded:: 2.1.0.0
.. class:: Utils

This is the class with many random utilities.  It defines three methods:


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

.. method:: print_package(pkg[, use_categories][, prefix][, cachemode])
.. index:: print

:Arguments: package name, use categories, cache mode, line prefix.
:Input: none.
:Output: (with cache mode off, otherwise nothing)
    ::
    prefix category/name version (num votes) [installed: version] [out of date]
    prefix     description

:Returns: (with cache mode on, otherwise nothing)
    ::
    prefix category/name version (num votes) [installed: version] [out of date]
    prefix     description

:Exceptions: none.
:Message codes: none.
:Former data:
    2.0 Name: showInfo.

Prints data about `pkg` (returns in cache mode).  Format specified above, in the Output and Return fields.

Build
=====

.. index:: Build; makepkg
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
    ERR3301, ERR34?? (ERR3401, ERR3450, ERR3451, ERR3452), INF3450.
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

    [makepkg's retcode or 3 if fails or 16 if needs an AUR dep,
        [AUR deps or 'makepkg'] or nothing
    ]

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
:Suggested way of handling:
    ::

    types = ['system', 'repos', 'aur']
    for pkg, pkgtype in depcheck([…]).items():
        print('{0}: found in {1}'.format(pkg, types[pkgtype])
        if pkgtype == 2: #AUR
            #build pkg here

:Former data:
    2.0 Returns: no -1

Performs a dependency check.  Data normally provided by
:meth:`prepare_deps()`.

Upgrade
=======

.. index:: Upgrade; Update; Syu
.. versionadded:: 2.1.0.0
.. class:: Upgrade

This is the class for upgrading the installed packages.  It defines one base
method and two additional ones.

.. method:: auto_upgrade()
.. index:: upgrade

:Arguments: none.
:Input: user interaction.
:Output: text.
:Returns: 0 or nothing.
:Exceptions: none.
:Message codes: none.

Upgrades packages.  Simillar to :meth:`Build.auto_build()`.

.. method:: gather_foreign_packages()
.. index:: foreign packages

:Arguments: none.
:Input: none.
:Output: none.
:Returns: foreign packages.
:Exceptions: none.
:Message codes: none.

Gathers a list of all foreign packages.

.. method:: list_upgradeable(pkglist)

:Arguments: a package list.
:Input:
    a list of packages to be compared.

    suggestion: self.gather_foreign_pkgs().keys()
:Output: none.
:Returns: upgradeable packages.
:Exceptions: none.
:Message codes: none.

Compares package versions and returns upgradeable ones.
