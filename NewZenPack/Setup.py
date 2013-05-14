##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################

from Cheetah.Template import Template as cTemplate


class Setup(object):

    def __init__(self, zenpack):
        self.zenpack = zenpack



    def write(self):
        setup = cTemplate(file='setup.tmpl', searchList=[self])
        print setup

# if __name__ == '__main__':
#     from ZenPack import ZenPack
#     zp = ZenPack('ZenPacks.training.NetBotz')
#     dc = zp.addDeviceClass('Device/Snmp', zPythonClass='NetBotzDevice')
#     e = dc.addComponentType('Enclosure')
#     e.addProperty('enclosure_status')
#     e.addProperty('error_status')
#     e.addProperty('parent_id')
#     e.addProperty('docked_id')

#     ts = e.addComponentType('TemperatureSensor')
#     ts.addProperty('port')

#     dc.deviceType.addProperty('temp_sensor_count', Type='int')

#     v = dc.addComponentType('Volume')
#     l = dc.addComponentType('Lun')
#     vs = dc.addComponentType('VServer')
#     zp.addRelation('VServer', 'Volume', Type='1-M', Contained=False)
#     zp.addRelation('Lun', 'Volume', Type='1-M', Contained=False)
#     ComponentJS(dc).write()
