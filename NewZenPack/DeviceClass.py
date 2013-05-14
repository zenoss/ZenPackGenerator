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


class DeviceClass(object):
    deviceClasses = {}

    def __init__(self, path, ZenPack, prefix='/zport/dmd', zPythonClass='Products.ZenModel.Device.Device'):
        self.zenpack = ZenPack
        self.path = '/'.join([prefix, path.lstrip('/')])
        self.id = self.path
        self.subClasses = {}
        self.zPythonClass = KlassExpand(self.zenpack, zPythonClass)
        self.DeviceComponent()

        DeviceClass.deviceClasses[self.id] = self
        self.zenpack.registerDeviceClass(self)

    def DeviceComponent(self):
        self.deviceComponent = self.zenpack.addComponent(self.zPythonClass, device=True)

    def addSubClass(self, deviceClass, *args, **kwargs):
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

    def addSubComponent(self, component, **kwargs):
        c = self.deviceComponent.addSubComponent(component, **kwargs)
        return c

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
        sdc = dc.addSubClass('Bar')
        self.assertEqual(sdc.path, '/zport/dmd/Storage/Foo/Bar')
        self.assertEqual(sdc.zPythonClass, 'Products.ZenModel.Device.Device')

    def test_DeviceClassComponentId(self):
        dc = DeviceClass('Storage/Foo', self.zp)
        self.assertEqual(dc.deviceComponent.id, 'Products.ZenModel.Device.Device')

    def test_setzPythonClass_on_DeviceClass(self):
        dc = DeviceClass('Storage/Foo', self.zp, zPythonClass='a.b.c.Device')
        self.assertEqual(dc.zPythonClass, 'a.b.c.Device')
        self.assertEqual(dc.deviceComponent.id, 'a.b.c.Device')

    def test_setzPythonClass_shortClass(self):
        dc = DeviceClass('Storage/Foo', self.zp, zPythonClass='Device')
        self.assertEqual(dc.zPythonClass, 'a.b.c.Device')
        self.assertEqual(dc.deviceComponent.id, 'a.b.c.Device')

    def test_addSubComponentToCustomDeviceComponent(self):
        from Component import Component
        from Relationship import Relationship
        dc = DeviceClass('Storage/NetApp', self.zp, zPythonClass='Device')
        sc = dc.addSubComponent('Fan')
        self.assertIsInstance(sc, Component)
        self.assertEqual(Relationship.relationships['a.b.c.Device a.b.c.Fan'].hasComponent(sc), True)
        self.assertEqual(Relationship.relationships['a.b.c.Device a.b.c.Fan'].hasComponent(dc.deviceComponent), True)

    def test_addSubComponentToDefaultDeviceComponent(self):
        from Component import Component
        from Relationship import Relationship
        dc2 = DeviceClass('Server/Linux', self.zp)
        sc2 = dc2.addSubComponent('Fan2')
        self.assertIsInstance(sc2, Component)
        self.assertEqual(Relationship.relationships['Products.ZenModel.Device.Device a.b.c.Fan2'].hasComponent(sc2), True)
        self.assertEqual(Relationship.relationships['Products.ZenModel.Device.Device a.b.c.Fan2'].hasComponent(dc2.deviceComponent), True)


if __name__ == "__main__":
    unittest.main()