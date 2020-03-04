#!/usr/bin/python3
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
from distutils.core import setup
import unittest
import sys

version = "0.6.4"

with open("CHANGES.rst") as chlogf, open('README.rst', encoding='utf-8') as rdmef:
    long_description = chlogf.read() + "\n\n" + rdmef.read()

setup(name='ofxstatement',
      version=version,
      author="Andrey Lebedev",
      author_email="andrey@lebedev.lt",
      url="https://github.com/kedder/ofxstatement",
      description=("Tool to convert proprietary bank statement to "
                   "OFX format, suitable for importing to GnuCash"),
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="GPLv3",
      keywords=["ofx", "banking", "statement"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
      packages=find_packages('src'),
      namespace_packages=["ofxstatement", "ofxstatement.plugins"],
      entry_points={
          'console_scripts':
          ['ofxstatement = ofxstatement.tool:run'],
          },
      package_dir={'': 'src'},
      install_requires=['setuptools',
                        'appdirs>=1.3.0'
                        ],
      extras_require={'test': ["mock", "pytest", "pytest-cov"]},
      tests_require=["mock"],
      include_package_data=True,
      zip_safe=True
      )
