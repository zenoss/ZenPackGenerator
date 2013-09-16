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


class Enumspy(Template):
    """Build the snmp modeller enumeration file """

    def __init__(self,
                 zenpack,
                 ):
        '''Args:
                 zenpack: ZenPack class instance
        '''

        super(Enumspy, self).__init__(zenpack)
        self.source_template = 'enumspy.tmpl'
        self.zenpack = zenpack

        # Write the path
        dest_file_part = "enums.py"
        self.dest_file = "%s/%s" % (zpDir(zenpack), dest_file_part)

    def write(self):
        '''Write the modelerplugin'''
        if self.zenpack.enums:
            self.processTemplate()
