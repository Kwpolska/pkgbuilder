#!/usr/bin/env python3
from setuptools import setup

setup(name='pkgbuilder',
      version='2.1.2.33',
      description='An AUR helper (and library) in python3',
      author='Kwpolska',
      author_email='kwpolska@kwpolska.tk',
      url='https://github.com/Kwpolska/pkgbuilder',
      license='3-clause BSD',
      long_description='A nice AUR helper (and library) written in Python3.',
      platforms='Arch Linux',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Topic :: System',
                   'Topic :: System :: Archiving :: Packaging',
                   'Topic :: Utilities'
                  ],
      py_modules=['pkgbuilder'],
      requires=['pyparsing', 'pyalpm', 'requests'],
      scripts=['scripts/pkgbuilder'],
      data_files=[
                  ('share/man/man8', ['docs/pkgbuilder.8.gz']),
                  ('share/locale/en/LC_MESSAGES', ['locale/en/LC_MESSAGES/\
pkgbuilder.mo']),
                  ('share/locale/pl/LC_MESSAGES', ['locale/pl/LC_MESSAGES/\
pkgbuilder.mo'])
                 ]
     )
