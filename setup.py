#!/usr/bin/env python3
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import codecs

setup(name='pkgbuilder',
      version='3.1.12',
      description='An AUR helper (and library) in Python 3.',
      keywords='arch pkgbuild',
      author='Chris “Kwpolska” Warrick',
      author_email='kwpolska@kwpolska.tk',
      url='https://github.com/Kwpolska/pkgbuilder',
      license='3-clause BSD',
      long_description=codecs.open('./docs/README.rst', 'r', 'utf-8').read(),
      platforms='Arch Linux',
      zip_safe=False,
      test_suite='tests',
      classifiers=['Development Status :: 6 - Mature',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.1',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: System',
                   'Topic :: System :: Archiving :: Packaging',
                   'Topic :: Utilities'],
      packages=['pkgbuilder'],
      requires=['pyalpm', 'requests'],
      scripts=['bin/pkgbuilder', 'bin/pb'],
      data_files=[('share/man/man8', ['docs/pkgbuilder.8.gz']),
                  ('share/man/man8', ['docs/pb.8.gz']),
                  ('share/locale/pl/LC_MESSAGES', ['locale/pl/LC_MESSAGES/'
                                                   'pkgbuilder.mo']),
                  ('share/locale/ja/LC_MESSAGES', ['locale/ja/LC_MESSAGES/'
                                                   'pkgbuilder.mo'])])
