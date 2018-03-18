============
Transactions
============

:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2011-2018, Chris Warrick.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2018-03-18
:Version: 4.2.16

.. index:: transaction
.. versionadded:: 4.1.0

To install built packages, PKGBUILDer uses transactions.  A transaction stores:

* package names (as requested by user), used for the validation step
* package file names, moved to pacman cache and installed through ``pacman -U``
* signature file names, moved to pacman cache
* options for running the transaction
* a reference to the transaction file name (if any; ``.tx`` files are autosaved when status changes occur)
* 

.. automodule:: pkgbuilder.transaction
   :members:
