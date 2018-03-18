=========
PBWrapper
=========

:Subtitle: A wrapper for pacman and PKGBUILDer.
:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2011-2018, Chris Warrick.
:License: BSD (see /LICENSE or Appendix B.)
:Date: 2018-03-18
:Version: 4.2.16
:Wrapper Version: 0.5.3
:Manual section: 8
:Manual group: PKGBUILDer manual

SYNOPSIS
========

*pb* <operation> [options] [targets]

DESCRIPTION
===========

*PBWrapper* (also known as just *pb*) is a wrapper for pacman and
PKGBUILDer, i.e. an application which handles checking if a package is
in the official repos or in the AUR and installs them according to that
information.

It is a part of PKGBUILDer and is included since version 2.1.4.0 of
PKGBUILDer.

Notice: Running PKGBUILDer and/or PBWrapper as root can deal catastrophic
damage to your system.  Run it as a regular user, you will be prompted for
the root password when one will be required (i.e. to run **pacman**).

OPERATIONS AND OPTIONS
======================

All operations and options from pacman and PKGBUILDer work.  Operations
other than **-S, --sync** are passed as-is to pacman.  The **-S,
--sync** switch activates a check for other parameters.  If one of
**-syu** (**--search --refresh --sysupgrade**) is present, the requests
are passed to pacman and PKGBUILDer, in that order, with arguments that
apply to the manager and nothing else.  If any other operations are
present (including **-i, --info**), the **targets** provided are checked
for presence in the AUR.  If a package is in the AUR, it is addded to
the queue that will be passed to PKGBUILDer, otherwise it is added to a
pacman queue.  Please note that brand new options will not work until
the next PKGBUILDer/PBWrapper release.

The **--debug** option enables additional debug information from
PBWrapper.

An additional option is **--unlock**, which unlocks the pacman database.

EXAMPLES
========

pb -S python hello
    Installs the Python interpreter from the repos (which is already on
    your system, especially if you have installed PKGBUILDer/PBWrapper)
    and GNU Hello from the AUR.  Note that, if you used ``pkgbuilder`` instead
    of ``pb``, the Python package would be fetched from ASP (instead of the
    repositories) and built locally.

pb -Si python hello
    Shows information for the python and hello packages.

pb -Syu
    Checks for repo and AUR updates (in that order) and offers
    installing them.

SEE ALSO
========
**pacman(8)**, **pkgbuilder(8)**, **makepkg(8)**, **PKGBUILD(5)**

You can visit the git repo at <https://github.com/Kwpolska/pkgbuilder>
or the documentation at <https://pkgbuilder.readthedocs.org>
for more info.

BUGS
====
Bugs should be reported at the GitHub page (<https://github.com/Kwpolska/pkgbuilder/issues>).
You can also send mail to <chris@chriswarrick.com>.
