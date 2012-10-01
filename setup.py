#!/usr/bin/python3
###############################################################################
#
# Copyright 2011 by CipherHealth, LLC
#
###############################################################################
"""Setup
"""
from setuptools import setup, find_packages
from distutils.core import setup, Command
import unittest

class RunTests(Command):
    """New setup.py command to run all tests for the package.
    """
    description = "run all tests for the package"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        tests = unittest.TestLoader().discover('src')
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(tests)

def get_version():
    initfname = 'src/ofxstatement/__init__.py'
    v = {}
    exec(compile(open(initfname).read(), initfname, 'exec'),
         globals(), v)
    return v['__version__']

with open('README.rst') as f:
    long_description = f.read()

setup(
      name='ofxstatement',
      version=get_version(),
      author = "Andrey Lebedev",
      author_email = "andrey@lebedev.lt",
      url = "https://github.com/kedder/ofxstatement",
      description = ("Tool to convert proprietary bank statement to "
                     "OFX format, suitable for importing to GnuCash"),
      long_description = long_description,
      license = "GPLv3",
      keywords = ["ofx", "banking", "statement"],
      cmdclass={'test': RunTests},
      classifiers = [
                     'Development Status :: 3 - Alpha',
                     'Programming Language :: Python :: 3',
                     'Natural Language :: English',
                     'Topic :: Office/Business :: Financial :: Accounting',
                     'Topic :: Utilities',
                     'Environment :: Console',
                     'Operating System :: OS Independent',
                     'License :: OSI Approved :: GNU Affero General Public License v3'
                     ],
      packages = find_packages('src'),
      entry_points = {'console_scripts':
                      ['ofxstatement = ofxstatement.tool:run']},
      package_dir = {'':'src'},
      install_requires = [
                          'setuptools',
                          'appdirs'
                          ],
      include_package_data = True,
      zip_safe = True
      )
