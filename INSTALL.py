#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# PKGBUILDer installer
# Copyright (C) 2011-2012, Kwpolska.
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

# There are no install instructions.  If you want to install
# the script, run this script with python.

"""PKGBUILDer AUR installer.
Use it if you don't have any AUR helpers installed."""

import subprocess
import os
import json
import urllib.request
import tarfile
import random
import gettext


def depcheck():
    """Dependency check."""

    print(_("""Performing a dependency check..."""))

    deps = {'pyalpm': None,
            'certifi': None, 'requests': None}

    print("""pyalpm    | extra     | """, end='')
    try:
        import pyalpm
        deps['pyalpm'] = True
        print(_('found'))
    except ImportError:
        deps['pyalpm'] = False
        print(_('not found'))

    print("""certifi   | AUR       | """, end='')
    try:
        import certifi
        deps['certifi'] = True
        print(_('found'))
    except ImportError:
        deps['certifi'] = False
        print(_('not found'))

    print("""requests  | AUR       | """, end='')
    try:
        import requests
        deps['requests'] = True
        print(_('found'))
    except ImportError:
        deps['requests'] = False
        print(_('not found'))

    return deps


def install(pkgname):
    """Cheap installation function."""
    PKGDATA = json.loads(urllib.request.urlopen('http://aur.archlinux\
.org/rpc.php?type=info&arg=' + pkgname).read().decode())
    RHANDLE = urllib.request.urlopen('http://aur.archlinux.org' +
                                     PKGDATA['results']['URLPath'])
    open(pkgname + '.tar.gz', 'wb').write(RHANDLE.read())
    THANDLE = tarfile.open(pkgname + '.tar.gz', 'r:gz')
    THANDLE.extractall()
    os.chdir('./' + pkgname + '/')

    ASROOT = ''
    if os.geteuid() == 0:
        ASROOT = ' --asroot'
    MPKG = subprocess.call('/usr/bin/makepkg -si' + ASROOT, shell=True)

    if MPKG == 1:
        print(_("""

Something went wrong.  Please read makepkg's output and try again.
You can also try to debug the work of this script yourself.
All the files this script was working on are placed in
    {}
(the number is random).

If I am wrong, though, congratulations!
""").format(PATH))

if __name__ == '__main__':
    try:

        T = gettext.translation('pkgbuilder', 'locale', fallback='en')
        _ = T.gettext
        PATH = ''

        print(_("""Hello!

PKGBUILDer is now available as an AUR package.  It is the suggested
way of installing PKGBUILDer.  This script will download the AUR
package and install it.  If you will have problems, please download
and compile the package manually.

"""))

        WHOCARES = input(_('Hit Enter/Return to continue. '))
        print('')

        UID = os.geteuid()
        PATH = '/tmp/pkgbuilderinstall-{}'.format(random.randint(1, 100))
        if os.path.exists(PATH) is False:
            os.mkdir(PATH)
        os.chdir(PATH)

        deps = depcheck()

        if deps['certifi'] is False or deps['requests'] is False:
            print(_("""Installing missing AUR dependencies..."""))
            if deps['certifi'] is False:
                install('python-certifi')

            if deps['requests'] is False:
                install('python-requests')

        install('pkgbuilder')

        print(_("""

Read the above output.  If the script had any problems, run it
again.  You can also try to debug the work of this script yourself.
All the files this script was working on are placed in
    {}
(the number is random).

If everything went fine, though, congratulations!  You can now use
PKGBUILDer.  For standalone usage, type `pkgbuilder` into the prompt
(zsh users: hash -r, other shells may need another command).  For
python module usage, type `import pkgbuilder` into the python prompt.
""").format(PATH))

    except KeyboardInterrupt:
        if PATH == '':
            print(_("""It looks like you want to quit.  Okay then, goodbye.
No work has been started yet.

If that's what you want to do, go for it.  If it isn't, run this
script again."""))
        else:
            print(_("""It looks like you want to quit.  Okay then, goodbye.
All the files this script was working on are placed in
    {}
(the number is random).

If that's what you want to do, go for it.  If it isn't, run this
script again.""").format(PATH))
