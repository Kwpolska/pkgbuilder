# -*- encoding: utf-8 -*-
# PKGBUILDer v4.2.18
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2018, Chris Warrick.
# See /LICENSE for licensing information.

"""
The User Interface.

:Copyright: © 2011-2018, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import sys
import time
import threading
import textwrap
import shutil

__all__ = ('get_termwidth', 'hanging_indent', 'mlist',
           'Progress', 'Throbber', 'ProgressThrobber')


def get_termwidth(default=None):
    """Get the width of this terminal.

    .. versionadded:: 3.3.0
    .. versionchanged:: 4.2.9
    """
    return shutil.get_terminal_size((default, default)).columns


def hanging_indent(text, intro, termwidth=None, change_spaces=True,
                   introwidth=None):
    """Produce text with a hanging indent.

    .. versionadded:: 3.3.0
    .. versionchanged:: 4.0.0
    """
    if termwidth is None:
        termwidth = get_termwidth(9001)
    if introwidth is None:
        introwidth = len(intro)
    nowrap = intro + text
    if intro:
        wrapv = textwrap.wrap(nowrap, termwidth,
                              break_on_hyphens=False)
    else:
        wrapv = textwrap.wrap(nowrap, termwidth - introwidth,
                              break_on_hyphens=False)
    wrap0 = wrapv[0]
    wraprest = textwrap.wrap('\n'.join(wrapv[1:]), termwidth -
                             introwidth,
                             break_on_hyphens=False)
    if change_spaces:
        wraprest = [i.replace('  ', ' ').replace(' ', '  ') for i
                    in wraprest]
    buf = wrap0
    for i in wraprest:
        buf += '\n' + introwidth * ' ' + i

    return buf


def mlist(items, sep='  ', change_spaces=True, termwidth=None, indentwidth=17):
    """Output a list of strings, complete with a hanging indent.

    .. versionadded:: 3.3.0
    .. versionchanged:: 4.0.0
    """
    if termwidth is None:
        termwidth = get_termwidth(9001)
    if items:
        if sep == '\n':
            buf = [hanging_indent(items[0], '', termwidth, change_spaces,
                                  indentwidth)]
            for i in items[1:]:
                buf.append(hanging_indent(i, indentwidth * ' ', termwidth,
                                          change_spaces))
            return '\n'.join(buf)
        else:
            return hanging_indent(sep.join(items), '', termwidth,
                                  change_spaces, indentwidth)
    else:
        return 'None'


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
            sys.stdout.write('\r({0}) {1}'.format(self.states[i], msg))
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
            if i == len(self.states):
                i = 0
        if not self.throb and printback:
            sys.stdout.write('\r({0}) {1}'.format(finalthrob, msg))
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
        """Initialize a ProgressThrobber message."""
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
        """Change the displayed message."""
        sys.stdout.write('\r' + ((self.ln * 2 + 4 + self._pml) * ' '))
        self._pml = len(msg)
        self.current += 1
        self.msg = msg
