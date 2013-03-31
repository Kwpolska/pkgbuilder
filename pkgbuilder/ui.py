#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.99.6.0
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
from contextlib import contextmanager

__all__ = ['UI']


class UI(object):
    """The User Interface."""
    pcount = 0
    pcur = 0
    throb = False
    _tt = None

    def pmsg(self, msg, single=False):
        """Print a progress message."""
        self.pcur += 1
        sys.stdout.write('\r')
        ln = len(str(self.pcount))
        sys.stdout.write(('({0:>' + str(ln) + '}/{1}) ').format(self.pcur,
                                                                self.pcount))
        sys.stdout.write('{0:<70}'.format(msg))
        sys.stdout.write('\r')
        if single:
            print()
        if self.pcur == self.pcount:
            self.pcount = 0
            self.pcur = 0
            if not single:
                print()

    def _throbber(self, msg, finalthrob='*', printback=True):
        """Display a throbber."""
        self.throb = True
        while self.throb:
            for i in ('|', '/', '-', '\\'):
                sys.stdout.write('\r({0}) {1}'.format(i, msg))
                time.sleep(0.1)
        if not self.throb and printback:
            sys.stdout.write('\r({0}) {1}'.format(finalthrob, msg))
            time.sleep(0.1)
            print()

    @contextmanager
    def throbber(self, msg, finalthrob='*', printback=True):
        """Run the throbber in a thread."""
        self._tt = threading.Thread(target=self._throbber, args=(
            msg, finalthrob, printback))
        self._tt.start()
        try:
            yield
        finally:
            self.throb = False
            while self.throbber_alive:
                time.sleep(0.1)

    @property
    def throbber_alive(self):
        """Check the status of a throbber."""
        if self._tt:
            return self._tt.is_alive()
        else:
            return False
