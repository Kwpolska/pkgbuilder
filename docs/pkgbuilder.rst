==========
PKGBUILDer
==========

:Subtitle: An AUR helper for humans.
:Author: Kwpolska <kwpolska@kwpolska.tk>
:Copyright: © 2011-2012, Kwpolska.
:License: BSD (see /LICENSE or Appendix B.)
:Date: 2012-10-03
:Version: 2.1.4.9
:Manual section: 8
:Manual group: PKGBUILDer manual

SYNOPSIS
========

*pkgbuilder* [-hVcCdvwSy] [-P PROTOCOL] [-isu] [PACKAGE [PACKAGE ...]]

DESCRIPTION
===========

PKGBUILDer is an AUR helper, i.e. an application which builds AUR
packages.  It can be used in conjunction with pacman (with a special
script).  It uses various techniques to automatize the process as
much as possible.

Since version 2.1.0, PKGBUILDer provides modules that can be used in
other scripts.

Notice: Running PKGBUILDer and/or PBWrapper as root can deal catastrophic
damage to your system.  Run it as a regular user, you will be prompted for
the root password when one will be required (i.e. to run **pacman**).

OPERATIONS
==========

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

**-P PROTOCOL, --protocol PROTOCOL**
    Chooses the protocol, http by default.

**-S, --sync**
    Originally for pacman syntax compatibility, now makes the script more
    wrapper-friendly: builds packages in */tmp* and uses *aur* instead of
    the category in search.

**-y, --refresh**
    A dummy option for pacman syntax compatibility.

EXAMPLES
========

pkgbuilder trashman
    Installs the package "trashman" from the AUR.  It is being built in
    the CWD.

pkgbuilder -S trashman
    Installs "trashman", but builds the package in /tmp-pkgbuilder-UID.

pkgbuilder -Syu
    Checks for updates and offers installing them.

(Trashman is a trash manager by Kwpolska, which you should install ASAP.)

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
