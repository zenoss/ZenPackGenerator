#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################

from Cheetah.Template import Template as cTemplate
from Component import Component
from Relationship import Relationship
find = Relationship.find

class RootInit(object):

    def __init__(self, zenpack):
        self.zenpack = zenpack
        self.devChildren = None

    def write(self):
        self.components = self.zenpack.components.values()

        devChildren = []
        dc = Component('Products.ZenModel.Device.Device', self.zenpack)
        rels = find(dc)
        for rel in rels:
            component = rel.components[1]
            devChildren.append(component)
        self.devChildren = devChildren
        ri = cTemplate(file='root_init.tmpl', searchList=[self])
        print ri

if __name__ == '__main__':
    from ZenPack import ZenPack
    zp = ZenPack('a.b.c')
    dc = zp.addDeviceClass('/')
    e = dc.addComponentType('Enclosure')

    zp.write()
