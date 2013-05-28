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
    '''Create a js file per unique deviceClass'''

    def __init__(self, deviceClass):
        '''Args:
                 deviceClass: a DeviceClass instance that contains components
        '''
        super(ComponentJS, self).__init__(deviceClass.zenpack)
        self.deviceClass = deviceClass
        self.zenpack = self.deviceClass.zenpack
        self.zPythonClass = self.deviceClass.zPythonClass

        self.source_template = 'component.js.tmpl'
        self.dest_file = "%s/resources/js/%s.js" % (zpDir(self.zenpack), self.name)

    @property
    def name(self):
        '''give a unique name'''

        zpid = self.deviceClass.zenpack.id
        zpc_name = "_".join(self.deviceClass.zPythonClass.split('.'))
        if self.deviceClass.zPythonClass.startswith(zpid):
            return zpc_name
        else:
            # if the deviceclass is outside of the context of the zenpack
            # provide the zenpack id plus the zPythonClass as a name
            return "_".join(zpid.split('.')) + "__" + zpc_name

    def write(self):
        '''Write the component javascript file.'''

        # Update the components just before we need them.
        self.components = self.deviceClass.componentTypes
        if self.components:
            #Todo property sorting options
            self.processTemplate()
