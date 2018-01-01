#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# List AUR OOD Packages/Orphans Installed
# Part of PKGBUILDer Sample Scripts
# Copyright © 2011-2018, Chris Warrick.
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

"""A script for listing the locally installed AUR packages that are marked as
“out-of-date” or are orphans."""

import pkgbuilder
import pkgbuilder.utils
import pkgbuilder.upgrade
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, epilog='Use both '
                                     'arguments to show data about orphanage '
                                     'status and outdated packages.')
    action = parser.add_argument_group('actions')
    action.add_argument('-m', '--orphans', action='store_true', default=False,
                        dest='orphans', help='show orphans')
    action.add_argument('-o', '--outdated', action='store_true',
                        default=False, dest='ood', help='show outdated '
                        'packages')
    args = parser.parse_args()

    foreign = pkgbuilder.upgrade.gather_foreign_pkgs().keys()
    ood = []
    orphans = []
    toprint = []
    for i in pkgbuilder.utils.info(foreign):
        if not i.human:
            orphans.append(i.name)

        if i.is_outdated:
            ood.append(i.name)

    if args.orphans and args.ood:
        both = list(set(ood + orphans))
        both.sort()
        for i in both:
            entry = ['(']
            if i in orphans:
                entry.append('M')
            else:
                entry.append(' ')

            if i in ood:
                entry.append('O')
            else:
                entry.append(' ')

            entry.append(') ')
            entry.append(i)
            toprint.append(''.join(entry))
    elif args.orphans:
        toprint = orphans
        toprint.sort()
    elif args.ood:
        toprint = ood
        toprint.sort()
    else:
        exit(1)
    print('\n'.join(toprint))
