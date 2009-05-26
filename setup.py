#!/usr/bin/env python

from setuptools import setup

setup(
  name='funcshell',
  version='0.0.1',
  description='A shell interface to Func',
  long_description='funchshell is a shell interface to Func.',
  license='MIT',
  platforms='Platform Independent',
  author='Silas Sewell',
  author_email='silas@sewell.ch',
  url='http://www.silassewell.com/projects/funcshell',
  scripts=['scripts/funcshell'],
  packages=['funcshell', 'funcshell.modules'],
)   
