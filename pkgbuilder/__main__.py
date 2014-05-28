#!/usr/bin/env python3
"""Run PKGBUILDer or PBWrapper."""
import sys
if sys.version_info[0] < 3:
    print('ERROR: RUNNING PY2K INSTEAD OF PY3K.')
    print('If you replaced /usr/bin/python with python2, you are an idiot.')
    print('Please revert that change.')
    exit(1)

import pkgbuilder
import pkgbuilder.main
import pkgbuilder.wrapper

def pkgbuildermain():
    try:
        pkgbuilder.main.main()
    except KeyboardInterrupt:
        pkgbuilder.DS.fancy_error(pkgbuilder.DS.inttext)
        exit(0)

def pbwrappermain():
    try:
        pkgbuilder.wrapper.wrapper()
    except KeyboardInterrupt:
        print(pkgbuilder.DS.wrapperinttext + '\n') # for safety.
        exit(0)

if __name__ == '__main__':
    pkgbuildermain()
