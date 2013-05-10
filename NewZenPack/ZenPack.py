#!/usr/bin/env python
##LICENSE##

from Component import Component
from Relationship import Relationship
from DeviceClass import DeviceClass
from Defaults import Defaults
from License import License
from memoize import memoize
import unittest

defaults = Defaults()


class ZenPack(object):

    def __init__(self,
                 id,
                 author=defaults.author,
                 version=defaults.version,
                 license=License(defaults.license)):

        self.id = id
        self.namespace = id
        self.deviceClasses = {}
        self.components = {}
        self.relationships = {}
        self.author = author
        self.version = version
        self.license = license
#        self.addComponent('Device', namespace='Products.ZenModel')
#        o = self.addComponent('OperatingSystem', id='os',
#                              Classes=['Products.ZenModel.Software.Software'],
#                              namespace='Products.ZenModel')
#        self.addComponent('IpInterface', id='interface', namespace='Products.ZenModel')
#        self.addRelation('os','interface')
#        o.write()
#        self.addComponent('Hardware', id='hw', namespace='Products.ZenModel')

    @memoize
    def addDeviceClass(self, deviceClass):
        dc = DeviceClass(deviceClass, self)
        self.deviceClasses[dc.id] = dc
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

    def relationshipLookup(self, component):
        relationships = []
        for relationship in self.relationships.values():
            if relationship.hasComponent(component):
                relationships.append(relationship)

        return relationships

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
    zp = ZenPack('a.b.c')
    zp.addRelation('Device', 'Vservers')
    unittest.main()
