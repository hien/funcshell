#!/usr/bin/env python

from distutils.core import setup

setup(
  name='funcshell',
  version='0.0.1',
  description='A CLI interface to Func',
  long_description='funchshell is a CLI interface to Func.',
  license='MIT',
  platforms='Platform Independent',
  author='Silas Sewell',
  author_email='silas@sewell.ch',
  url='http://github.com/silas/funcshell',
  download_url='http://silassewell.googlecode.com/files/funcshell-0.0.1.tar.gz',
  scripts = ['scripts/funcshell'],
  packages=['funcshell'],
)   
