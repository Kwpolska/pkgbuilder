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

import os
import json
import requests


class TestPB(unittest.TestCase):
    # PBDS
    def test_pbds(self):
        pbds = pkgbuilder.PBDS()

    def test_pbds_logging(self):
        pbds = pkgbuilder.PBDS()
        pbds.log.debug('PB unittest/TestPB is running now on this machine.')

    # AUR
    def test_aur(self):
        aur = pkgbuilder.AUR()

    def test_aur_exact(self):
        aur = pkgbuilder.AUR()
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
        aur = pkgbuilder.AUR()
        req = aur.request('info', 'pkgbuilder', 'http')
        if req['results']['Maintainer'] != 'Kwpolska':
            raise Exception('test_aur_contents: Kwpolska isn’t \
the maintainer of PKGBUILDer')

        if req['results']['Name'] != 'pkgbuilder':
            raise Exception('test_aur_contents: AUR is terribly broken, \
“pkgbuilder” isn’t the name of package “pkgbuilder”')

    # Utils
    def test_utils(self):
        utils = pkgbuilder.Utils()

    def test_utils_info(self):
        utils = pkgbuilder.Utils()
        req = utils.info('pkgbuilder')
        if req['Maintainer'] != 'Kwpolska':
            raise Exception('test_utils_info: Kwpolska isn’t \
the maintainer of PKGBUILDer')

        if req['Name'] != 'pkgbuilder':
            raise Exception('test_utils_info: AUR is terribly broken, \
“pkgbuilder” isn’t the name of package “pkgbuilder”')

    def test_utils_search(self):
        utils = pkgbuilder.Utils()
        req = utils.search('pkgbuilder')
        if req[0]['Maintainer'] != 'Kwpolska':
            raise Exception('test_utils_search: Kwpolska isn’t \
the maintainer of PKGBUILDer')

        if req[0]['Name'] != 'pkgbuilder':
            raise Exception('test_utils_search: AUR is terribly broken, \
“pkgbuilder” isn’t the name of package “pkgbuilder”')

    def test_utils_print_package(self):
        utils = pkgbuilder.Utils()
        # It’s cheaper to use existing package data.
        fpkg = {'CategoryID': '16',
                'Description': 'A basic Python AUR helper/library.',
                'FirstSubmitted': '1316529993',
                'ID': '52542',
                'LastModified': 'two universes ago',
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
    A basic Python AUR helper/library."""

        req = utils.print_package(fpkg, True, True)

        if req != sample:
            raise Exception('test_utils_print_package: output doesn’t \
match the example')

    # Build
    def test_build(self):
        build = pkgbuilder.Build()

    def test_build_download(self):
        build = pkgbuilder.Build()
        req = build.download('/packages/pk/pkgbuilder/pkgbuilder.tar.gz',
                             '/dev/null')
        if req == 0:
            raise Exception('test_build_download: the file is empty, \
            and the error handling in the actual script ignored that.')

    def test_build_extract(self):
        os.chdir('/tmp')
        build = pkgbuilder.Build()
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

    # Upgrade
    def test_upgrade(self):
        upgrade = pkgbuilder.Upgrade()
        # Cannot test too much here.

if __name__ == '__main__':
    unittest.main()
