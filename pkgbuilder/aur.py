#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v3.3.1
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2014, Kwpolska.
# See /LICENSE for licensing information.

"""
    pkgbuilder.aur
    ~~~~~~~~~~~~~~

    A class for calling the AUR API.

    :Copyright: © 2011-2014, Kwpolska.
    :License: BSD (see /LICENSE).
"""

import pkgbuilder
from pkgbuilder.exceptions import ConnectionError, HTTPError, NetworkError
import requests
import requests.exceptions
import json

__all__ = ['AUR']


class AUR:
    """A class for calling the AUR API.

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

    rpc = 'https://aur.archlinux.org/rpc.php?v=2'
    emptystr = '{"version":2,"type":"%s","resultcount":0,"results":[]}'
    ua = 'PKGBUILDer/' + pkgbuilder.__version__

    def jsonreq(self, rtype, arg):
        """Makes a request and returns plain JSON data."""
        if arg == []:
            # No need to bother.
            return self.emptystr % rtype

        try:
            req = requests.get(self.rpc, params={'type': rtype, 'arg': arg}, headers={'User-Agent': self.ua})
            req.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(e.args[0].reason, e)
        except requests.exceptions.HTTPError as e:
            raise HTTPError(req, e)
        except requests.exceptions.RequestException as e:
            raise NetworkError(str(e), e)

        return req.text

    def jsonmultiinfo(self, args):
        """Makes a multiinfo request and returns plain JSON data."""
        if args == []:
            # No need to bother.
            return self.emptystr % 'multiinfo'

        try:
            req = requests.get(self.rpc, params={'type': 'multiinfo', 'arg[]':
                                                 args}, headers={'User-Agent': self.ua})
            req.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(e.args[0].reason, e)
        except requests.exceptions.HTTPError as e:
            raise HTTPError(req, e)
        except requests.exceptions.RequestException as e:
            raise NetworkError(str(e), e)

        return req.text

    def request(self, rtype, arg):
        """Makes a request and returns the AURDict."""
        return json.loads(self.jsonreq(rtype, arg))

    def multiinfo(self, args):
        """Makes a multiinfo request and returns the AURDict."""
        return json.loads(self.jsonmultiinfo(args))
