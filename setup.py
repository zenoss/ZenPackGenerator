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
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

import zpg

packages = [
    'zpg',
]


requires = [
    'Cheetah',
    'PyYaml',
    'gitpython',
    'colorama',
    'inflect',
    'Mock',
]


setup(
    name="zpg",
    version=zpg.__version__,
    description="ZenPack Generator",
    long_description=open('README.rst').read() + '\n\n' +
    open('HISTORY.rst').read(),
    author="Zenoss Labs",
    author_email="labs@zenoss.com",
    url="http://github.com/zenoss/ZenPackGenerator",
    keywords="zenpack",
    package_dir={'zpg': 'zpg'},
    package_data={'': ['LICENSE', 'NOTICE'], 'zpg': ['Templates/*.tmpl']},
    packages=packages,
    requires=requires,
    install_requires=requires,
    entry_points={'console_scripts': ['zpg = zpg:main']},
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Code Generators",
        "Topic :: System :: Monitoring"
    ],
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers

)
