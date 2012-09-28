======================
aur module (AUR class)
======================
:Author: Kwpolska
:Copyright: © 2011-2012, Kwpolska.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2012-09-28
:Version: 2.1.4.7

.. module:: aur

AUR
===

.. index:: AUR; RPC
.. index:: RPC
.. versionadded:: 2.1.0.0
.. class:: AUR

This is the class used for calling the AUR API.  It defines four methods:

.. method:: request(rtype, arg[, prot])
.. index:: request

Makes a request and returns data.  Valid types of requests are listed on
the `AUR API's page`_.  Currently tested and working ones are:

+-------------+-----------------------------------+
+ name        | purpose                           |
+=============+===================================+
| info        | get info about `arg`              |
+-------------+-----------------------------------+
| search      | search for `arg` in the AUR       |
+-------------+-----------------------------------+
| maintsearch | show packages maintained by `arg` |
+-------------+-----------------------------------+

multiinfo is implemented in another function, :meth:`multiinfo()`.

.. _`AUR API's page`: http://aur.archlinux.org/rpc.php

.. method:: multiinfo(args[, prot])
.. index:: multiinfo

Makes a multiinfo request.  A multiinfo request can retrieve information
for multiple packages.

.. method:: jsonreq(rtype, arg[, prot])

Makes a :meth:`request()`, but returns plain JSON data.  Valid values of
`rtype` are listed in :meth:`request()`'s documentation.

.. method:: jsonmultiinfo(args[, prot])

Makes a :meth:`multiinfo()` request, but returns plain JSON data.
