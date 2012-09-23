========================
pbds module (PBDS class)
========================

:Author: Kwpolska
:Copyright: © 2011-2012, Kwpolska.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2012-09-23
:Version: 2.1.4.6

.. module: pbds

PBDS
====

.. index:: PBDS
.. versionadded:: 2.1.0.0
.. class:: PBDS

This is the class used for storing data.  Currently, it stores the following
information (not including information humans should not touch and care about):

+-----------+-----------------------------------------------+---------------+
| variable  | contents/usage                                | default       |
+===========+===============================================+===============+
| colors    | colors currently used in the script           | [colors]_     |
+-----------+-----------------------------------------------+---------------+
| pacman    | using wrapper-friendly behavior? [pacman]_    | False         |
+-----------+-----------------------------------------------+---------------+
| validate  | validating package installation?              | True          |
+-----------+-----------------------------------------------+---------------+
| depcheck  | checking if deps are installed?               | True          |
+-----------+-----------------------------------------------+---------------+
| pkginst   | if makepkg should install packages            | True          |
+-----------+-----------------------------------------------+---------------+
| protocol  | protocol used to connect to the AUR           | http          |
+-----------+-----------------------------------------------+---------------+
| categories| AUR categories list                           | [categories]_ |
+-----------+-----------------------------------------------+---------------+
| inttext   | text shown while interrupting (^C)            | [inttext]_    |
+-----------+-----------------------------------------------+---------------+
| confhome  | configuration home                            | [conf]_       |
+-----------+-----------------------------------------------+---------------+
| kwdir     | directory used by all projects by yours truly | [conf]_       |
+-----------+-----------------------------------------------+---------------+
| confdir   | configuration directory                       | [conf]_       |
+-----------+-----------------------------------------------+---------------+
| log       | logger object (eg. PBDS.log.info)             | logger object |
+-----------+-----------------------------------------------+---------------+

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

.. [categories] The categories come from `aurweb <https://aur.archlinux.org>`_,
    and are as follows:

::

    categories = ['ERROR', 'none', 'daemons', 'devel', 'editors',
                  'emulators', 'games', 'gnome', 'i18n', 'kde',
                  'lib', 'modules', 'multimedia', 'network',
                  'office', 'science', 'system', 'x11',
                  'xfce', 'kernels']

.. [inttext] Used by /scripts/pkgbuilder, internationalized, looks like this:
    ``Aborted by user! Quitting...``

.. [conf] In order: ``~/.config/``, ``~/.config/kwpolska``,
    ``~/.config/kwpolska/pkgbuilder`` (may differ depending on system config)

It also has a few methods:

.. method:: debugmode(nochange)

.. versionadded:: 2.1.4.0

Print all the logged messages to stderr.

.. method:: colorson()

Turns colors on.

.. method:: colorsoff()

Turns colors off.

.. method:: fancy_msg(msg)
.. method:: fancy_msg2(msg)
.. method:: fancy_warning(msg)
.. method:: fancy_warning2(msg)
.. method:: fancy_error(msg)
.. method:: fancy_error2(msg)

``makepkg``’s message functions with PKGBUILDer’s own additions.  Use for displaying messages.
