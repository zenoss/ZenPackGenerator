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


class SnmpModelerPlugin(Template):
    """Build the snmp modeller object"""
    
    snmpmodelerplugins = {}

    def __init__(self,
                 zenpack,
                 component,
                 id
                 ):
        '''Args:
                 zenpack: ZenPack class instance
        '''

        super(SnmpModelerPlugin, self).__init__(zenpack)
        self.source_template = 'snmpmodelerplugin.tmpl'
        self.id = id
        self.zenpack = zenpack
        self.component = component


        # Write the path
        dest_file_part = "modeler/plugins/"+"/".join(self.id.split('.'))
        self.dest_file = "%s/%s.py" % (zpDir(zenpack), dest_file_part)

        SnmpModelerPlugin.snmpmodelerplugins[self.id] = self
        self.zenpack.registerSnmpModelerPlugin(self)

    def write(self):
        '''Write the modelerplugin'''

        self.processTemplate()
