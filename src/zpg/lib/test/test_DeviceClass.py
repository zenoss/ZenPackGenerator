import unittest
from zpg.lib.DeviceClass import DeviceClass
from zpg.lib.Relationship import Relationship
from zpg.lib.Component import Component

#Unit tests Start here
class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from zpg.lib.ZenPack import ZenPack
        self.zp = ZenPack('a.b.c')

    def tearDown(self):
        del(self.zp)


class TestDeviceClassCreate(SimpleSetup):
    #@unittest.skip("Skipping")
    def test_DeviceClassCreate(self):
        dc = DeviceClass(self.zp, '/Storage/Foo')
        self.assertIsInstance(dc, DeviceClass)
        self.assertEqual(dc.zPythonClass, 'Products.ZenModel.Device.Device')

    def test_SubDeviceClassCreate(self):
        dc = DeviceClass(self.zp, 'Storage/Foo')
        sdc = dc.addClass('Bar')
        self.assertEqual(sdc.path, '/zport/dmd/Storage/Foo/Bar')
        self.assertEqual(sdc.zPythonClass, 'Products.ZenModel.Device.Device')

        sdc_zp = dc.addClass('Bar2',zPythonClass='Products.ZenModel.Foo.Foo')
        self.assertEqual(sdc_zp.path, '/zport/dmd/Storage/Foo/Bar2')
        self.assertEqual(sdc_zp.zPythonClass, 'Products.ZenModel.Foo.Foo')

        sdc_p = dc.addClass('Bar3',prefix='bah')
        self.assertEqual(sdc_p.path, '/zport/dmd/Storage/Foo/Bar3')

    def test_DeviceClassComponentId(self):
        dc = DeviceClass(self.zp, 'Storage/Foo')
        self.assertEqual(dc.deviceType.id, 'Products.ZenModel.Device.Device')

    def test_setzPythonClass_on_DeviceClass(self):
        dc = DeviceClass(self.zp, 'Storage/Foo', zPythonClass='a.b.c.Device')
        self.assertEqual(dc.zPythonClass, 'a.b.c.Device')
        self.assertEqual(dc.deviceType.id, 'a.b.c.Device')

    def test_setzPythonClass_shortClass(self):
        dc = DeviceClass(self.zp, 'Storage/Foo', zPythonClass='Device')
        self.assertEqual(dc.zPythonClass, 'a.b.c.Device')
        self.assertEqual(dc.deviceType.id, 'a.b.c.Device')

    def test_addSubComponentToCustomDeviceComponent(self):
        dc = DeviceClass(self.zp, 'Storage/NetApp', zPythonClass='Device')
        sc = dc.addComponentType('Fan')
        self.assertIsInstance(sc, Component)
        self.assertEqual(Relationship.relationships['a.b.c.Device a.b.c.Fan'].hasComponent(sc), True)
        self.assertEqual(Relationship.relationships['a.b.c.Device a.b.c.Fan'].hasComponent(dc.deviceType), True)

    def test_addSubComponentToDefaultDeviceComponent(self):
        dc2 = DeviceClass(self.zp, 'Server/Linux')
        sc2 = dc2.addComponentType('Fan2')
        self.assertIsInstance(sc2, Component)
        self.assertEqual(Relationship.relationships['Products.ZenModel.Device.Device a.b.c.Fan2'].hasComponent(sc2), True)
        self.assertEqual(Relationship.relationships['Products.ZenModel.Device.Device a.b.c.Fan2'].hasComponent(dc2.deviceType), True)


class TestDeviceClassComponents(SimpleSetup):
    def test_componentTypes(self):
        dc = DeviceClass(self.zp, 'Storage/Example', zPythonClass='Device')
        fc = dc.addComponentType('Fan')
        dc.addComponentType('Battery')
        dc.addComponentType('Cpu')
        fc.addComponentType('Blade')
        self.assertEqual(['a.b.c.Battery', 'a.b.c.Blade', 'a.b.c.Cpu', 'a.b.c.Fan'], [c.id for c in dc.componentTypes])

if __name__ == '__main__':
    unittest.main()
