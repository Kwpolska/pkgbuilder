===========================================
Appendix A. PKGBUILDer message numbers list
===========================================
:Info: This is an appendix to the PKGBUILDer documentation.
:Author: Kwpolska <kwpolska@kwpolska.tk>
:Date: 2011-10-14
:Version: 2.1.2.1

In order to help debugging, messages are numbered.
Each message number has four digits:  the first one is the
category and the other three are error identifiers.

Categories
==========

1. AUR class
2. Utils class
3. Build class
    1. download, extract
    2. depcheck, predepcheck
    3. makepkg
    4. auto_build, validation
4. Update class
5. non-module problems

Usage instructions
------------------

In order to get the category identifier, you need to:

 * multiply the desired list element by 1000
 * multiply the desired subelement (if any) by 100
 * add the results together

In order to get the first possible number of this (sub)category, add 1 to
the result of the above calculations.

Informations
============

======== =============== =========================================
INF#     Component       Message
======== =============== =========================================
[3450]_  validation      installed
======== =============== =========================================

.. [3450] occurs, when PKGBUILDer finds out that the package that
   was meant to be bulit is correctly installed.

Warnings
========

======== =============== =========================================
INF#     Component       Message
======== =============== =========================================
0        none            Nothing there yet.
======== =============== =========================================


Errors
======

======== =============== =========================================
ERR#     Component       Message
======== =============== =========================================
[3001]_  build_runner    package not found
[3101]_  download        0 bytes downloaded
[3151]_  extract         0 files extracted
[3201]_  depcheck        cannot find the requested dependency
[3202]_  depcheck        UnicodeDecodeError while reading file
[3301]_  makepkg         returned 1
[3401]_  auto_build      AUR dependency required
[3451]_  validation      not installed
[3452]_  validation      outdated
[5002]_  search          search string too short
======== =============== =========================================

Explainations:

.. [3001] occurs, when PKGBUILDer cannot find the requested package.
   The name is probably mispelled or the package was deleted.

.. [3101] occurs, when PKGBUILDer downloaded 0 bytes.  It usually
   means that something bad happened during the download.

.. [3151] occurs, when PKGBUILDer extracted 0 files from the
   downloaded tarball.  It means that the tarball is broken.  Please
   tell the maintainer about this problem.

.. [3201] occurs, when the $depends or $makedepends array of the
   PKGBUILD requests a package, that does not exist in the system,
   repositories, nor the AUR.

.. [3202] occurs, when Python cannot decode UTF-8 the PKGBUILD.  If
   the PKGBUILD cannot be read, dependency checks cannot be performed.
   Possible reasons include incorrectly encoded characters in the
   Maintainer/Submitter field.  Please inform the package maintainer
   through the comments.  Include the output of `iconv PKGBUILD`. Example
   output: `# Maintainer: Juan Piconv: illegal input sequence at position
   20` The PKGBUILDer's error message is also valid and will help the
   maintainer.

.. [3301] occurs, when makepkg exits with the return code 1.  It means
   that something bad happened.  Refer to makepkg's output for more info.

.. [3401] occurs, when the $depends or $makedepends array of the
   PKGBUILD request a package, which exists in the AUR.  It is plain
   informational. Right after displaying this message, the script will
   automatically build the required packages.

.. [3451] occurs, when PKGBUILDer finds out that the package is not
   installed on your system.  It means that the package that was bulit
   before this message was issued wasn't installed properly (eg. root
   password wasn't provided at the right time, 'n' was hit when pacman was
   asking for proceeding).

.. [3452] occurs, when PKGBUILDer finds out that the package is
   installed, but outdated.  It means that the package that was bulit before
   this message was issued wasn't installed properly (eg. root password
   wasn't provided at the right time, 'n' was hit when pacman was asking for
   proceeding).

.. [5002] occurs, when your search string is shorter than 3 letters.
   The AUR API ignores these requests.  However, the script searches for
   an exact match.  If one is found, it is being shown.
