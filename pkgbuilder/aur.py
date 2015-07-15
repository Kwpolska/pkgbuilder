#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v4.0.3
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2015, Chris Warrick.
# See /LICENSE for licensing information.

"""
Call the AUR API.

:Copyright: © 2011-2015, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import pkgbuilder
from pkgbuilder.exceptions import ConnectionError, HTTPError, NetworkError
import requests
import requests.exceptions
import json

__all__ = ('AUR',)


class AUR(object):

    """
    Call the AUR API.

    Valid request types for :meth:`request()` (and
    :meth:`jsonrequest()`):

    +---------+-----------------------------------+
    + name    | purpose                           |
    +=========+===================================+
    | info    | get info about `arg`              |
    +---------+-----------------------------------+
    | search  | search for `arg` in the AUR       |
    +---------+-----------------------------------+
    | msearch | show packages maintained by `arg` |
    +---------+-----------------------------------+

    A more accurate list might be available at the AUR RPC website:
    https://aur.archlinux.org/rpc.php

    multiinfo is implemented in another function, :meth:`multiinfo()`.

    .. note:: Most people don’t actually want this and will prefer to use
              ``pkgbuilder.utils.{info,search,msearch}()`` instead.
    """

    # FIXME: make this 'aur.archlinux.org' on 2015-08-08
    base = 'https://aur4.archlinux.org'
    base_changed = False  # FIXME: drop base changing framework on 2015-08-08
    rpcver = 4
    _rpc = '/rpc.php?v='
    emptystr = '{"version":%s,"type":"%s","resultcount":0,"results":[]}'
    ua = 'PKGBUILDer/' + pkgbuilder.__version__

    @property
    def rpc(self):
        """Return the RPC URL."""
        return self.base + self._rpc + str(self.rpcver)

    def jsonreq(self, rtype, arg):
        """Make a request and returns plain JSON data."""
        if arg == []:
            # No need to bother.
            return self.emptystr % (self.rpcver, rtype)

        try:
            req = requests.get(self.rpc, params={'type': rtype, 'arg': arg},
                               headers={'User-Agent': self.ua})
            req.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            # FIXME: drop base changing framework on 2015-08-08
            if self.base_changed:
                raise ConnectionError(e.args[0].args[0], e)
            else:
                self.base = 'https://aur.archlinux.org'
                self.base_changed = True
                o = self.jsonreq(rtype, arg)
                print("WARNING: AUR base URL changed to aur.archlinux.org.")
                print("         Please update PKGBUILDer or report an "
                      "issue if there is no new version available.")
                return o
        except requests.exceptions.HTTPError as e:
            raise HTTPError(req, e)
        except requests.exceptions.RequestException as e:
            raise NetworkError(str(e), e)

        return req.text

    def jsonmultiinfo(self, args):
        """Make a multiinfo request and returns plain JSON data."""
        if args == []:
            # No need to bother.
            return self.emptystr % (self.rpcver, 'multiinfo')

        try:
            req = requests.get(self.rpc,
                               params={'type': 'multiinfo', 'arg[]': args},
                               headers={'User-Agent': self.ua})
            req.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            # FIXME: drop base changing framework on 2015-08-08
            if self.base_changed:
                raise ConnectionError(e.args[0].args[0], e)
            else:
                self.base = 'https://aur.archlinux.org'
                self.base_changed = True
                o = self.jsonmultiinfo(args)
                print("WARNING: AUR base URL changed to aur.archlinux.org.")
                print("         Please update PKGBUILDer or report an "
                      "issue if there is no new version available.")
                return o
        except requests.exceptions.HTTPError as e:
            raise HTTPError(req, e)
        except requests.exceptions.RequestException as e:
            raise NetworkError(str(e), e)

        return req.text

    def request(self, rtype, arg):
        """Make a request and returns the AURDict."""
        return json.loads(self.jsonreq(rtype, arg))

    def multiinfo(self, args):
        """Make a multiinfo request and returns the AURDict."""
        return json.loads(self.jsonmultiinfo(args))
