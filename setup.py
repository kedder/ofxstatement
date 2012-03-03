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
    version='0.1.0-dev',
    author = "Andrey Lebedev",
    author_email = "andrey@lebedev.lt",
    description = "Proprietary bank statement to OFX converter",
    license = "GPL",
    keywords = "ofx banking statement",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent'],
    packages = find_packages('src'),
    package_dir = {'':'src'},
    ),
    install_requires = [
        'setuptools',
    ],
    include_package_data = True,
    zip_safe = True
    )
