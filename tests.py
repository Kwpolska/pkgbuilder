#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer test suite
# Copyright (C) 2012, Kwpolska.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the author of this software nor the names of
#    contributors to this software may be used to endorse or promote
#    products derived from this software without specific prior written
#    consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest
import pkgbuilder
import pkgbuilder.aur
import pkgbuilder.build
import pkgbuilder.pbds
import pkgbuilder.upgrade
import pkgbuilder.utils
import pkgbuilder.wrapper
import os
import requests


class TestPB(unittest.TestCase):
    maxDiff = None
    def test_aur(self):
        pkgbuilder.aur.AUR()

    def test_aur_request(self):
        aur = pkgbuilder.aur.AUR()
        self.pbreq = aur.request('info', 'pkgbuilder', 'http')
        self.assertEqual(self.pbreq['results']['Maintainer'], 'Kwpolska')
        self.assertEqual(self.pbreq['results']['Name'], 'pkgbuilder')

    def test_build_download(self):
        self.assertNotEqual(pkgbuilder.build.download(
                         '/packages/pk/pkgbuilder/pkgbuilder.tar.gz',
                         '/dev/null'), 0)

    def test_build_extract(self):
        os.chdir('/tmp')
        r = requests.get('http://kwpolska.github.com/pub/pb-testsuite.tar.gz')
        with open('/tmp/pb-testsuite.tar.gz', 'wb') as f:
            f.write(r.content)

        req = pkgbuilder.build.extract('/tmp/pb-testsuite.tar.gz')
        self.assertEqual(req, 2)
        with open('/tmp/pb-testsuite/testsuite', 'r') as f:
            sanitycheck = f.read().strip()

        self.assertEqual(sanitycheck, '26313240')

    def test_pbds(self):
        pkgbuilder.pbds.PBDS()

    def test_pbds_logging(self):
        pbds = pkgbuilder.pbds.PBDS()
        pbds.log.debug('PB unittest/TestPB is running now on this machine.')

    def test_utils_info(self):
        self.pbpkg = pkgbuilder.utils.info(['pkgbuilder'])[0]
        self.assertTrue(self.pbpkg.human, 'Kwpolska')
        self.assertTrue(self.pbpkg.name, 'pkgbuilder')

    def test_utils_print_package_search(self):
        # It’s cheaper to use existing package data.
        fpkg = {'CategoryID': 16,
                'Description': 'A Python AUR helper/library.',
                'FirstSubmitted': 1316529993,
                'ID': 52542,
                'LastModified': 4294967294,
                'License': 'BSD',
                'Maintainer': 'Kwpolska',
                'Name': 'pkgbuilder-is-awesome',
                'NumVotes': 8897,  # brought to you by random.org
                'OutOfDate': 1,
                'URL': 'https://github.com/Kwpolska/pkgbuilder',
                'URLPath': '/packages/pk/pkgbuilder/pkgbuilder.tar.gz',
                'Version': 'testsuite'}

        sample = """system/pkgbuilder-is-awesome testsuite (8897 votes) \
\x1b[1;1m\x1b[1;31m[out of date]\x1b[1;0m
    A Python AUR helper/library."""

        fpkg = pkgbuilder.package.AURPackage.from_aurdict(fpkg)
        req = pkgbuilder.utils.print_package_search(fpkg, True, True)
        self.assertEqual(req, sample)

    def test_utils_print_package_info(self):
        # It’s cheaper to use existing package data.
        fpkg = {'CategoryID': 16,
                'Description': 'A Python AUR helper/library.',
                'FirstSubmitted': 1316529993,
                'ID': 52542,
                'LastModified': 4294967294,
                'License': 'BSD',
                'Maintainer': 'Kwpolska',
                'Name': 'pkgbuilder-is-awesome',
                'NumVotes': 8897,  # brought to you by random.org
                'OutOfDate': 1,
                'URL': 'https://github.com/Kwpolska/pkgbuilder',
                'URLPath': '/packages/pk/pkgbuilder/pkgbuilder.tar.gz',
                'Version': 'testsuite'}

        sample = """Repository     : aur
Category       : system
Name           : pkgbuilder-is-awesome
Version        : testsuite
URL            : https://github.com/Kwpolska/pkgbuilder
Licenses       : BSD
Votes          : 8897
Out of Date    : \x1b[1;1m\x1b[1;31myes\x1b[1;0m
Maintainer     : Kwpolska
First Submitted: 2011-09-20T14:46:33Z
Last Updated   : 2106-02-07T06:28:14Z
Description    : A Python AUR helper/library.
"""
        fpkg = pkgbuilder.package.AURPackage.from_aurdict(fpkg)
        req = pkgbuilder.utils.print_package_info([fpkg], True)
        self.assertEqual(req, sample)

    def test_main(self):
        # Can’t test too much here…
        pkgbuilder.main.main([])

    def test_wrapper(self):
        # …or there…
        pkgbuilder.wrapper.wrapper(['unittests', 'UTshibboleet'])

    def test_pb_help(self):
        """Make sure ``pb --help`` works"""
        import sys
        from io import StringIO
        capture = StringIO()
        stdout = sys.stdout
        try:
            sys.stdout = capture
            pkgbuilder.wrapper.wrapper('--help')
        finally:
            sys.stdout = stdout

        # More interested in if the above erred rather than the actual output
        self.assertTrue(capture.getvalue())

    def test_call_pacman(self):
        """Make sure ``pb`` command can call pacman"""

        pacman = pkgbuilder.DS.paccommand
        try:
            pkgbuilder.DS.paccommand = 'true'
            pkgbuilder.wrapper.wrapper(['-Qh'])
        finally:
            pkgbuilder.DS.paccommand = pacman


if __name__ == '__main__':
    unittest.main()
