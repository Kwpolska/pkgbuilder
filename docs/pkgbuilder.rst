==========
PKGBUILDer
==========

:Subtitle: An AUR helper (and library) in Python 3.
:Author: Kwpolska <kwpolska@kwpolska.tk>
:Copyright: © 2011-2013, Kwpolska.
:License: BSD (see /LICENSE or Appendix B.)
:Date: 2013-09-02
:Version: 3.1.7
:Manual section: 8
:Manual group: PKGBUILDer manual

SYNOPSIS
========

*pkgbuilder* [-hVcCdDvwSy] [--debug] [--safeupgrade] [-Fisu] [PACKAGE [PACKAGE ...]]

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

**-i, --info**
    Displays info about **PACKAGE** in a fashion similar to pacman.

**-s, --search**
    Searches the AUR for packages with **PACKAGE** as the query.

**-u, --sysupgrade**
    Checks for package updates in the AUR.  If updates are found,
    they will be installed if the user says so.  Pass twice to downgrade.

Additionally, parameters **-S**, **--sync**, **-y** and **-refresh**
are accepted for pacman syntax compatibility. **-S**/**--sync**
makes the script build its packages in /tmp instead of the current
working directory (CWD).

OPTIONS
=======

**-h, --help**
    Shows the help message.

**-v, --version**
    Shows the version number.

**-c, --clean**
    Cleans the build directory after a finished build. (*makepkg -c*)

**-C, --nocolors**
    Forces the script to ignore the ANSI color codes.

**--debug**
    Outputs debug information to stderr.

**-d, --nodepcheck**
    Skips dependency checks.  It may (and, most likely, will)
    break makepkg.

**-D, --vcsupgrade**
    Upgrades all the VCS packages on the system.  Requires **-u**.

**-v, --novalidation**
    Skips package installation validation phase (checking
    if the package is installed).

**-w, --buildonly**
    Skips package installation after building.

**-S, --sync**
    Builds packages in */tmp* and uses *aur* instead of the category in search.

**--safeupgrade**
    Upgrades PKGBUILDer safely.  Now obsolete, because an update for PKGBUILDer
    forces this option anyways.

**-y, --refresh**
    A dummy option for pacman syntax compatibility.

EXAMPLES
========

pkgbuilder hello
    Installs the package hello from the AUR.  It is being built in
    the CWD.

pkgbuilder -S hello
    Installs hello, but builds the package in /tmp/pkgbuilder-UID.

pkgbuilder -F hello
    Fetches the tarball for hello to the CWD and unpacks it.

pkgbuilder -SF hello
    Like above, but does it in /tmp/pkgbuilder-UID.

pkgbuilder python
    Python is a binary repo package, triggering a ABS download via rsync (no
    need for ``extra/abs``).  -S and/or -F are also accepted.

pkgbuilder -Syu
    Checks for updates and offers installing them.

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
send mail to <kwpolska@kwpolska.tk>.
