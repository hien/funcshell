#!/usr/bin/env python

from setuptools import setup

setup(
  name='funcshell',
  version='0.0.1',
  description='A CLI interface to Func',
  long_description='funchshell is a CLI interface to Func.',
  license='MIT',
  platforms='Platform Independent',
  author='Silas Sewell',
  author_email='silas@sewell.ch',
  url='http://code.google.com/p/silassewell/wiki/funcshell',
  download_url='http://silassewell.googlecode.com/files/funcshell-0.0.1.tar.gz',
  packages=['funcshell'],
  entry_points = {
    'console_scripts': [
      'funcshell = funcshell:main',
    ],
  },
)   
