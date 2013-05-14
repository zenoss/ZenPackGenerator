#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################

import unittest
from utils import KlassExpand
from Relationship import Relationship
find = Relationship.find

class DeviceClass(object):
    deviceClasses = {}

    def __init__(self, path, ZenPack, prefix='/zport/dmd', zPythonClass='Products.ZenModel.Device.Device'):
        self.zenpack = ZenPack
        self.path = '/'.join([prefix, path.lstrip('/')])
        self.id = self.path
        self.subClasses = {}
        self.zPythonClass = KlassExpand(self.zenpack, zPythonClass)
        self.DeviceType()

        DeviceClass.deviceClasses[self.id] = self
        self.zenpack.registerDeviceClass(self)

    def DeviceType(self):
        self.deviceType = self.zenpack.addComponentType(self.zPythonClass, device=True)

    def addClass(self, deviceClass, *args, **kwargs):
        if 'prefix' in kwargs:
            del(kwargs['prefix'])

        if 'zPythonClass' in kwargs:
            return DeviceClass(deviceClass,
                               self.zenpack,
                               prefix=self.path,
                               *args,
                               **kwargs)
        else:
            return DeviceClass(deviceClass,
                               self.zenpack,
                               prefix=self.path,
                               zPythonClass=self.zPythonClass,
                               *args,
                               **kwargs)

    def addComponentType(self, component, **kwargs):
        c = self.deviceType.addComponentType(component, **kwargs)
        return c

    @property
    def componentTypes(self):
        def ComponentFind(child=None):
            components = []
            if child:
                rels = find(child, First=True)
                for rel in rels:
                    newchild = rel.child()
                    components.append(newchild)
                    if child == newchild:
                        rval = ComponentFind(None)
                    else:
                        rval = ComponentFind(newchild)
                    if rval:
                        components = components + rval
            return components
        components = ComponentFind(self.deviceType)
        return sorted(components)


#Unit tests Start here
class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from ZenPack import ZenPack
        self.zp = ZenPack('a.b.c')


class TestDeviceClassCreate(SimpleSetup):
    #@unittest.skip("Skipping")
    def test_DeviceClassCreate(self):
        dc = DeviceClass('/Storage/Foo', self.zp)
        self.assertIsInstance(dc, DeviceClass)
        self.assertEqual(dc.zPythonClass, 'Products.ZenModel.Device.Device')

    def test_SubDeviceClassCreate(self):
        dc = DeviceClass('Storage/Foo', self.zp)
        sdc = dc.addClass('Bar')
        self.assertEqual(sdc.path, '/zport/dmd/Storage/Foo/Bar')
        self.assertEqual(sdc.zPythonClass, 'Products.ZenModel.Device.Device')

    def test_DeviceClassComponentId(self):
        dc = DeviceClass('Storage/Foo', self.zp)
        self.assertEqual(dc.deviceType.id, 'Products.ZenModel.Device.Device')

    def test_setzPythonClass_on_DeviceClass(self):
        dc = DeviceClass('Storage/Foo', self.zp, zPythonClass='a.b.c.Device')
        self.assertEqual(dc.zPythonClass, 'a.b.c.Device')
        self.assertEqual(dc.deviceType.id, 'a.b.c.Device')

    def test_setzPythonClass_shortClass(self):
        dc = DeviceClass('Storage/Foo', self.zp, zPythonClass='Device')
        self.assertEqual(dc.zPythonClass, 'a.b.c.Device')
        self.assertEqual(dc.deviceType.id, 'a.b.c.Device')

    def test_addSubComponentToCustomDeviceComponent(self):
        from Component import Component
        from Relationship import Relationship
        dc = DeviceClass('Storage/NetApp', self.zp, zPythonClass='Device')
        sc = dc.addComponentType('Fan')
        self.assertIsInstance(sc, Component)
        self.assertEqual(Relationship.relationships['a.b.c.Device a.b.c.Fan'].hasComponent(sc), True)
        self.assertEqual(Relationship.relationships['a.b.c.Device a.b.c.Fan'].hasComponent(dc.deviceType), True)

    def test_addSubComponentToDefaultDeviceComponent(self):
        from Component import Component
        from Relationship import Relationship
        dc2 = DeviceClass('Server/Linux', self.zp)
        sc2 = dc2.addComponentType('Fan2')
        self.assertIsInstance(sc2, Component)
        self.assertEqual(Relationship.relationships['Products.ZenModel.Device.Device a.b.c.Fan2'].hasComponent(sc2), True)
        self.assertEqual(Relationship.relationships['Products.ZenModel.Device.Device a.b.c.Fan2'].hasComponent(dc2.deviceType), True)

class TestDeviceClassComponents(SimpleSetup):
    def test_componentTypes(self):
        dc = DeviceClass('Storage/Example', self.zp, zPythonClass='Device')
        fc = dc.addComponentType('Fan')
        dc.addComponentType('Battery')
        dc.addComponentType('Cpu')
        fc.addComponentType('Blade')
        self.assertEqual(['a.b.c.Battery', 'a.b.c.Blade', 'a.b.c.Cpu', 'a.b.c.Fan'], [c.id for c in dc.componentTypes])



if __name__ == "__main__":
    unittest.main()
