========================
pbds module (PBDS class)
========================

:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2011-2018, Chris Warrick.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2018-03-18
:Version: 4.2.15

.. module: pbds

PBDS
====

.. index:: PBDS
.. versionadded:: 2.1.0.0
.. class:: PBDS

This is the class used for storing data.  Currently, it stores the following
information (not including information humans should not touch and care about):

+----------------+-----------------------------------------------+-----------------------------------+
| variable       | contents/usage                                | default/acceptable values         |
+================+===============================================+===================================+
| colors         | colors currently used in the script           | [colors]_                         |
+----------------+-----------------------------------------------+-----------------------------------+
| pacman         | using wrapper-friendly behavior? [pacman]_    | False                             |
+----------------+-----------------------------------------------+-----------------------------------+
| validate       | validating package installation?              | True                              |
+----------------+-----------------------------------------------+-----------------------------------+
| depcheck       | checking if deps are installed?               | True                              |
+----------------+-----------------------------------------------+-----------------------------------+
| pkginst        | if makepkg should install packages            | True                              |
+----------------+-----------------------------------------------+-----------------------------------+
| inttext        | text shown while interrupting (^C)            | [inttext]_                        |
+----------------+-----------------------------------------------+-----------------------------------+
| wrapperinttext | text shown while wrapper is interrupting (^C) | [wrapperinttext]_                 |
+----------------+-----------------------------------------------+-----------------------------------+
| paccommand     | Pacman command to use                         | pacman                            |
+----------------+-----------------------------------------------+-----------------------------------+
| hassudo        | If ``sudo`` is present (see :meth:`sudo`)     | (bool)                            |
+----------------+-----------------------------------------------+-----------------------------------+
| uid            | Current UID                                   | ``os.geteuid()``                  |
+----------------+-----------------------------------------------+-----------------------------------+
| confhome       | configuration home                            | ``~/.config/``                    |
+----------------+-----------------------------------------------+-----------------------------------+
| kwdir          | directory used by all projects by yours truly | ``~/.config/kwpolska``            |
+----------------+-----------------------------------------------+-----------------------------------+
| confdir        | configuration directory                       | ``~/.config/kwpolska/pkgbuilder`` |
+----------------+-----------------------------------------------+-----------------------------------+
| log            | logger object (e.g. PBDS.log.info)            | logger object                     |
+----------------+-----------------------------------------------+-----------------------------------+
| ui             | an instance of :class:`pkgbuilder.ui.UI`      | None or :class:`pkgbuilder.ui.UI` |
+----------------+-----------------------------------------------+-----------------------------------+
| pyc            | a pycman instance                             | None or pycman instance           |
+----------------+-----------------------------------------------+-----------------------------------+

.. [colors] Code below.

::


    colors = {
        'all_off':    '\x1b[1;0m',
        'bold':       '\x1b[1;1m',
        'blue':       '\x1b[1;1m\x1b[1;34m',
        'green':      '\x1b[1;1m\x1b[1;32m',
        'red':        '\x1b[1;1m\x1b[1;31m',
        'yellow':     '\x1b[1;1m\x1b[1;33m'
    }

.. [pacman] *wrapper-friendly behavior* (-S): building in /tmp;
    :meth:`Utils.print_package` says aur/name

.. [inttext] Used by /bin/pkgbuilder, internationalized, looks like this:
    ``Aborted by user! Quitting...``

.. [wrapperinttext] Used by /bin/pb, internationalized, looks like this:
    ``Interrupt signal received\n``

.. [conf] In order: ``~/.config/``, ``~/.config/kwpolska``,
    ``~/.config/kwpolska/pkgbuilder`` (may differ depending on system config)

.. automodule:: pkgbuilder.pbds
   :members:
