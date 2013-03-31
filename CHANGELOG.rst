=====================
Appendix C. Changelog
=====================
:Info: This is the changelog for PKGBUILDer.
:Author: Kwpolska <kwpolska@kwpolska.tk>
:Copyright: © 2011-2013, Kwpolska.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2013-03-27
:Version: 2.99.5.0

.. index:: CHANGELOG

Versioning scheme
=================
PKGBUILDer uses the following versioning schemes:

:3.0.0: generation.major.minor
:2.99.x.x: 2.99.stage.revision (3.0.0 test versions)
:2.1.1.0–2.1.6.3: generation.major.minor.revision
:2.1.0: generation.major.minor
:1.0–2.0: generation.revision

 * generation: 1 is the first Perl version, 2 is the Python version.
 * major: basic release number.
 * minor: sub-release number.
 * revision: changes that aren’t important enough to be new minor versions.

Generation 3
============

Testing git-only releases
-------------------------

:2.99.6.0: Package classes done.
:2.99.5.0: Exceptions 2.0 fully implemented.
:2.99.4.0: First four stages done.

Generation 2
============
:2.1.6.0–2.1.6.3: VerbosePkgLists, DS.run_command() and subsequent fixes to
                    the latter
:2.1.5.14: Fixing a quite important bug in the install process
:2.1.5.13: 2013!
:2.1.5.11—2.1.5.12: Fixes to the AUR v2.0 magic.
:2.1.5.10: AUR v2.0 support.
:2.1.5.9: And another issue that I have not noticed, in a tiny change of Update
          behavior.  Sorry for all those updates, but I do not do testing on
          everything, just on stuff I think could break a lot (have you seen a
          bugfix for the ABS build magic?  I haven’t.  Well, the validation fix
          was partially related to the ABS magic, but it was detected during a
          run of ``pb -S`` with an inexistent package that I thought might
          exist.  I actually revised all the changed that happened since
          2.1.5.5 (a release without those bugs) and I think I’m done with
          everything now.
:2.1.5.8: A bug in the wrapper fixed.  Sorry, but sometimes I forget to test
          certain things, and I forgot that the protocol choice in PBWrapper
          is implemented through a workaround.  Also, fixed the installation
          validation behavior.
:2.1.5.7: Fixed some bugs that managed to slip through while working on
          2.1.5.6.
;2.1.5.6: Added ABS support.
:2.1.5.4—2.1.5.5: Applying patches from vadmium/pkgbuilder, also adding a few
                  other fixes and changing the ``pb`` version number up to
                  0.2.0.
:2.1.5.3: A bugfix for package copying and installation (signatures were passed
          to -U) broke the installation mechanism so only one package got
          installed.  Also, fixing a bug with a STDIN that is not a terminal
          (eg. ``xargs``, and I hope nobody is using it to search for stuff)
:2.1.5.2: Fixed a bug where an error in makepkg while running an Upgrade
          crashed PB and thrown an unhelpful traceback.
:2.1.5.1: More tiny bugfixes.
:2.1.5.0: A release including the sample scripts, among other stuff.  This is a
          release which now has all the functionality I want it to have.  And
          it’s time to move onto a new project, the aurqt interface for the
          AUR.  Or maybe something else?
:2.1.4.7: Quite a lot of changes.
:2.1.4.5-2.1.4.6: Fixes some bugs.
:2.1.4.4: The mature release, including downrades, excluding mess.
:2.1.4.2-2.1.4.3:  Bug fixes, thanks to fosskers (from aura, another AUR
                   helper).
:2.1.4.1: Dropped the useless msgcodes, which made no sense at all.
:2.1.4.0: ``pb`` wrapper!
:2.1.3.7: depcheck ignores empty deps now.
:2.1.3.2-2.1.3.6: little, unimportant fixes, for docs and locale and whatnot.
:2.1.3.1: print_package_*
:2.1.3.0: Now divided into modules.
:2.1.2.33: Bugfix release, final release of 2.1.2 series.
:2.1.2.32: Test suite introduced.  (unittests, nosetests were used in the very
           beginning)
:2.1.2.31: The big changes begin.  Introducing requests.
:2.1.2.1-2.1.2.30: Tiny, unimportant bugfixes.

                   Somehow, my version numbering broke, and after .5 we got
                   .26.  There was something wrong with the thing, so I upped
                   it to be 26.  It was, of course, supposed to go further and
                   the 2 came over from the minor version.  Crazy.
:2.1.2.0: Support for the new pyalpm.
:2.1.1.8: Fixed the license.
:2.1.1.7: Some little changes.
:2.1.1.6: Fixed AUR dep detection.  (not released into git.)
:2.1.1.5: Some fixes for locale support.
:2.1.1.4: Locale support!
:2.1.1.0-2.1.1.3: Little changes and refinements.
:2.1.0: First OOP-based release.  Including: -Syu, BSD License, own AUR class,
        documentation, module usage-friendliness.
:2.1.0-prerelease: A prerelease build of 2.1.0.  This one still works with the
                   AUR class by Xyne.
:2.0: First release.

Generation 1
============

:1.1: A more advanced version, never released publicly, and I do not even have
      any backups.  Nobody cares anyways.
:1.0: First and only release.
