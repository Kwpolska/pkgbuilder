==========
PKGBUILDer
==========

:Subtitle: An AUR helper (and library) in Python 3.
:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2011-2015, Chris Warrick.
:License: BSD (see /LICENSE or Appendix B.)
:Date: 2015-07-13
:Version: 4.0.2
:Manual section: 8
:Manual group: PKGBUILDer manual

SYNOPSIS
========

*pkgbuilder* [-hVcCdDvwSy] [--debug] [--skippgpcheck] [--userfetch USER] [-FisuU] [PACKAGE [PACKAGE ...]]

DESCRIPTION
===========

PKGBUILDer is an AUR helper, i.e. an application which builds AUR
packages.  It can be used in conjunction with pacman (with a special
script).  It uses various techniques to automatize the process as
much as possible.

Since version 2.1.0.0, PKGBUILDer provides modules that can be used in
other scripts.

Since version 2.1.5.6, PKGBUILDer also provides support for ABS packages.
Passing an ABS package name to the ``-S`` option will result in a seamless
detection and build process.

Notice: Running PKGBUILDer and/or PBWrapper as root can deal catastrophic
damage to your system.  Run it as a regular user, you will be prompted for
the root password when one will be required (i.e. to run **pacman**).

OPERATIONS
==========

**-F, --fetch**
    Fetch (and don’t build) **PACKAGE**\s in a fashion similar to
    ``cower -d``.

**--userfetch USER**
    Fetch all AUR packages of an user.

**-y, --refresh**
    A dummy option for pacman syntax compatibility.

**-i, --info**
    Display info about **PACKAGE** in a fashion similar to pacman.

**-s, --search**
    Search the AUR for packages with **PACKAGE** as the query.

**-u, --sysupgrade**
    Check for package updates in the AUR.  If updates are found,
    they will be installed or fetched if the user accepts.  Pass twice to
    downgrade.

**-U, --upgrade**
    Copy pacman packages to the cache and install them.

Additionally, parameters **-S**, **--sync**, **-y** and **-refresh**
are accepted for pacman syntax compatibility. **-S**/**--sync**
makes the script build its packages in /tmp instead of the current
working directory (CWD).

OPTIONS
=======

**-h, --help**
    Show the help message.

**-V, --version**
    Show the version number.

**-c, --clean**
    Clean the build directory after a finished build. (*makepkg -c*)

**-C, --nocolors**
    Force the script to ignore the ANSI color codes.

**--debug**
    Output debug information to stderr.

**-d, --nodepcheck**
    Skip dependency checks.  It may (and, most likely, will)
    break makepkg.

**-D, --vcsupgrade**
    Upgrade all the VCS packages on the system.  Requires **-u**.

**-v, --novalidation**
    Skip package installation validation phase (checking
    if the package is installed).

**-w, --buildonly**
    Skip package installation after building.

**--skippgpcheck**
    Skip PGP checks.

**-S, --sync**
    Build packages in */tmp* and uses *aur* instead of the category in search.

EXAMPLES
========

pkgbuilder hello
    Install the package hello from the AUR.  It will be built in
    the CWD.

pkgbuilder -S hello
    Install hello, but builds the package in /tmp/pkgbuilder-UID.

pkgbuilder -F hello
    Fetch the AUR git repository for hello to the CWD.

pkgbuilder -SF hello
    Like above, but does it in /tmp/pkgbuilder-UID.

pkgbuilder python
    Python is a binary repo package, triggering a ABS download via rsync (no
    need for ``extra/abs``).  -S and/or -F are also accepted.

pkgbuilder -Syu
    Check for updates and offer installing them.

pkgbuilder -uF
    Check for updates and offer fetching them.

hello is a package for GNU Hello: http://www.gnu.org/software/hello/

SEE ALSO
========
**pb(8)**, a wrapper for pacman and PKGBUILDer, included with PKGBUILDer, also
known as PBWrapper.

**pacman(8)**, **makepkg(8)**, **PKGBUILD(5)**

You can visit the git repo at <https://github.com/Kwpolska/pkgbuilder>
for more info.

BUGS
====
Bugs should be reported at the GitHub page
(<https://github.com/Kwpolska/pkgbuilder/issues>).  You can also
send mail to <chris@chriswarrick.com>.
