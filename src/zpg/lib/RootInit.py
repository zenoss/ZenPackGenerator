#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################


from Template import Template
from Component import Component
from Relationship import Relationship
from utils import zpDir
find = Relationship.find

class RootInit(Template):

    def __init__(self, zenpack):
        self.zenpack = zenpack
        self.devChildren = None
        super(RootInit, self).__init__(zenpack)
        self.source_template = 'root_init.tmpl'
        self.dest_file = "%s/%s" % (zpDir(zenpack), '__init__.py')

    def write(self):
        self.components = self.zenpack.components.values()

        devChildren = []
        dc = Component('Products.ZenModel.Device.Device', self.zenpack)
        rels = find(dc)
        for rel in rels:
            component = rel.components[1]
            devChildren.append(component)
        self.devChildren = devChildren
        self.processTemplate()


if __name__ == '__main__':
    from ZenPack import ZenPack
    zp = ZenPack('a.b.c')
    dc = zp.addDeviceClass('/')
    e = dc.addComponentType('Enclosure')

    zp.write()
