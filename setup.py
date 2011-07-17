# -*- coding: utf-8 -*-
# Author: Matías Bordese

from setuptools import setup, find_packages

version = '0.1'

setup(name='nlg4patch',
      version=version,
      description="Software patches verbalization.",
      keywords='nlg unidiff patch verbalization',
      author='Matias Bordese',
      author_email='mbordese@gmail.com',
      url='http://github.com/matiasb/nlg4patch',
      license='GPL-3',
      packages=find_packages(),
      namespace_packages=['nlg4patch']
     )
