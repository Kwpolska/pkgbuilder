#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='pkgbuilder',
      version='2.1.5.13',
      description='An AUR helper (and library) in Python 3.',
      author='Kwpolska',
      author_email='kwpolska@kwpolska.tk',
      url='https://github.com/Kwpolska/pkgbuilder',
      license='3-clause BSD',
      long_description=open('./docs/README.rst').read(),
      platforms='Arch Linux',
      classifiers=['Development Status :: 6 - Mature',
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
                   'Topic :: Utilities'],
      packages=['pkgbuilder'],
      requires=['pyalpm', 'requests'],
      scripts=['bin/pkgbuilder', 'bin/pb'],
      data_files=[('share/man/man8', ['docs/pkgbuilder.8.gz']),
                  ('share/man/man8', ['docs/pb.8.gz']),
                  ('share/locale/en/LC_MESSAGES', ['locale/en/LC_MESSAGES/'
                                                   'pkgbuilder.mo']),
                  ('share/locale/pl/LC_MESSAGES', ['locale/pl/LC_MESSAGES/'
                                                   'pkgbuilder.mo']),
                  ('share/locale/ja/LC_MESSAGES', ['locale/ja/LC_MESSAGES/'
                                                   'pkgbuilder.mo'])])
