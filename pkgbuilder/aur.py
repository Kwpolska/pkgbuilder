#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v3.1.0
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2013, Kwpolska.
# See /LICENSE for licensing information.

"""
    pkgbuilder.aur
    ~~~~~~~~~~~~~~

    A class for calling the AUR API.

    :Copyright: © 2011-2013, Kwpolska.
    :License: BSD (see /LICENSE).
"""

#from . import _
from .exceptions import ConnectionError, HTTPError, NetworkError
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

    rpc = 'https://aur.archlinux.org/rpc.php?type={0}&arg={1}'
    mrpc = 'https://aur.archlinux.org/rpc.php?type=multiinfo{0}'

    def jsonreq(self, rtype, arg):
        """Makes a request and returns plain JSON data."""
        if arg == []:
            # No need to bother.  String for JSON.
            return '{"type": "info", "resultcount": 0, "results": []}'

        try:
            req = requests.get(self.rpc.format(rtype, arg))
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
            # No need to bother.  String for JSON.
            return '{"type": "info", "resultcount": 0, "results": []}'

        urlargs = '&arg[]=' + '&arg[]='.join(args)
        try:
            req = requests.get(self.mrpc.format(urlargs))
            req.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(e.args[0].reason, e)
        except requests.exceptions.HTTPError as e:
            raise HTTPError(req, origexception=e)
        except requests.exceptions.RequestException as e:
            raise NetworkError(str(e), e)

        return req.text

    def request(self, rtype, arg):
        """Makes a request and returns the AURDict."""
        return json.loads(self.jsonreq(rtype, arg))

    def multiinfo(self, args):
        """Makes a multiinfo request and returns the AURDict."""
        return json.loads(self.jsonmultiinfo(args))
