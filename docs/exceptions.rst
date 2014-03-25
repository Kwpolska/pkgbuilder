========================
Exceptions in PKGBUILDer
========================

:Author: Chris “Kwpolska” Warrick <kwpolska@kwpolska.tk>
:Copyright: © 2011-2014, Kwpolska.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2014-03-25
:Version: 3.2.0

.. index:: Exceptions
.. versionadded:: 3.0.0

Starting with version 3.0.0, the exceptions were split up into multiple ones,
all inheriting from PBException.  All exceptions have two guaranteed
attributes: ``msg``, which is a more-or-less human-friendly message, and
``src``, which explains where the problem came from (string or instance of an
object, depending on the exception — it is clearly visible in the source code).

.. automodule:: pkgbuilder.exceptions
   :members:
