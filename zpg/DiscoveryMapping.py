#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

from .colors import error, warn, debug, info, green, red, yellow


class DiscoveryMapping(object):
    ''' Discovery Mapping Object '''

    discoveryMappings = {}

    def __init__(self,
                 zenpack,
                 oid,
                 deviceClass,
                 *args,
                 **kwargs
                 ):
        """Args:
             zenpack:
             oid: 
             deviceClass: 
        """
        self.zenpack = zenpack
        self.oid = oid
        self.deviceClass = deviceClass

        for key in kwargs:
            do_not_warn = False
            clsname = self.__class__.__name__
            layer = "%s:%s" % (clsname, self.name)
            msg = "WARNING: [%s] unknown keyword ignored in file: '%s'"
            margs = (layer, key)
            if not do_not_warn:
                warn(self.logger, yellow(msg) % margs)

        DiscoveryMapping.discoveryMappings[self.oid] = self
        self.zenpack.registerDiscoveryMapping(self)
