#!/usr/bin/env python3
"""Run PKGBUILDer or PBWrapper."""

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
        print(pkgbuilder.DS.wrapperinttext + '\n')
        exit(0)


if __name__ == '__main__':
    pkgbuildermain()
