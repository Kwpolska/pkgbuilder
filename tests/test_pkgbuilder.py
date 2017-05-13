#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer test suite
# Copyright © 2011-2017, Chris Warrick.
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
import pkgbuilder.__main__
import pkgbuilder.aur
import pkgbuilder.build
import pkgbuilder.pbds
import pkgbuilder.upgrade
import pkgbuilder.utils
import pkgbuilder.wrapper


class TestPB(unittest.TestCase):
    maxDiff = None
    # It’s cheaper to use existing package data.
    fpkg = pkgbuilder.package.AURPackage.from_aurdict({
        'Description': 'A Python AUR helper/library.', 'CategoryID': 16, 'ID':
        52542, 'Maintainer': 'Kwpolska',
        'Depends': ['python', 'pyalpm>=0.5.1-1', 'python-requests', 'asp'],
        'URLPath': '/packages/pk/pkgbuilder/pkgbuilder.tar.gz', 'Version':
        '3.2.0-1', 'PackageBase': 'pkgbuilder', 'FirstSubmitted': 1316529993,
        'OutOfDate': 1000, 'NumVotes': 19, 'Name': 'pkgbuilderts', 'LastModified':
        1395757472, 'URL': 'https://github.com/Kwpolska/pkgbuilder', 'License':
        ['BSD'], 'Popularity': 7, 'Keywords': ['foo', 'bar']})

    def setUp(self):
        """Start stuff."""
        pkgbuilder.DS._pycreload()
        #self.patches = [mock.patch('pkgbuilder.aur.AUR.request', self._aurinforequest)]
        #for p in self.patches:
            #p.start()

    #def tearDown(self):
        #for p in self.patches:
            #p.stop()

    def test_aur(self):
        pkgbuilder.aur.AUR()

    def test_pbds(self):
        pkgbuilder.pbds.PBDS()

    def test_pbds_logging(self):
        pbds = pkgbuilder.pbds.PBDS()
        pbds.log.debug('PB unittest/TestPB is running now on this machine.')

    def test_utils_print_package_search(self):
        sample = ('aur/pkgbuilderts 3.2.0-1 (19 votes) '
                  '\x1b[1;1m\x1b[1;31m[out of date]\x1b[1;0m\n'
                  '    A Python AUR helper/library.')

        req = pkgbuilder.utils.print_package_search(self.fpkg, True)
        self.assertEqual(req, sample)

    def test_utils_print_package_info(self):
        sample = ('Repository     : aur\n'
                  'Name           : pkgbuilderts\n'
                  'Package Base   : pkgbuilder\n'
                  'Version        : 3.2.0-1\n'
                  'URL            : https://github.com/Kwpolska/pkgbuilder\n'
                  'Licenses       : BSD\n'
                  'Groups         : None\n'
                  'Provides       : None\n'
                  'Depends On     : python  pyalpm>=0.5.1-1  python-requests  asp\n'
                  'Make Deps      : None\n'
                  'Check Deps     : None\n'
                  'Optional Deps  : None\n'
                  'Conflicts With : None\n'
                  'Replaces       : None\n'
                  'Votes          : 19\n'
                  'Popularity     : 7\n'
                  'Out of Date    : \x1b[1;1m\x1b[1;31myes\x1b[1;0m\n'
                  'Maintainer     : Kwpolska\nFirst Submitted: '
                  '2011-09-20T14:46:33Z\nLast Updated   : '
                  '2014-03-25T14:24:32Z\nDescription    : '
                  'A Python AUR helper/library.\n'
                  'Keywords       : foo  bar\n')

        req = pkgbuilder.utils.print_package_info([self.fpkg], True)
        self.assertEqual(req, sample)

    def test_main(self):
        # Can’t test too much here…
        pkgbuilder.__main__.main([])

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
