#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#


from .Template import Template
from .Component import Component
from .Relationship import Relationship
from ._zenoss_utils import zpDir
find = Relationship.find


class RootInit(Template):

    """ Write the template to a __init__.py file
        eg.  Create ZenPacks.zenoss.Foo/ZenPacks/zenoss/Foo/__init__.py """

    def __init__(self, zenpack):
        self.zenpack = zenpack
        self.devChildren = None
        super(RootInit, self).__init__(zenpack)
        self.source_template = 'root_init.tmpl'
        self.dest_file = "%s/%s" % (zpDir(zenpack), '__init__.py')

    def write(self):
        """Write __init__.py"""
        self.components = self.zenpack.components.values()

        devChildren = {}

        # Search for any components contained inside the Device Component.
        dc = Component(self.zenpack, 'Products.ZenModel.Device.Device')
        rels = find(dc)
        for rel in rels:
            component = rel.components[1]
            devChildren[component] = rel
        self.devChildren = devChildren
        self.processTemplate()
