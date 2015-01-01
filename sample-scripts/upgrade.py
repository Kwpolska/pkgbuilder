#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Upgrade Counter and Lister
# Part of PKGBUILDer Sample Scripts
# Copyright © 2011-2015, Chris Warrick.
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

"""A script for listing the possible upgrades for AUR packages."""

import pkgbuilder
import pkgbuilder.upgrade
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Work with AUR upgrades.')
    parser.add_argument('-c', '--count', action='store_true', default=False,
                        dest='count', help='return only the count of '
                        'available upgrades')
    parser.add_argument('-l', '--list', action='store_true', default=False,
                        dest='list', help='list possible upgrades')
    parser.add_argument('-d', '--downgrade', action='store_true',
                        default=False, dest='downgrade',
                        help='include packages that can be downgraded')
    args = parser.parse_args()

    if not args.count and not args.list:
        exit(0)

    foreign = pkgbuilder.upgrade.gather_foreign_pkgs()
    gradable = pkgbuilder.upgrade.list_upgradable(foreign.keys(), False)
    upgradable = gradable[0]
    downgradable = gradable[1]

    if args.downgrade:
        count = len(upgradable) + len(downgradable)
        plist = gradable[0] + gradable[1]
        plist.sort()
    else:
        count = len(upgradable)
        plist = gradable[0]
        plist.sort()

    if args.count:
        print(count)

    if args.list:
        for i in plist:
            print('{} - {} -> {}'.format(i[0], i[1], i[2]))
