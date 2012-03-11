###############################################################################
#
# Copyright 2011 by CipherHealth, LLC
#
###############################################################################
"""Setup
"""
from setuptools import setup, find_packages

setup(
      name='ofxstatement',
      version='0.1.0',
      author = "Andrey Lebedev",
      author_email = "andrey@lebedev.lt",
      url = "https://github.com/kedder/ofxstatement",
      description = ("Tool to convert proprietary bank statement to "
                     "OFX format, suitable for importing to GnuCash"),
      license = "GPL",
      keywords = "ofx banking statement",
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
      entry_points = {'ofxstatement':
                      ['ofxstatement = ofxstatement.tool:run']},
      package_dir = {'':'src'},
      install_requires = [
                          'setuptools',
                          'appdirs'
                          ],
      include_package_data = True,
      zip_safe = True
      )
