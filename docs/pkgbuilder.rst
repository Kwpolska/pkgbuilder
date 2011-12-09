==========
PKGBUILDer
==========

:Author: Kwpolska <kwpolska@kwpolska.tk>
:Copyright: See Appendix B.
:Date: 2011-12-09
:Version: 2.1.2.19
:Manual section: 8
:Manual group: PKGBUILDer manual

SYNOPSIS
========

*pkgbuilder* <operation> [options] [targets]

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
    Displays info about **targets** in a fashion similar to pacman.

**-s, --search**
    Searches the AUR for packages with **targets** as the query.

**-u, --sysupgrade**
    Checks for package updates in the AUR.  If updates are found,
    they will be installed if the user says so.

Additionally, parameters **-S**, **--sync**, **-y** and **-refresh**
are accepted for pacman syntax compatibility. **-S**/**--sync**
makes the script build its packages in /tmp instead of the current
working directory (CWD).

OPTIONS
=======

**-C, --nocolor**
    Forces the script to ignore the ANSI color codes.

**-V, --novalidation**
    Skips package installation validation phase (checking
    if the package is installed).

**-S, --sync**
    Originally for pacman syntax compatibility, now makes the script more
    wrapper-friendly: builds packages in */tmp* and uses *aur* instead of
    the category in search.

EXAMPLES
========

pkgbuilder dropbox
    Installs the package "dropbox" from the AUR.  It is being built in
    the CWD.

pkgbuilder -S dropbox
    Installs "dropbox", but builds thhe package in /tmp-pkgbuilder-UID.

pkgbuilder -Syu
    Checks for updates and offers installing them.

SEE ALSO
========
**pacman(8)**, **makepkg(8)**

You can visit the git repo at <https://github.com/Kwpolska/pkgbuilder>
for more info.

BUGS
====
Bugs shall be reported at the GitHub page
(<https://github.com/Kwpolska/pkgbuilder/issues>).  You can also
send mail to <kwpolska@kwpolska.tk>.
