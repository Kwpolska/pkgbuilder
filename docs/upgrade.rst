==============================
upgrade module (Upgrade class)
==============================

:Author: Kwpolska
:Copyright: See Appendix B.
:Date: 2012-08-14
:Version: 2.1.3.5

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

.. method:: auto_upgrade()
.. index:: upgrade

:Arguments: none.
:Input: user interaction.
:Output: text.
:Returns: 0 or nothing.
:Exceptions: none.
:Message codes: none.

Upgrades packages.  Simillar to :meth:`Build.auto_build()`.

.. method:: gather_foreign_packages()
.. index:: foreign packages

:Arguments: none.
:Input: none.
:Output: none.
:Returns: foreign packages.
:Exceptions: none.
:Message codes: none.

Gathers a list of all foreign packages.

.. method:: list_upgradeable(pkglist)

:Arguments: a package list.
:Input:
    a list of packages to be compared.

    suggestion: self.gather_foreign_pkgs().keys()
:Output: none.
:Returns: upgradeable packages.
:Exceptions: none.
:Message codes: none.

Compares package versions and returns upgradeable ones.
