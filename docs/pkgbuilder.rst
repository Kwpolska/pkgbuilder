==========
PKGBUILDer
==========

:Author: Kwpolska <kwpolska@kwpolska.tk>
:Copyright: See Appendix B.
:Date: 2012-09-04
:Version: 2.1.4.0
:Manual section: 8
:Manual group: PKGBUILDer manual

SYNOPSIS
========

*pkgbuilder* [-hVcdvwSy] [-P PROTOCOL] [-isu] [PACKAGE [PACKAGE ...]]

DESCRIPTION
===========

PKGBUILDer is an AUR helper, i.e. an application which builds AUR
packages.  It can be used in conjunction with pacman (with a special
script).  It uses various techniques to automatize the process as
much as possible.

Since version 2.1.0, PKGBUILDer provides modules that can be used in
other scripts.

OPERATIONS
==========

**-i, --info**
    Displays info about **PACKAGE** in a fashion similar to pacman.

**-s, --search**
    Searches the AUR for packages with **PACKAGE** as the query.

**-u, --sysupgrade**
    Checks for package updates in the AUR.  If updates are found,
    they will be installed if the user says so.

Additionally, parameters **-S**, **--sync**, **-y** and **-refresh**
are accepted for pacman syntax compatibility. **-S**/**--sync**
makes the script build its packages in /tmp instead of the current
working directory (CWD).

OPTIONS
=======

**-c, --nocolors**
    Forces the script to ignore the ANSI color codes.

**--debug**
    Outputs debug information to stderr.

**-d, --nodepcheck**
    Skips dependency checks.  It may (and, most likely, will)
    break makepkg.

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

(Trashman is an XDG trash manager by Kwpolska, which you should install.)

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
