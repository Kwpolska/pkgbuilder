=========
PBWrapper
=========

:Author: Kwpolska <kwpolska@kwpolska.tk>
:Copyright: See Appendix B.
:Date: 2012-09-18
:Version: 2.1.4.4
:Wrapper Version: 0.1.1
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

EXAMPLES
========

pb -S python trashman
    Installs the Python interpreter from the repos (which is already on
    your system, especially if you have installed PKGBUILDer/PBWrapper)
    and Trashman from the AUR.

pb -Si python trashman
    Shows information for the python and trashman packages.

pb -Syu
    Checks for repo and AUR updates (in that order) and offers
    installing them.

(Trashman is an XDG trash manager by Kwpolska.  Python is the awesome
language both Trashman and PKGBUILDer/PBWrapper are written in.)

SEE ALSO
========
**pacman(8)**, **pkgbuilder(8)**, **makepkg(8)**, **PKGBUILD(5)**

You can visit the git repo at <https://github.com/Kwpolska/pkgbuilder>
for more info.

BUGS
====
Bugs should be reported at the GitHub page
(<https://github.com/Kwpolska/pkgbuilder/issues>), with the PBWrapper
label.  You can also send mail to <kwpolska@kwpolska.tk>.
