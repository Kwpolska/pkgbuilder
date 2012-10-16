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
import json
import requests


class TestPB(unittest.TestCase):
    # AUR
    def test_aur(self):
        aur = pkgbuilder.aur.AUR()

    def test_aur_exact(self):
        aur = pkgbuilder.aur.AUR()
        jrr = json.loads(aur.jsonreq('info', 'pkgbuilder', 'http'))
        jrs = json.loads(aur.jsonreq('info', 'pkgbuilder', 'https'))
        arr = aur.request('info', 'pkgbuilder', 'http')
        ars = aur.request('info', 'pkgbuilder', 'https')
        if jrr == jrs == arr == ars:
            pass
        else:
            print('\ntest_aur_exact:')
            print('/jrr')
            print(jrr)
            print('/jrs')
            print(jrs)
            print('/arr')
            print(arr)
            print('/ars')
            print(ars)
            raise Exception('test_aur_exact: something doesn’t match, \
see stdout for details')

    def test_aur_request(self):
        aur = pkgbuilder.aur.AUR()
        req = aur.request('info', 'pkgbuilder', 'http')
        if req['results']['Maintainer'] != 'Kwpolska':
            raise Exception('test_aur_contents: Kwpolska isn’t \
the maintainer of PKGBUILDer')

        if req['results']['Name'] != 'pkgbuilder':
            raise Exception('test_aur_contents: AUR is terribly broken, \
“pkgbuilder” isn’t the name of package “pkgbuilder”')

    # Build
    def test_build(self):
        build = pkgbuilder.build.Build()

    def test_build_download(self):
        build = pkgbuilder.build.Build()
        req = build.download('/packages/pk/pkgbuilder/pkgbuilder.tar.gz',
                             '/dev/null')
        if req == 0:
            raise Exception('test_build_download: the file is empty, \
            and the error handling in the actual script ignored that.')

    def test_build_extract(self):
        os.chdir('/tmp')
        build = pkgbuilder.build.Build()
        r = requests.get('http://kwpolska.github.com/pb-testsuite.tar.gz')
        f = open('/tmp/pb-testsuite.tar.gz', 'wb')
        f.write(r.content)
        f.close()
        req = build.extract('/tmp/pb-testsuite.tar.gz')
        if req != 2:
            raise Exception('test_build_extract: need to extract \
exactly 2 files')
        scf = open('/tmp/pb-testsuite/testsuite', 'r')
        sanitycheck = scf.read().strip()
        scf.close()
        if sanitycheck != '26313240':
            raise Exception('test_build_extract: file value test failed, '
                            + sanitycheck + ' vs 26313240')

    # PBDS
    def test_pbds(self):
        pbds = pkgbuilder.pbds.PBDS()

    def test_pbds_logging(self):
        pbds = pkgbuilder.pbds.PBDS()
        pbds.log.debug('PB unittest/TestPB is running now on this machine.')

    # Upgrade
    def test_upgrade(self):
        upgrade = pkgbuilder.upgrade.Upgrade()
        # Cannot test too much here.

    # Utils
    def test_utils(self):
        utils = pkgbuilder.utils.Utils()

    def test_utils_info(self):
        utils = pkgbuilder.utils.Utils()
        req = utils.info(['pkgbuilder'])[0]
        if req['Maintainer'] != 'Kwpolska':
            raise Exception('test_utils_info: Kwpolska isn’t \
the maintainer of PKGBUILDer')

        if req['Name'] != 'pkgbuilder':
            raise Exception('test_utils_info: AUR is terribly broken, \
“pkgbuilder” isn’t the name of package “pkgbuilder”')

    def test_utils_search(self):
        utils = pkgbuilder.utils.Utils()
        req = utils.search('pkgbuilder')
        if req[0]['Maintainer'] != 'Kwpolska':
            raise Exception('test_utils_search: Kwpolska isn’t \
the maintainer of PKGBUILDer')

        if req[0]['Name'] != 'pkgbuilder':
            raise Exception('test_utils_search: AUR is terribly broken, \
“pkgbuilder” isn’t the name of package “pkgbuilder”')

    def test_utils_print_package_search(self):
        utils = pkgbuilder.utils.Utils()
        # It’s cheaper to use existing package data.
        fpkg = {'CategoryID': '16',
                'Description': 'A Python AUR helper/library.',
                'FirstSubmitted': '1316529993',
                'ID': '52542',
                'LastModified': '4294967294',
                'License': 'BSD',
                'Maintainer': 'Kwpolska',
                'Name': 'pkgbuilder-is-awesome',
                'NumVotes': '8897',  # brought to you by random.org
                'OutOfDate': '1',
                'URL': 'https://github.com/Kwpolska/pkgbuilder',
                'URLPath': '/packages/pk/pkgbuilder/pkgbuilder.tar.gz',
                'Version': 'testsuite'}

        sample = """system/pkgbuilder-is-awesome testsuite (8897 votes) \
\x1b[1;1m\x1b[1;31m[out of date]\x1b[1;0m
    A Python AUR helper/library."""

        req = utils.print_package_search(fpkg, True, True)

        if req != sample:
            raise Exception('test_utils_print_package_search: output \
doesn’t match the example')

    def test_utils_print_package_info(self):
        utils = pkgbuilder.utils.Utils()
        # It’s cheaper to use existing package data.
        fpkg = {'CategoryID': '16',
                'Description': 'A Python AUR helper/library.',
                'FirstSubmitted': '1316529993',
                'ID': '52542',
                'LastModified': '4294967294',
                'License': 'BSD',
                'Maintainer': 'Kwpolska',
                'Name': 'pkgbuilder-is-awesome',
                'NumVotes': '8897',  # brought to you by random.org
                'OutOfDate': '1',
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
        req = utils.print_package_info([fpkg], True, True)
        if req != sample:
            raise Exception('test_utils_print_package_info: output \
doesn’t match the example')

    def test_main(self):
        # Can’t test too much here…
        pkgbuilder.main.main([])

    def test_wrapper(self):
        # …or there…
        pkgbuilder.wrapper.wrapper(['unittests', 'UTshibboleet'])
    
    def test_pb_help(self):
        """Make sure "pb --help" works"""
        import sys
        from io import StringIO
        capture = StringIO()
        stdout = sys.stdout
        try:
            sys.stdout = capture
            pkgbuilder.wrapper.wrapper(("--help"))
        finally:
            sys.stdout = stdout
        
        # More interested in if the above erred rather than the actual output
        self.assertTrue(capture.getvalue())
    
    def test_call_pacman(self):
        """Make sure "pb" command can call Pacman"""
        
        pacman = pkgbuilder.DS.paccommand
        try:
            pkgbuilder.DS.paccommand = "true"
            pkgbuilder.wrapper.wrapper(["dummy-pacman-argument"])
        finally:
            pkgbuilder.DS.paccommand = pacman

if __name__ == '__main__':
    unittest.main()
