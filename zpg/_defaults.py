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
log = logging.getLogger('Defaults')

"""Defaults for Zenoss ZenPack Builder"""
defaults = {
    'color': True,
    'author': 'ZenossLabs <labs@zenoss.com>',
    'author_email': 'labs@zenoss.com',
    'description': 'A tool to assist building zenpacks.',
    'version': '1.0.5',
    'license': 'GPL',
    'license_header': '''
######################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is
# installed.
#
######################################################################
''',
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
    def __init__(self):
        self.defaults = defaults
        user_zpg_defaults = expanduser('~')+'/.zpg'
        if os.path.exists(user_zpg_defaults):
            with open(user_zpg_defaults, 'r') as f:
                try:
                    self.userdefaults = json.load(f, cls=DefaultsJSONDecoder)
                except Exception:
                    print "Failed to load user defaults to error in ~/.zpg json file"
                    self.userdefaults = None
        else:
            self.userdefaults = None

    def get(self, *args, **kwargs):
        return self.userdefaults.get(args[0], self.defaults.get(*args, **kwargs))
