#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################


from Component import Component
from Relationship import Relationship
from DeviceClass import DeviceClass
from Defaults import Defaults
from License import License
from utils import prepId

#from UI import UI
from memoize import memoize
import unittest

defaults = Defaults()


class ZenPack(object):

    def __init__(self,
                 id,
                 author=defaults.author,
                 version=defaults.version,
                 license=License(defaults.license),
                 destdir='/foo'):

        self.id = id
        self.namespace = id
        self.deviceClasses = {}
        self.components = {}
        self.relationships = {}
        self.author = author
        self.version = version
        self.license = license
        self.prepname = prepId(id).replace('.', '_')


#        self.addComponent('Device', namespace='Products.ZenModel')
#        o = self.addComponent('OperatingSystem', id='os',
#                              Classes=['Products.ZenModel.Software.Software'],
#                              namespace='Products.ZenModel')
#        self.addComponent('IpInterface', id='interface', namespace='Products.ZenModel')
#        self.addRelation('os','interface')
#        o.write()
#        self.addComponent('Hardware', id='hw', namespace='Products.ZenModel')

    @memoize
    def addDeviceClass(self, deviceClass, *args, **kwargs):
        dc = DeviceClass(deviceClass, self, *args, **kwargs)
        return dc

    @memoize
    def addComponent(self, component, **kwargs):
        c = Component(component, self, **kwargs)
        return c

    @memoize
    def addRelation(self, *args, **kwargs):
        r = Relationship(self, *args, **kwargs)
        return r

    def registerComponent(self, component):
        self.components[component.id] = component

    def registerRelationship(self, relationship):
        self.relationships[relationship.id] = relationship

    def registerDeviceClass(self, deviceClass):
        self.deviceClasses[deviceClass.id] = deviceClass

    #def relationshipLookup(self, component):
    #    relationships = []
    #    for relationship in self.relationships.values():
    #        if relationship.hasComponent(component):
    #            relationships.append(relationship)

    #    return relationships

    def __repr__(self):
        return "%s \n\tAUTHOR: %s\n\tVERSION: %s\n\tLICENSE: %s" \
               % (self.id, self.author, self.version, self.license)


# Unit Tests Start here
class SimpleSetup(unittest.TestCase):
    def setUp(self):
        self.zp = ZenPack('a.b.c')


class TestZenPackLicense(SimpleSetup):
    def test_default(self):
        self.assertEqual(str(self.zp.license), str(License(defaults.license)))


class TestZenPackDeviceClass(SimpleSetup):
    def test_addDeviceClass(self):
        dc1 = self.zp.addDeviceClass('Devices/Storage/DC1')
        self.assertIsInstance(dc1, DeviceClass)

    def test_addMemoizedDeviceClass(self):
        dc1 = self.zp.addDeviceClass('Devices/Storage/DC1')
        dc2 = self.zp.addDeviceClass('Devices/Storage/DC1')
        self.assertIs(dc1, dc2)


class TestZenPackComponent(SimpleSetup):
    def test_addComponent(self):
        c1 = self.zp.addComponent('Foo')
        self.assertIsInstance(c1, Component)

    def test_addMemoizedComponent(self):
        c1 = self.zp.addComponent('Component')
        c2 = self.zp.addComponent('Component')
        self.assertIs(c1, c2)

    def test_ComponentId(self):
        c1 = self.zp.addComponent('Component')
        self.assertEqual(c1.id, 'a.b.c.Component')


class TestZenPackRelationships(SimpleSetup):
    def test_oneToManyCont(self):
        self.zp.addRelation('Device', 'Vservers')
        self.zp.addRelation('Device', 'SystemNodes')
        self.zp.addRelation('Device', 'ClusterPeers')

if __name__ == "__main__":
    from Configure import Configure
    zp = ZenPack('ZenPacks.training.NetBotz')
    c = Configure(zp)
    dc = zp.addDeviceClass('Device/Snmp', zPythonClass='NetBotzDevice')
    e = dc.addSubComponent('Enclosure')
    e.addProperty('enclosure_status')
    e.addProperty('error_status')
    e.addProperty('parent_id')
    e.addProperty('docked_id')

    ts = e.addSubComponent('TemperatureSensor')
    ts.addProperty('port')

    deviceComponent = dc.deviceComponent
    deviceComponent.addProperty('temp_sensor_count', Type='int')

    deviceComponent.write()
    e.write()
    ts.write()

    # Configure.zcml
    c.write()

    unittest.main()
