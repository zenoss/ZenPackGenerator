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


class ImpactPy(Template):
    """Build the impact object"""

    def __init__(self,
                 zenpack,
                 ):
        '''Args:
                 zenpack: ZenPack class instance

        '''

        super(ImpactPy, self).__init__(zenpack)
        self.source_template = 'impact.tmpl'
        self.zenpack = zenpack
        self.components = zenpack.components

        self.dest_file = "%s/impact.py" % zpDir(zenpack)
        self.imports = defaults.get('impact_imports')

    def updateImports(self):
        impact_components = []
        for c in self.components.values():
            if c.hasImpact():
                for ic in c.impacts:
                    if ic not in impact_components:
                        impact_components.append(ic)
                for ibc in c.impactedBy:
                    if ibc not in impact_components:
                        impact_components.append(ibc)

        for c in impact_components:
            klass = c.id.split('.')[-1]
            istring = "from {0} import {1}".format(c.id, klass)
            if istring not in self.imports:
                self.imports.append(istring)

    def write(self):
        '''Write the impact file'''

        self.updateImports()
        self.processTemplate()
