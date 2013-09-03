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

# This is a hack to pull in the defaults from zpg until we have
#  something better.  This eliminates the necessity of importing
#  zpg at the start and allows us to run the setup file without the
#  dependencies installed.
filepath = os.path.abspath(__file__)
folder = os.path.dirname(filepath)
defaults_path = os.path.join(folder, 'zpg', '_defaults.py')
with open(defaults_path, 'r') as fd:
    data = "".join(fd.readlines())
    exec data

packages = [
    'zpg',
]


requires = [
    'Cheetah',
    'PyYaml',
    'gitpython',
    'colorama',
    'inflect',
    'lxml',
    'Mock',
    'nose',
    'pep8',
    'argparse'
]


setup(
    name="zpg",
    version=defaults.get("version", "0.0.1"),  # zpg.__version__
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
    setup_requires=requires,
    install_requires=requires,
    entry_points={'console_scripts': ['zpg = zpg:generate']},
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
)
