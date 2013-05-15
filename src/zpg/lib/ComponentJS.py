##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################

from Template import Template
from utils import zpDir

class ComponentJS(Template):

    def __init__(self, deviceClass):
        super(ComponentJS, self).__init__(deviceClass.zenpack)
        self.deviceClass = deviceClass
        self.zenpack = self.deviceClass.zenpack
        self.zPythonClass = self.deviceClass.zPythonClass

        self.source_template = 'component.js.tmpl'
        self.dest_file = "%s/resources/js/%s.js" % (zpDir(self.zenpack), self.name)

    @property
    def name(self):
        zpid = self.deviceClass.zenpack.id
        zpc_name = "_".join(self.deviceClass.zPythonClass.split('.'))
        if self.deviceClass.zPythonClass.startswith(zpid):
            return zpc_name
        else:
            return "_".join(zpid.split('.')) + "__" + zpc_name

    def write(self):
        # Update the components just before we need them.
        self.components = self.deviceClass.componentTypes
        if self.components:
            #Todo property sorting options
            self.processTemplate()
