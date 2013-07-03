#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################

from ._zenoss_utils import KlassExpand, zpDir
from .Template import Template


class Impact(Template):
    """Build the impact object"""

    def __init__(self,
                 zenpack,
                 ):
        '''Args:
                 zenpack: ZenPack class instance

        '''

        super(Impact, self).__init__(zenpack)
        self.source_template = 'impact.tmpl'
        self.zenpack = zenpack
        self.components = zenpack.components

        self.dest_file = "%s/impact.py" % zpDir(zenpack)

    def write(self):
        '''Write the impact file'''

        #self.updateImports()
        self.processTemplate()
