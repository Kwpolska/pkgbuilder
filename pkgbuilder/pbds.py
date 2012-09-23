#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.5
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2012, Kwpolska.
# See /LICENSE for licensing information.

# Names convention: pkg = a package object, pkgname = a package name.

"""
    pkgbuilder.PBDS
    ~~~~~~~~~~~~~~~
    PKGBUILDer Data Storage.

    :Copyright: © 2011-2012, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import _, __version__
import sys
import os
import logging


### PBDS           PB global data storage  ###
class PBDS():
    """PKGBUILDer Data Storage."""
    # For fancy-schmancy messages stolen from makepkg.
    colors = {
        'all_off':    '\x1b[1;0m',
        'bold':       '\x1b[1;1m',
        'blue':       '\x1b[1;1m\x1b[1;34m',
        'green':      '\x1b[1;1m\x1b[1;32m',
        'red':        '\x1b[1;1m\x1b[1;31m',
        'yellow':     '\x1b[1;1m\x1b[1;33m'
    }


    pacman = False
    validate = True
    depcheck = True
    pkginst = True
    protocol = 'http'
    categories = ['ERROR', 'none', 'daemons', 'devel', 'editors',
                  'emulators', 'games', 'gnome', 'i18n', 'kde',
                  'lib', 'modules', 'multimedia', 'network',
                  'office', 'science', 'system', 'x11',
                  'xfce', 'kernels']
    inttext = _('Aborted by user! Exiting...')

    ### STUFF NOT TO BE CHANGED BY HUMAN BEINGS.  EVER.
    mp1 = '=='
    mp2 = '  '
    debug = False
    console = None

    if os.getenv('PACMAN') is None:
        paccommand = 'pacman'
    else:
        paccommand = os.getenv('PACMAN')

    if os.path.exists('/usr/bin/sudo'):
        hassudo = True
    else:
        hassudo = False

    # Creating the configuration/log stuff...
    confhome = os.getenv('XDG_CONFIG_HOME')
    if confhome is None:
        confhome = os.path.expanduser('~/.config/')

    kwdir = os.path.join(confhome, 'kwpolska')
    confdir = os.path.join(kwdir, 'pkgbuilder')

    if not os.path.exists(confhome):
        os.mkdir(confhome)

    if not os.path.exists(kwdir):
        os.mkdir(kwdir)

    if not os.path.exists(confdir):
        os.mkdir(confdir)

    if not os.path.exists(confdir):
        print(' '.join(_('ERROR:'), _('Cannot create the configuration '
                                      'directory.')))
        print(' '.join(_('WARNING:'), _('Logs will not be created.')))

    logging.basicConfig(format='%(asctime)-15s [%(levelname)-7s] '
                        ':%(name)-10s: %(message)s',
                        filename=os.path.join(confdir, 'pkgbuilder.log'),
                        level=logging.DEBUG)
    log = logging.getLogger('pkgbuilder')
    log.info('*** PKGBUILDer v' + __version__)

    def debugmode(self, nochange=False):
        """Print all the logged messages to stderr."""
        if not self.debug:
            self.console = logging.StreamHandler()
            self.console.setLevel(logging.DEBUG)
            self.console.setFormatter(logging.Formatter('[%(levelname)-7s] '
                                      ':%(name)-10s: %(message)s'))
            logging.getLogger('').addHandler(self.console)
            self.debug = True
            self.mp1 = 'pb'
            self.mp2 = 'pb'
        elif self.debug and nochange:
            pass
        else:
            logging.getLogger('').removeHandler(self.console)
            self.debug = False
            self.mp1 = '=='
            self.mp2 = '  '

    def colorson(self):
        """Colors on."""
        self.colors = {
            'all_off':    '\x1b[1;0m',
            'bold':       '\x1b[1;1m',
            'blue':       '\x1b[1;1m\x1b[1;34m',
            'green':      '\x1b[1;1m\x1b[1;32m',
            'red':        '\x1b[1;1m\x1b[1;31m',
            'yellow':     '\x1b[1;1m\x1b[1;33m'
        }

    def colorsoff(self):
        """Colors off."""
        self.colors = {
            'all_off':    '',
            'bold':       '',
            'blue':       '',
            'green':      '',
            'red':        '',
            'yellow':     ''
        }

    def fancy_msg(self, text):
        """makepkg's msg().  Use for main messages."""
        sys.stderr.write(self.colors['green'] + self.mp1 + '>' +
                         self.colors['all_off'] +
                         self.colors['bold'] + ' ' + text +
                         self.colors['all_off'] + '\n')
        self.log.info('(auto fancy_msg     ) ' + text)

    def fancy_msg2(self, text):
        """makepkg's msg2().  Use for sub-messages."""
        sys.stderr.write(self.colors['blue'] + self.mp2 + '->' +
                         self.colors['all_off'] +
                         self.colors['bold'] + ' ' + text +
                         self.colors['all_off'] + '\n')
        self.log.info('(auto fancy_msg2    ) ' + text)

    def fancy_warning(self, text):
        """makepkg's warning().  Use when you have problems."""
        sys.stderr.write(self.colors['yellow'] + self.mp1 + '> ' +
                         _('WARNING:') + self.colors['all_off'] +
                         self.colors['bold'] + ' ' + text +
                         self.colors['all_off'] + '\n')
        self.log.warning('(auto fancy_warning ) ' + text)

    def fancy_warning2(self, text):
        """Like fancy_warning, but looks like a sub-message (fancy_msg2)."""
        sys.stderr.write(self.colors['yellow'] + self.mp2 + '->' +
                         self.colors['all_off'] + self.colors['bold'] + ' ' +
                         text + self.colors['all_off'] + '\n')
        self.log.warning('(auto fancy_warning2) ' + text)

    def fancy_error(self, text):
        """makepkg's error().  Use for errors.  Quitting is suggested."""
        sys.stderr.write(self.colors['red'] + self.mp1 + '> ' + _('ERROR:') +
                         self.colors['all_off'] + self.colors['bold'] + ' ' +
                         text + self.colors['all_off'] + '\n')
        self.log.error('(auto fancy_error   ) ' + text)

    def fancy_error2(self, text):
        """Like fancy_error, but looks like a sub-message (fancy_msg2)."""
        sys.stderr.write(self.colors['red'] + self.mp2 + '->' +
                         self.colors['all_off'] + self.colors['bold'] + ' ' +
                         text + self.colors['all_off'] + '\n')
        self.log.error('(auto fancy_error2  ) ' + text)
