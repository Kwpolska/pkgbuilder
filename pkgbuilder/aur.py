#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.62.1.4.5
# An AUR helper (and library) in Python 3.
# Copyright © 2011-2012, Kwpolska.
# See /LICENSE for licensing information.

# Names convention: pkg = a package object, pkgname = a package name.

"""
    pkgbuilder.AUR
    ~~~~~~~~~~~~~~
    A class for calling the AUR API.

    :Copyright: © 2011-2012, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import _, PBError
import requests
import json


### AUR             AUR RPC calls           ###
class AUR:
    """A class for calling the AUR API."""

    rpc = '{}://aur.archlinux.org/rpc.php?type={}&arg={}'
    mrpc = '{}://aur.archlinux.org/rpc.php?type=multiinfo{}'

    def jsonreq(self, rtype, arg, prot='http'):
        """Makes a request and returns plain JSON data."""
        req = requests.get(self.rpc.format(prot, rtype, arg))
        if req.status_code != 200:
            raise PBError(_('AUR: HTTP Error {}').format(
                req.status_code))

        return req.text

    def jsonmultiinfo(self, args, prot='http'):
        """Makes a multiinfo request and returns plain JSON data."""
        urlargs = '&arg[]=' + '&arg[]='.join(args)
        req = requests.get(self.mrpc.format(prot, urlargs))
        if req.status_code != 200:
            raise PBError(_('AUR: HTTP Error {}').format(
                req.status_code))

        return req.text

    def request(self, rtype, arg, prot='http'):
        """Makes a request."""
        return json.loads(self.jsonreq(rtype, arg, prot))

    def multiinfo(self, args, prot='http'):
        """Makes a multiinfo request."""
        return json.loads(self.jsonmultiinfo(args, prot))
