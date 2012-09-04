======================
aur module (AUR class)
======================
:Author: Kwpolska
:Copyright: See Appendix B.
:Date: 2012-09-04
:Version: 2.1.4.0

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

:Arguments: request type, argument (package name), protocol.
:Input: none.
:Output: none.
:Returns: Data from the API.
:Exceptions: requests.exceptions.*, PBError.
:Message codes: ERR1001.

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

:Arguments: a list of packages, protocol.
:Input: none.
:Output: none.
:Returns: Data from the API.
:Exceptions: requests.exceptions.*, PBError.
:Message codes: ERR1001.

Makes a multiinfo request.  A multiinfo request can retrieve information
for multiple packages.

.. method:: jsonreq(rtype, arg[, prot])

:Arguments: request type, argument (package name), protocol.
:Input: none.
:Output: none.
:Returns: JSON data from the API.
:Exceptions: requests.exceptions.*, PBError.
:Message codes: ERR1001.


Makes a :meth:`request()`, but returns plain JSON data.  Valid values of
`rtype` are listed in :meth:`request()`'s documentation.

.. method:: jsonmultiinfo(args[, prot])

:Arguments: a list of packages, protocol.
:Input: none.
:Output: none.
:Returns: JSON data from the API.
:Exceptions: requests.exceptions.*, PBError.
:Message codes: ERR1001.

Makes a :meth:`multiinfo()` request, but returns plain JSON data.
