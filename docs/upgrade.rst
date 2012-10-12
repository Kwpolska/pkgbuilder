==============================
upgrade module (Upgrade class)
==============================

:Author: Kwpolska
:Copyright: © 2011-2012, Kwpolska.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2012-10-12
:Version: 2.1.5.3

.. module:: upgrade

Upgrade
=======

.. index:: Upgrade
.. index:: Update
.. index:: Syu
.. versionadded:: 2.1.0.0
.. class:: Upgrade

This is the class for upgrading the installed packages.  It defines one base
method and two additional ones.

.. method:: auto_upgrade([downgrade][, vcsup])
.. index:: upgrade

Upgrades packages.  Simillar to :meth:`Build.auto_build()`.

.. method:: gather_foreign_packages()
.. index:: foreign packages

Gathers a list of all foreign packages.

.. method:: list_upgradable(pkglist[, vcsup])

.. versionchanged:: 2.1.4.4

Compares package versions and returns upgradable and downgradable ones.
