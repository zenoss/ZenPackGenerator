#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################

from utils import KlassExpand, zpDir
from Template import Template


class ImpactZcml(Template):
    """Build the impact object"""

    def __init__(self,
                 zenpack,
                 ):
        '''Args:
                 zenpack: ZenPack class instance
                 impactArray: [
                 		component: Reference Component
                                impacts: An Array of components that impact the reference component.
                                impactedBy: An Array of components that are impacted by the reference component.
                              ]

        '''

        super(ImpactZcml, self).__init__(zenpack)
        self.source_template = 'impact.zcml.tmpl'
        self.zenpack = zenpack
        self.components = zenpack.components

        self.dest_file = "%s/impact.zcml" % zpDir(zenpack)

    def write(self):
        '''Write the impact file'''

        #self.updateImports()
        self.processTemplate()
