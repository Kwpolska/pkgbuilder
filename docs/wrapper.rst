=========
PBWrapper
=========
:Author: Kwpolska
:Copyright: See Appendix B.
:Date: 2012-09-08
:Version: 2.1.4.2
:PBWrapper Version: 0.1.0

.. index:: wrapper
.. index:: PBWrapper
.. versionadded:: 2.1.4.0
.. module:: wrapper

This is the wrapper for pacman and PKGBUILDer, ``bin/pb``.  It is a complete
mess, but at least it works.  All the arguments it gets are passed to pacman,
unless the operation is -S.  Then, an additional check is made.

For ``-S`` and ``-Si`` requests, the packages are checked, one by one, if they
are in the AUR.  If one is, ``pkgbuilder -Si`` is requested.  If not, all error
handling is left to pacman.

For ``-Ss`` and ``-Syu`` requests, they are passed to both managers, complete
with additional arguments applicable to one or another.

.. note:: Actually, pkgbuilder isn’t called as a subprocess, the arguments are
    just passed to the main() function, so no time is wasted on reloading
    everything.

.. note:: Currently, the -P --protocol argument is not supported.  It will be fixed
    as soon as possible.
