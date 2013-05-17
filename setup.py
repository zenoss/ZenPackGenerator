import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ZenPack Generator",
    version = "0.0.1",
    author = "Zenoss Labs",
    author_email = "labs@zenoss.com",
    description = ("A tool to build snmp based zenpacks."),
    license = "GPL",
    keywords = "snmp zenpack",
    url = "https://github.com/zenoss/ZenPackGenerator",
    package_dir={'': 'src'},
    packages=['zpg'],
    install_requires=['Cheetah','PyYaml', 'gitpython', 'inflect'],
    requires=['Cheetah','PyYaml', 'gitpython', 'inflect'],
    entry_points={'console_scripts': ['zpg = zpg.main:main'] },
    long_description=read('README'),
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
