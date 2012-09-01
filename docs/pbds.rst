========================
pbds module (PBDS class)
========================

:Author: Kwpolska
:Copyright: See Appendix B.
:Date: 2012-08-26
:Version: 2.1.3.7

.. module: pbds

PBDS
====

.. index:: PBDS
.. versionadded:: 2.1.0.0
.. class:: PBDS

This is the class used for storing data.  Currently, it stores this
information:

+-----------+-----------------------------------------------+-------------------+
| variable  | contents/usage                                | default           |
+===========+===============================================+===================+
| colors    | colors currently used in the script           | [colors]_         |
+-----------+-----------------------------------------------+-------------------+
| pacman    | using wrapper-friendly behavior? [pacman]_    | False             |
+-----------+-----------------------------------------------+-------------------+
| validate  | validating package installation?              | True              |
+-----------+-----------------------------------------------+-------------------+
| depcheck  | checking if deps are installed?               | True              |
+-----------+-----------------------------------------------+-------------------+
| mkpkginst | if makepkg should install packages            | True              |
+-----------+-----------------------------------------------+-------------------+
| protocol  | protocol used to connect to the AUR           | http              |
+-----------+-----------------------------------------------+-------------------+
| categories| AUR categories list                           | [categories]_     |
+-----------+-----------------------------------------------+-------------------+
| inttext   | text shown while interrupting (^C)            | [inttext]_        |
+-----------+-----------------------------------------------+-------------------+
| confdir   | configuration directory                       | [confdir]_        |
+-----------+-----------------------------------------------+-------------------+
| log       | logger object (eg. PBDS.log.info)             | logger object     |
+-----------+-----------------------------------------------+-------------------+

.. [colors] Code below.

::

    self.colors = {
        'all_off':    '\x1b[1;0m',
        'bold':       '\x1b[1;1m',
        'blue':       '\x1b[1;1m\x1b[1;34m',
        'green':      '\x1b[1;1m\x1b[1;32m',
        'red':        '\x1b[1;1m\x1b[1;31m',
        'yellow':     '\x1b[1;1m\x1b[1;33m'
    }

.. [pacman] *wrapper-friendly behavior* (-S): building in /tmp;
    :meth:`Utils.print_package` says aur/name

.. [categories] The categories come from `aurweb <https://aur.archlinux.org>`_, and are as follows:

::

    self.categories = ['ERROR', 'none', 'daemons', 'devel', 'editors',
                       'emulators', 'games', 'gnome', 'i18n', 'kde',
                       'lib', 'modules', 'multimedia', 'network',
                       'office', 'science', 'system', 'x11',
                       'xfce', 'kernels']

.. [inttext] Used by /scripts/pkgbuilder, internationalized, looks like this: ``[ERR5001] Aborted by user! Exiting…``

.. [confdir] Config directory.  Usually ``~/.config/kwpolska/pkgbuilder``

It also has a few methods:

.. method:: debugout()

.. versionadded:: 2.1.4.0

:Arguments: none.
:Input: none.
:Output: none.
:Returns: nothing.
:Exceptions: none.
:Message codes: none.

Print all the logged messages to stderr.

.. method:: colorson()

:Arguments: none.
:Input: none.
:Output: none.
:Returns: nothing.
:Exceptions: none.
:Message codes: none.

Turns colors on.

.. method:: colorsoff()

:Arguments: none.
:Input: none.
:Output: none.
:Returns: nothing.
:Exceptions: none.
:Message codes: none.

Turns colors off.

.. method:: fancy_msg()
.. method:: fancy_msg2()
.. method:: fancy_warning()
.. method:: fancy_warning2()
.. method:: fancy_error()
.. method:: fancy_error2()

:Arguments: a message to show.
:Input: none.
:Output: the message.
:Returns: nothing.
:Exceptions: none.
:Message codes: none, although messages may contain some.

``makepkg``’s message functions with PKGBUILDer’s own additions.  Use for displaying messages.
