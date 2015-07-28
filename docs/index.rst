PKGBUILDer.  An AUR helper (and library) in Python 3.
=====================================================


.. note::
    This documentation is compatible with version |release| of
    PKGBUILDer.
    The current version on your system can be checked by running
    ``pkgbuilder -v``.

.. note::
    The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”,
    “SHOULD”, “SHOULD NOT”, “RECOMMENDED”,  “MAY”, and “OPTIONAL” in this
    document are to be interpreted as described in RFC 2119.

PKGBUILDer is an AUR helper, i.e. an application which builds AUR
packages.  It can be used in conjunction with pacman (with a special
script).  It uses various techniques to automatize the process as
much as possible.

Since version 2.1.0, PKGBUILDer provides modules that can be used in
other scripts.

For standalone use, see the :doc:`PKGBUILDer man page <pkgbuilder>`.
Reading the :doc:`README <README>` is also a good idea.

For the PBWrapper (``pb``), see the :doc:`PBWrapper man page <pb>`.

For developers using PKGBUILDer as a Python module, see the respective class
documents.

User Documentation
------------------

By reading those three documents, you will know your way around PKGBUILDer as
an user.

.. toctree::
   :titlesonly:

   PKGBUILDer man page <pkgbuilder>
   PBWrapper man page <pb>
   README for PKGBUILDer <README>

Developer Documentation
-----------------------

Those documents will let a developer do something.  Note that most of them is
auto-generated from the Python source and you are actually better off reading
that.

.. toctree::
   :titlesonly:

   aur
   build
   main
   package
   pbds
   transaction
   ui
   upgrade
   utils
   wrapper
   exceptions
   sample-scripts

Appendices
----------

.. toctree::
   :titlesonly:

   CONTRIBUTING
   LICENSE
   CHANGELOG

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
