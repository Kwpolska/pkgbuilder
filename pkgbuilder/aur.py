#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.99.5.0
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

    multiinfo is implemented in another function, :meth:`multiinfo()`.
    """

    rpc = '{0}://aur.archlinux.org/rpc.php?type={1}&arg={2}'
    mrpc = '{0}://aur.archlinux.org/rpc.php?type=multiinfo{1}'

    def jsonreq(self, rtype, arg, prot='https'):
        """Makes a request and returns plain JSON data."""
        if arg == []:
            return '[]'  # No need to bother, string for JSON.

        try:
            req = requests.get(self.rpc.format(prot, rtype, arg))
            req.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(e.args[0].reason, e)
        except requests.exceptions.HTTPError as e:
            raise HTTPError(req, e)
        except requests.exceptions.RequestException as e:
            raise NetworkError(str(e), e)

        return req.text

    def jsonmultiinfo(self, args, prot='https'):
        """Makes a multiinfo request and returns plain JSON data."""
        if args == []:
            return '[]'  # No need to bother, string for JSON.

        urlargs = '&arg[]=' + '&arg[]='.join(args)
        try:
            req = requests.get(self.mrpc.format(prot, urlargs))
            req.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(e.args[0].reason, e)
        except requests.exceptions.HTTPError as e:
            raise HTTPError(req, origexception=e)
        except requests.exceptions.RequestException as e:
            raise NetworkError(str(e), e)

        return req.text

    def request(self, rtype, arg, prot='https'):
        """Makes a request and returns the AURDict."""
        return json.loads(self.jsonreq(rtype, arg, prot))

    def multiinfo(self, args, prot='https'):
        """Makes a multiinfo request and returns the AURDict."""
        return json.loads(self.jsonmultiinfo(args, prot))
