=====================
Appendix C. Changelog
=====================
:Info: This is the changelog for PKGBUILDer.
:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2011-2018, Chris Warrick.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2018-03-18
:Version: 4.2.15

.. index:: CHANGELOG

Versioning scheme
=================
PKGBUILDer uses the following versioning schemes:

3.0.0+
    major.minor.revision

2.99.x.x
    2.99.stage.revision (3.0.0 test versions)

2.1.1.0–2.1.6.3
    generation.major.minor.revision

2.1.0
    generation.major.minor

1.0–2.0
    generation.revision

Where:
 * generation
    1 is the first Perl version, 2 is the Python version (dropped for 3.0.0).
 * major
    basic release number.
 * minor
    sub-release number.
 * revision
    changes that aren’t important enough to be new minor versions.

GitHub holds releases, too
==========================

More information can be found on GitHub in the `releases section <https://github.com/Kwpolska/pkgbuilder/releases>`_.

Version History
===============

4.2.15
    * Avoid crashes if package name contains `+` signs (or other characters not allowed in regular expressions).

4.2.14
    * Fix multiinfo glitch if there are no packages

4.2.13
    * Split multiinfo requests into batches of 150, preventing crashes when the request URL becomes too large (Issue #53)

4.2.12
    * use asp instead of abs/rsync
    * remove some references to ABS
    * **deprecated** ``pkgbuilder.build.rsync`` — use ``pkgbuilder.build.asp_export`` instead.

4.2.11
    * Report missing packages in -F properly (via Issue #52)

4.2.10
    * Fix #50 -- prevent infinite loop when building with -w, --buildonly
      (crashes early and explains why)

4.2.9
    * Add an option to force chdir to a place before building (Issue #45)
    * Support ``--ignore`` for upgrades (Issue #46)
    * Use ``shutil.get_terminal_size()`` instead of ``stty size`` (Issue #47)
    * Fix ABS package builds (Issue #48)
    * Use new PyPI URL scheme in PKGBUILDer’s PKGBUILD

4.2.8
    * Show help message for pb -Sh (Issue #44)

4.2.7
    * Add support for AUR keywords (Issue #43)

4.2.6
    * Fix dependency loop for split packages

4.2.5
    *AUR RPC v5 compatiblity
    * Pacman 5.0 compatiblity

4.2.4
    * Fix “out of date” flag check

4.2.3
    * Translate “Running transaction…” line correctly
    * Support ``--noconfirm`` in -Syu
    * Pull existing git repos instead of cloning new ones or aborting (Issue #36)
    * Display “skipping package” message when exceptions occur
    * Support architecture-specific dependencies (Issue #37)

4.2.2
    * Display a better message if some packages fail to build.

4.2.1
    * Default to empty strings in Packages (Issue #35; thanks @mfussenegger)
    * Fix duplicate --confirm argument in ``pb``

4.2.0
    * Support for config files!
    * Change domain to aur.archlinux.org

4.1.0
    * Add transactions framework — users can retry failed installs; less code duplication
    * Add --noconfirm option
    * Fix issue with git clones by adding explicit clone destination

4.0.3
    * Add ``--deep`` option to create deep clones (especially useful for ``-F`` and ``--userfetch``)

4.0.2
    * Update documentation (man pages, README)
    * Support upgrade-fetch (``-uF``) properly
    * Drop fancy-style upgrade messages (use pacman-style messages only, no matter what mode of operation was used)
    * Add ``git`` to PKGBUILD dependencies

4.0.1
    * Fix ``prepare_deps`` for split PKGBUILDs (take all packages’ data, something makepkg actually does **not** do)

4.0.0
    * Use RPCv4
    * Use git clones instead of source tarballs (#34)
    * Display Popularity field
    * Delete Category field
    * Use ``.SRCINFO` files instead of running PKGBUILDs (via ``python-srcinfo``)
    * Don’t build split packages twice (happened in eg. ``pkgbuilder -Syu``)
    * Run ``sudo true`` before attempting to move files so that ``mv`` failures don’t cause an infinite loop
    * Add ``--skippgpcheck`` option (mirrors makepkg’s)
    * API change: use one ``__main__.py`` file instead of two different files
    * API change: move some UI functions from ``pkgbuilder.utils`` to ``pkgbuilder.ui``
    * API change: cd out of the directory in ``build_runner``

3.5.1
    * Fix AURv4 support (use URLPath)

3.5.0
    AURv4 compatibility and minor bugfixes.

3.4.0
    Pacman v4.2.0 compatibility.

3.3.2
    Various minor fixes.

3.3.1
    * Don’t crash on new RPC fields
    * Add PackageBaseID field (in AUR v3.0.0+1)

3.3.0
    PKGBUILDer is now compatible with AURv3.  Note this is perliminary support, and
    as such, there might still be bugs.

3.2.0
    * Downgrade listings have been fixed (Issue #31)
    * Packages are now moved to /var/cache/pacman/pkg/ and installed from
      there (previously, they were copied and installed from /tmp)

3.1.13
    * Fix packages being built when -i was issued (Issue #29)
    * Fix some instances where PKGBUILDer would quit, even though it shouldn’t (as
      requested while running the main function — internal only)
    * Modify downgrade messages to fit pacman more
    * Update the translations

3.1.12
    Make setup.py work properly and have PKGBUILDer install.

3.1.11
    * Fix AUR/HTTP exceptions reporting. (via Issue #28)

3.1.10
    * Inexistent packages don’t crash badly anymore
    * AUR-dependency-builds do not crash everything either
    * -Syu can work without ``stty size`` working
    * $CARCH is defined for dependency checks (Issue #28)

3.1.9
    Something went wrong last release, and it did not fix what it was supposed to…

3.1.8
    Fixed pkgbuilder -F (broken one version ago)

3.1.7
    AUR v2.3.0 compatiblity (fonts category)

3.1.6
    Added --userfetch.

3.1.5
    Added Vietnamese.

3.1.4
    Fixed a mess.

3.1.3
    Fixes to the safeupgrade; added Italian, Spanish and Turkish.

3.1.2
    Modified timestamp generation in the Package classes.

3.1.1
    A quick bugfix update.

3.1.0
    Added some magic to AUR dependency building.

3.0.1
    A lot of tiny fixes.

    Also known as release *three point oh point **ell***, blame Consolas.

3.0.0
    A new major release, introducing many new wonderful features.

2.99.6.0
    Package classes done.

2.99.5.0
    Exceptions 2.0 fully implemented.

2.99.4.0
    First four stages done.

2.1.6.0–2.1.6.3
    VerbosePkgLists, DS.run_command() and subsequent fixes to the latter

2.1.5.14
    Fixing a quite important bug in the install process

2.1.5.13
    2013!  Oh, and the revision number is 13, too!

2.1.5.11—2.1.5.12
    Fixes to the AUR v2.0 magic.

2.1.5.10
    AUR v2.0 support.

2.1.5.9
    And another issue that I have not noticed, in a tiny change of Update
    behavior.  Sorry for all those updates, but I do not do testing on
    everything, just on stuff I think could break a lot (have you seen a bugfix
    for the ABS build magic?  I haven’t.  Well, the validation fix was
    partially related to the ABS magic, but it was detected during a run of
    ``pb -S`` with an inexistent package that I thought might exist.  I
    actually revised all the changes that happened since 2.1.5.5 (a release
    without those bugs) and I think I’m done with everything now.

2.1.5.8
    A bug in the wrapper fixed.  Sorry, but sometimes I forget to test certain
    things, and I forgot that the protocol choice in PBWrapper is implemented
    through a workaround.  Also, fixed the installation validation behavior.

2.1.5.7
    Fixed some bugs that managed to slip through while working on 2.1.5.6.

2.1.5.6
    Added ABS support.

2.1.5.4—2.1.5.5
    Applying patches from vadmium/pkgbuilder, also adding a few other fixes and
    changing the ``pb`` version number up to 0.2.0.

2.1.5.3
    A bugfix for package copying and installation (signatures were passed to
    ``-U``) broke the installation mechanism so only one package got installed.
    Also, fixing a bug with a STDIN that is not a terminal (eg. ``xargs``, and
    I hope nobody is using it to search for stuff)

2.1.5.2
    Fixed a bug where an error in makepkg while running an Upgrade
    crashed PB and thrown an unhelpful traceback.

2.1.5.1
    More tiny bugfixes.

2.1.5.0
    A release including the sample scripts, among other stuff.  This is a
    release which now has all the functionality I want it to have.  And it’s
    time to move onto a new project, the aurqt interface for the AUR.  Or maybe
    something else? [Update from the future: it wasn’t all I wanted.  Moreover,
    PKGBUILDer is a dependency of aurqt.]

2.1.4.9
    Some more bugfixes.

2.1.4.8
    Introducing a backwards-compatibility-breaking change of
    .utils.Utils.info()

2.1.4.7
    Quite a lot of changes.

2.1.4.5-2.1.4.6
    Fixes some bugs.

2.1.4.4
    The mature release, including downgrades, excluding mess.

2.1.4.2-2.1.4.3
     Bug fixes, thanks to fosskers (from aura, another AUR helper).

2.1.4.1
    Dropped the useless msgcodes, which made no sense at all.

2.1.4.0
    ``pb`` wrapper!

2.1.3.7
    depcheck ignores empty deps now.

2.1.3.2-2.1.3.6
    little, unimportant fixes, for docs and locale and whatnot.

2.1.3.1
    print_package_*

2.1.3.0
    Now divided into modules.

2.1.2.33
    Bugfix release, final release of 2.1.2 series.

2.1.2.32
    Test suite introduced.  (unittests, nosetests were used in the very
          beginning)

2.1.2.31
    The big changes begin.  Introducing requests.

2.1.2.1-2.1.2.30
    Tiny, unimportant bugfixes.  Somehow, my version numbering broke, stuff
    went completely apeshit, and I do not understand it.

2.1.2.0
    Support for the new pyalpm.

2.1.1.8
    Fixed the license.

2.1.1.7
    Some little changes.

2.1.1.6
    Fixed AUR dep detection.  (not released into git.)

2.1.1.5
    Some fixes for locale support.

2.1.1.4
    Locale support!

2.1.1.0-2.1.1.3
    Little changes and refinements.

2.1.0
    First OOP-based release.  Including -Syu, BSD License, our own AUR class,
    documentation, module usage-friendliness.

2.1.0-prerelease
    A prerelease build of 2.1.0.  This one still works with the AUR class by
    Xyne.

2.0
    First release.

1.1
    A more advanced version, never released publicly, and I do not even have
    any backups.  Nobody cares anyways.

1.0
    First and only release.
