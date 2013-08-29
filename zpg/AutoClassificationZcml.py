#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################

from ._defaults import Defaults
from ._zenoss_utils import KlassExpand, zpDir
from .Template import Template
defaults = Defaults()


class AutoClassificationZcml(Template):
    """Build the autoclassification.zcml file"""

    def __init__(self,
                 zenpack,
                 ):
        '''Args:
                 zenpack: ZenPack class instance

        '''

        super(AutoClassificationZcml, self).__init__(zenpack)
        self.source_template = 'autoclassification.zcml.tmpl'
        self.zenpack = zenpack
        self.components = zenpack.components

        self.dest_file = "%s/autoclassification.zcml" % zpDir(zenpack)

    def discoveryMappings(self):
        if self.zenpack.discoveryMappings:
            return True
        return False

    def write(self):
        '''Write the file'''

        if self.discoveryMappings():
            self.processTemplate()
