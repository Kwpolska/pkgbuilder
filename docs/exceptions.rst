========================
Exceptions in PKGBUILDer
========================

:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2011-2023, Chris Warrick.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2023-01-30
:Version: 4.3.2

.. index:: Exceptions
.. versionadded:: 3.0.0

Starting with version 3.0.0, the exceptions were split up into multiple ones,
all inheriting from PBException.  All exceptions have two guaranteed
attributes: ``msg``, which is a more-or-less human-friendly message, and
``src``, which explains where the problem came from (string or instance of an
object, depending on the exception — it is clearly visible in the source code).

.. automodule:: pkgbuilder.exceptions
   :members:
