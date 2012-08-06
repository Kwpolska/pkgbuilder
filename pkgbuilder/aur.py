#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer v2.1.3.1
# An AUR helper/library.
# Copyright (C) 2011-2012, Kwpolska.
# See /LICENSE for licensing information.

# Names convention: pkg = a package object, pkgname = a package name.

"""
    pkgbuilder.AUR
    ~~~~~~~~~~~~~~
    A class for calling the AUR API.

    :Copyright: (C) 2011-2012, Kwpolska.
    :License: BSD (see /LICENSE).
"""

from . import DS, T, _, PBError
import requests
import json


### AUR             AUR RPC calls           ###
class AUR:
    """A class for calling the AUR API."""

    def __init__(self):
        """AUR init.

:Arguments: none.
:Input: none.
:Output: none.
:Returns: an AUR object.
:Exceptions: none.
:Message codes: none."""
        self.rpc = '{0}://aur.archlinux.org/rpc.php?type={1}&arg={2}'
        self.mrpc = '{0}://aur.archlinux.org/rpc.php?type=multiinfo{1}'

    def jsonreq(self, rtype, arg, prot='http'):
        """Makes a request and returns plain JSON data.

:Arguments: request type, argument (package name), protocol.
:Input: none.
:Output: none.
:Returns: JSON data from the API.
:Exceptions: requests.exceptions.*, PBError.
:Message codes: ERR1001."""
        r = requests.get(self.rpc.format(prot, rtype, arg))
        if r.status_code != 200:
            raise PBError(_('[ERR1001] AUR: HTTP Error {0}').format(
                r.status_code))

        return r.text

    def jsonmultiinfo(self, args, prot='http'):
        """Makes a multiinfo request and returns plain JSON data.

:Arguments: a list of packages, protocol.
:Input: none.
:Output: none.
:Returns: JSON data from the API.
:Exceptions: requests.exceptions.*, PBError.
:Message codes: ERR1001."""
        urlargs = '&arg[]=' + '&arg[]='.join(args)
        r = requests.get(self.mrpc.format(prot, urlargs))
        if r.status_code != 200:
            raise PBError(_('[ERR1001] AUR: HTTP Error {0}').format(
                r.status_code))

        return r.text

    def request(self, rtype, arg, prot='http'):
        """Makes a request.

:Arguments: request type, argument (package name), protocol.
:Input: none.
:Output: none.
:Returns: data from the API.
:Exceptions: requests.exceptions.*, PBError.
:Message codes: ERR1001."""
        return json.loads(self.jsonreq(rtype, arg, prot))

    def multiinfo(self, args, prot='http'):
        """Makes a multiinfo request.

:Arguments: a list of packages, protocol.
:Input: none.
:Output: none.
:Returns: data from the API.
:Exceptions: requests.exceptions.*, PBError.
:Message codes: ERR1001."""

        return json.loads(self.jsonmultiinfo(args, prot))
