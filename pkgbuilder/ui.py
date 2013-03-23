#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.1.6.3
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2013, Kwpolska.
# See /LICENSE for licensing information.

"""
    pkgbuilder.ui
    ~~~~~~~~~~~~~

    The User Interface.

    :Copyright: © 2011-2013, Kwpolska.
    :License: BSD (see /LICENSE).
"""

import sys
import time
import threading

__all__ = ['UI']


class UI(object):
    """The User Interface."""
    pcount = 0
    pcur = 0
    throb = False

    def pmsg(self, msg):
        """Print a progress message."""
        self.pcur += 1
        sys.stdout.write('\r')
        ln = len(str(self.pcount))
        sys.stdout.write(('({:>' + str(ln) + '}/{}) ').format(self.pcur,
                                                              self.pcount))
        sys.stdout.write('{:<70}'.format(msg))
        sys.stdout.write('\r')
        if self.pcur == self.pcount:
            self.pcount = 0
            self.pcur = 0
            print()

    def _throbber(self, msg, finalthrob='*', printback=True):
        """Display a throbber."""
        self.throb = True
        while self.throb:
            for i in ('|', '/', '-', '\\'):
                sys.stdout.write('\r({}) {}'.format(i, msg))
                time.sleep(0.1)
        if not self.throb and printback:
            sys.stdout.write('\r({}) {}'.format(finalthrob, msg))
            time.sleep(0.1)
            print()

    def throbber(self, msg, finalthrob='*', printback=True):
        """Run the throbber in a thread."""
        threading.Thread(target=self._throbber, args=(msg, finalthrob,
                                                      printback)).start()
