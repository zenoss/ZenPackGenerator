#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################


class Defaults(object):
    """Defaults for Zenoss ZenPack Builder
    Parameters
    ----------
    None.

    Returns
    -------
    None
    """

    def __init__(self):
        self.author = 'ZenossLabs <labs@zenoss.com>'
        self.version = '0.0.1'
        self.license = 'gpl'
        self.klasses = ['Products.ZenModel.DeviceComponent.DeviceComponent',
                        'Products.ZenModel.ManagedEntity.ManagedEntity']

        self.imports = ['from zope.component import implements',
                        'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
                        'from Products.Zuul.decorators import info',
                        'from Products.Zuul.form import schema',
                        'from Products.Zuul.infos import ProxyProperty',
                        'from Products.Zuul.utils import ZuulMessageFactory as _t',
                        ]


