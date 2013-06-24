#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

"""
ZenPack Generator (zpg)
~~~~~~~~~~~~~~~~~~~~~~~

ZenPack Generator is a generator for ZenPacks to extend Zenoss, written in
Python.  Basic usage:

    >>> import zpg
    >>> zpg.generate('examples/netbotz.json')
    ...

... or from the command line:

    $ zpg -j examples/netbotz.json
    ...


:copyright: (c) 2013 Zenoss, Inc.
:license: GPL

"""

from ._defaults import defaults

__title__ = 'ZenPack Generator'
__version__ = defaults.get('version', "0.0.1")
__build__ = defaults.get('build', 0x000001)
__author__ = defaults.get('author', 'Zenosslabs <labs@zenoss>')
__license__ = defaults.get('license', 'GPL')
__copyright__ = defaults.get('copyright', 'Copyright 2013 Zenoss, Inc.')

from .api import generate
from ._defaults import defaults
from ._zenoss_utils import prepId, KlassExpand, zpDir
from .Component import Component
from .ComponentJS import ComponentJS
from .Configure import Configure
from .DeviceClass import DeviceClass
from .DirLayout import DirLayout, initpy
from .License import License
from .Property import Property
from .Relationship import Relationship
from .RootInit import RootInit
from .Setup import Setup
from .Template import Template
from .UtilsTemplate import UtilsTemplate
from .ZenPack import ZenPack, Opts

__all__ = [
    "defaults",
    "__title__",
    "__version__",
    "__build__",
    "__author__",
    "__license__",
    "__copyright__",
    "generate",
    "ZenPack"
]

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):

        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
logging.basicConfig(format="%(message)s")
