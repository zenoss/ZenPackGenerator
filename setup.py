#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#


import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
#def read(fname):
#    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ZenPack Generator",
    version = "0.0.2",
    author = "Zenoss Labs",
    author_email = "labs@zenoss.com",
    description = ("A tool to assist building zenpacks."),
    license = "GPL",
    keywords = "zenpack",
    url = "https://github.com/zenoss/ZenPackGenerator",
    package_dir={'': 'zpg'},
    package_data={'': ['Templates/*.tmpl']},
    install_requires=['Cheetah','PyYaml', 'gitpython', 'inflect', 'Mock'],
    requires=['Cheetah','PyYaml', 'gitpython', 'inflect', 'Mock'],
    entry_points={'console_scripts': ['zpg = zpg.main:main'] },
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Software Development :: Code Generators",
        "Topic :: System :: Monitoring"
    ],
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers

)
