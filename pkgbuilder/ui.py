#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v3.5.1
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2015, Chris Warrick.
# See /LICENSE for licensing information.

"""
The User Interface.

:Copyright: © 2011-2015, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import sys
import time
import threading

__all__ = ('Progress', 'Throbber', 'ProgressThrobber')


class Progress(object):
    """A static progress indicator with numbers.

    Usage::

        pm = Progress(total=2)
        pm.msg('Doing step 1...')
        step1()
        pm.msg('Doing step 2...')
        step2()
    """
    current = 0
    total = 1
    _pml = 0

    def __init__(self, total=1):
        """Initialize a Progress message."""
        self.total = total

    def msg(self, msg, single=False):
        """Print a progress message."""
        self.current += 1
        ln = len(str(self.total))
        sys.stdout.write('\r' + ((ln * 2 + 4 + self._pml) * ' '))
        self._pml = len(msg)
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write(('({0:>' + str(ln) + '}/{1}) ').format(self.current,
                                                                self.total))
        sys.stdout.write(msg)
        sys.stdout.write('\r')
        sys.stdout.flush()
        if single:
            print()
        if self.current == self.total:
            self.total = 0
            self.current = 0


class Throbber(object):
    """A nice animated throbber.

    Usage::

        with Throbber('Doing important stuff...'):
            dostuff()
    """
    throb = False
    states = ('|', '/', '-', '\\')
    _tt = None

    def __init__(self, msg, finalthrob='*', printback=True):
        """Initialize."""
        self.msg = msg
        self.finalthrob = finalthrob
        self.printback = printback

    def __enter__(self):
        """Run the throbber in a thread."""
        self._tt = threading.Thread(target=self._throb, args=(
            self.msg, self.finalthrob, self.printback))
        self._tt.start()
        return self

    def __exit__(self, *args, **kwargs):
        """Clean stuff up."""
        self.throb = False
        while self.throbber_alive:
            time.sleep(0.1)

    def _throb(self, msg, finalthrob='*', printback=True):
        """Display a throbber."""
        self.throb = True
        i = 0
        while self.throb:
            sys.stdout.write('\r({0}) {1}'.format(self.states[i], self.msg))
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
            if i == len(self.states):
                i = 0
        if not self.throb and self.printback:
            sys.stdout.write('\r({0}) {1}'.format(self.finalthrob, self.msg))
            sys.stdout.flush()
            time.sleep(0.1)
            print()

    @property
    def throbber_alive(self):
        """Check the status of a throbber."""
        if self._tt:
            return self._tt.is_alive()
        else:
            return False


class ProgressThrobber(Progress, Throbber):
    """An animated progress throbber.

    Similar to Progress, but the / is animated.

    Usage::

        with ProgressThrobber('Working...', total=2) as pt:
            dostuff()
            pt.bump('Cleaning up...')
            cleanup()
    """
    current = 0
    finalthrob = '/'
    printback = True

    def __init__(self, msg, total=1):
        self.total = total
        self.ln = len(str(self.total))
        self.bump(msg)

    def _throb(self, msg, finalthrob='/', printback=True):
        """Display a throbber."""
        self.throb = True
        i = 0
        while self.throb:
            sys.stdout.write(('\r({0:>' + str(self.ln) +
                              '}{1}{2}) {3}').format(self.current,
                                                     self.states[i],
                                                     self.total, self.msg))
            sys.stdout.write('\r')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
            if i == len(self.states):
                i = 0

        sys.stdout.write('\r({0}{1}{2}) {3}'.format(self.current,
                                                    self.finalthrob,
                                                    self.total, self.msg))
        sys.stdout.flush()
        time.sleep(0.1)
        if self.printback:
            print()

    def bump(self, msg):
        sys.stdout.write('\r' + ((self.ln * 2 + 4 + self._pml) * ' '))
        self._pml = len(msg)
        self.current += 1
        self.msg = msg
