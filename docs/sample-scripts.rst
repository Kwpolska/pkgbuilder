=========================
PKGBUILDer Sample Scripts
=========================
:Author: Kwpolska
:Copyright: © 2011-2012, Kwpolska.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2012-10-31
:Version: 2.1.5.8

.. index:: sample scripts

PKGBUILDer, since version 2.1.5.0, includes some sample scripts that are
utilizing it as a library.  Currently included:

 * ``aur-ood-orphans`` — lists the locally installed packages that are marked as
   “out-of-date” or are orphans in the AUR.  (Mind using the results to get
   something done about those packages?  Thanks in advance, from everyone in
   this univ^H^H^H^Hcommunity.)
 * ``list-non-aur`` — lists packages that don’t exist in any sync repo nor the
   AUR.
 * ``upgrade`` — lists or shows the count of possible AUR upgrades.  For use
   eg. in conky.  ``-h``/``--help`` for details.
