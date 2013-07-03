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
from ._zenoss_utils import zpDir


class ZenPackUI(Template):
    """Build the ZenPack global js file to register components."""
    def __init__(self, ZenPack):
        super(ZenPackUI, self).__init__(ZenPack)
        self.zenpack = ZenPack
        self.source_template = 'zenpackjs.tmpl'
        self.dest_file = "%s/resources/js/%s.js" % (
            zpDir(self.zenpack), self.zenpack.id)

    def write(self):
        # Update the components just before we need them.
        self.components = self.zenpack.components.values()
        if self.components:
            # Todo property sorting options
            self.processTemplate()
