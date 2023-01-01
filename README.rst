=====================================================
PKGBUILDer.  An AUR helper (and library) in Python 3.
=====================================================
:Info: This is the README file for PKGBUILDer.
:Author: Chris Warrick <chris@chriswarrick.com>
:Date: 2021-08-30
:Version: 4.3.1

.. index: README

PURPOSE
-------
Building and installing AUR packages.

INSTALLATION
------------

There are two ways to install PKGBUILDer:

1. Get it from the AUR: https://aur.archlinux.org/packages/pkgbuilder/
2. Add the PKGBUILDer unofficial repository: https://wiki.archlinux.org/index.php/Unofficial_user_repositories#pkgbuilder

After adding the repository, you need to run::

    # pacman-key -r 5EAAEA16
    # pacman-key --lsign 5EAAEA16
    # pacman -Syyu

BASIC USAGE
-----------

``pkgbuilder`` is a command-line application.  It takes various options and
package names as arguments.  The following options are needed for basic usage:

* ``-S`` to work in /tmp instead of the current directory
* ``-F`` to fetch packages instead of installing them
* ``-s`` to search for packages in the AUR
* ``-i`` to get info about an AUR package
* ``-u`` to upgrade all AUR packages on your system

PKGBUILDer also comes with ``pb``, a wrapper that works with both pacman and
the AUR.

For more information, refer to the ``-h`` command, the ``pkgbuilder(8)`` man
page, or the online documentation at https://pkgbuilder.readthedocs.org/.

CONFIGURATION
-------------

PKGBUILDer supports per-user configuration, in the file
~/.config/kwpolska/pkgbuilder/pkgbuilder.ini.  It can also be configured on a
per-usage basis via command-line arguments.

SECURITY AND EDITING PKGBUILDs
------------------------------

By default, PKGBUILDer strives to be the no-questions-asked package manager.
This means that all packages are built immediately, without any confirmations.
The behavior can be overridden with the ``--edit-pkgbuild`` command-line
option, or with ``edit=pkgbuild=true`` in PKGBUILDer’s config file.

COPYRIGHT
---------
Copyright © 2011-2023, Chris Warrick.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions, and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions, and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of the author of this software nor the names of
   contributors to this software may be used to endorse or promote
   products derived from this software without specific prior written
   consent.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
