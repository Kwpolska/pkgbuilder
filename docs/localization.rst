==============================
Appendix A. Localization Guide
==============================
:Author: Kwpolska
:Copyright: © 2011-2012, Kwpolska.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2012-10-06
:Version: 2.1.5.1

.. index:: locale

Hello!  It looks like you want to localize PKGBUILDer.  Great!  Doing so is not
so hard, and requires just a few minutes.

1. Fork the repo on GitHub and clone your fork locally.
2. Run ``mkdir -p locale/[CODE]/LC_MESSAGES`` in your terminal, replacing
   ``[CODE]`` by your language code, as in /usr/share/locale.
3. Copy the ``/messages.pot`` file to
   ``locale/[CODE]/LC_MESSAGES/pkgbuilder.po``.
4. Do your work.  The comments will inform you where this string is, and the
   ones starting with 'TRANSLATORS:' are for you to read and make use of.
   Other comments come from my code and you shouldn’t care about them.  And
   if it is directed for translators, let me know.  The Poedit_ app may be
   of help.  Please take care of the headers at the top of the file (with a
   text editor, do not use poedit for that!)  and modify them.  The
   Last-Translator, Language-Team and Language are important, the others are
   auto-generated anyways.
5. Commit (with the ``-s/--signoff`` flag!) and hit *Pull Request* on GitHub.
6. Your translation will be added in the next release, or, if a release isn’t
   planned in the near future, a new release will be made.  Your addition will
   be appreciated.  Note that I cannot translate new strings, and, as a result,
   I might ask you for additions in the future.

.. _Poedit: http://www.poedit.net/
