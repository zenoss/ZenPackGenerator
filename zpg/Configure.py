#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

from ._zenoss_utils import zpDir
from .Template import Template


class Configure(Template):

    ''' Write the template to a setup.py file
        eg.  Create ZenPacks.zenoss.Foo/ZenPacks/zenoss/Foo/configure.zcml '''

    def __init__(self, zenpack):
        '''Args:
                 zenpack: ZenPack Class instance
        '''
        super(Configure, self).__init__(zenpack)
        self.source_template = 'configure.zcml.tmpl'
        self.dest_file = "%s/%s" % (zpDir(zenpack), 'configure.zcml')
        self.zenpack = zenpack
        self.components = zenpack.components
        self.deviceClasses = zenpack.deviceClasses
        self.componentJSs = zenpack.componentJSs

    def customPathReporters(self):
        '''Return true if there are any custompath reporters'''
        for c in self.components.values():
            if c.custompaths():
                return True
        return False

    def impactAdapters(self):
        '''Return true if there are any impact relationships'''
        for c in self.components.values():
            if c.hasImpact():
                return True
        return False

    def discoveryMappings(self):
        if self.zenpack.discoveryMappings:
            return True
        return False
        

# TODO
# Router and facade
# custom device loaders
# dynamic view
# datasources
# datapoints

    def write(self):
        ''' Write the configure.zcml file '''
        self.processTemplate()

# if __name__ == '__main__':
    # zp.write()
