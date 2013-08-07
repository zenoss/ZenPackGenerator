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
from os.path import expanduser
import logging
import json

# Wrapped in Exception handler so that setup.py can load this file.
try:
    from .colors import error, warn, debug, info, green, red, disable_color
except Exception:
    pass

log = logging.getLogger('Defaults')

"""Defaults for Zenoss ZenPack Builder"""
defaults = {
    'color': True,
    'author': 'ZenossLabs <labs@zenoss.com>',
    'author_email': 'labs@zenoss.com',
    'description': 'A tool to assist building zenpacks.',
    'version': '1.0.11',
    'license': 'GPLv2',
    'component_classes': [
        'Products.ZenModel.DeviceComponent.DeviceComponent',
        'Products.ZenModel.ManagedEntity.ManagedEntity'
    ],
    'device_classes': [
        'Products.ZenModel.Device.Device'
    ],
    'component_imports': [
        'from zope.interface import implements',
        'from Products.ZenModel.Device import Device',
        'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
        'from Products.Zuul.decorators import info',
        'from Products.Zuul.form import schema',
        'from Products.Zuul.infos import ProxyProperty',
        'from Products.Zuul.utils import ZuulMessageFactory as _t',
    ],
    'device_imports': [
        'from zope.interface import implements',
        'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
        'from Products.Zuul.form import schema',
        'from Products.Zuul.infos import ProxyProperty',
        'from Products.Zuul.utils import ZuulMessageFactory as _t',
    ],
    'impact_imports': [
        'from zope.component import adapts',
        'from zope.interface import implements',
        'from Products.ZenUtils.guid.interfaces import IGlobalIdentifier',
        'from ZenPacks.zenoss.Impact.impactd import Trigger',
        'from ZenPacks.zenoss.Impact.impactd.relations import ImpactEdge',
        'from ZenPacks.zenoss.Impact.impactd.interfaces import \
IRelationshipDataProvider',
        'from ZenPacks.zenoss.Impact.impactd.interfaces import INodeTriggers'
    ],
}


class DefaultsJSONDecoder(json.JSONDecoder):
    def decode(self, json_string):
        """
        json_string is basically string that you give to json.loads method
        """
        #json_string = re.sub('"Contained"', '"contained"', json_string)
        default_obj = super(DefaultsJSONDecoder, self).decode(json_string)
        return default_obj


class Defaults(object):
    def zpg_home(self):
        return expanduser('~') + '/.zpg/'

    def user_zpg_defaults_config(self):
        return self.zpg_home() + 'config'

    def user_zpg_license_dir(self):
        return self.zpg_home() + 'licenses'

    def __init__(self):
        self.defaults = defaults

        if os.path.exists(self.user_zpg_defaults_config()):
            debug(log, "Loading user configuration from %s" %
                       self.user_zpg_defaults_config())
            with open(self.user_zpg_defaults_config(), 'r') as f:
                try:
                    self.userdefaults = json.load(f, cls=DefaultsJSONDecoder)
                    if self.userdefaults:
                        debug(log, "  Loaded.")
                except Exception:
                    debug(log, red("  Failed."))
                    self.userdefaults = None
        else:
            self.userdefaults = None

    def get(self, *args, **kwargs):
        if self.userdefaults:
            return self.userdefaults.get(args[0],
                                         self.defaults.get(*args, **kwargs))
        else:
            return self.defaults.get(*args, **kwargs)
