#!/usr/bin/python3
# pkgbuilder installer
# Copyright Kwpolska 2011.

# There are no install instructions.  If you want to install
# the script, run this script with python.

"""pkgbuilder AUR installer
experimental and useless"""

import subprocess
import os
import json
import urllib.request
import tarfile
import random
import gettext

try:
    T = gettext.translation('pkgbuilder', 'locale') # for installer
    def _(message):
        """gettext"""
        out = T.lgettext(message)
        return out.decode()


    print(_("""Hello!

PKGBUILDer is now available as an AUR package.  It is the suggested
way of installing PKGBUILDer.  This script will download the AUR
package and install it.  If you will have problems, please download
and compile the package manually.

"""))

    WHOCARES = input(_('Hit Enter/Return to continue. '))
    print('')

    UID = os.geteuid()
    PATH = '/tmp/pkgbuilderinstall-{0}'.format(random.randint(1, 100))
    if os.path.exists(PATH) == False:
        os.mkdir(PATH)
    os.chdir(PATH)


    PKGDATA = json.loads(urllib.request.urlopen('http://aur.archlinux.org\
/rpc.php?type=info&arg=pkgbuilder').read().decode())
    RHANDLE = urllib.request.urlopen('http://aur.archlinux.org'+
    PKGDATA['results']['URLPath'])
    open('pkgbuilder.tar.gz', 'wb').write(RHANDLE.read())
    THANDLE = tarfile.open('pkgbuilder.tar.gz', 'r:gz')
    THANDLE.extractall()
    os.chdir('./pkgbuilder/')

    ASROOT = ''
    if os.geteuid() == 0:
        ASROOT = ' --asroot'
    MPKG = subprocess.call('/usr/bin/makepkg -si'+ASROOT, shell=True)

    if MPKG == 1:
        print(_("""

Something went wrong.  Please read makepkg's output and try again.
You can also try to debug the work of this script yourself.
All the files this script was working on are placed in
    {0}
(the number is random).

If I am wrong, though, congratulations!
""").format(PATH))

    print(_("""

Read the above output.  If the script had any problems, run it
again.  You can also try to debug the work of this script yourself.
All the files this script was working on are placed in
    {0}
(the number is random).

If everything went fine, though, congratulations!  You can now use
PKGBUILDer.  For standalone usage, type `pkgbuilder` into the prompt
(zsh users: hash -r, other shells may need another command).  For
python module usage, type `import pkgbuilder` into the python prompt.
""").format(PATH))

except KeyboardInterrupt:
    print(_("""It looks like you want to quit.  Okay then, goodbye.
All the files this script was working on are placed in
    {0}
(the number is random).

If that's what you want to do, go for it.  If it isn't, run this
script again.""").format(PATH))
