import unittest
import os
from zpg.lib.ZenPack import ZenPack
from zpg.lib.DeviceClass import DeviceClass
from zpg.lib.Component import Component
from zpg.lib.License import License
from zpg.lib.Defaults import Defaults
from mock import mock_open, patch, MagicMock
defaults = Defaults()


class SimpleSetup(unittest.TestCase):
    def setUp(self):
        self.zp = ZenPack('a.b.c')

    def tearDown(self):
        del(self.zp)


class WriteBase(unittest.TestCase):
    def setUp(self):
        from zpg.lib.ZenPack import ZenPack
        self.zp = ZenPack('a.b.c')
        self.mkdir = os.mkdir
        self.makedirs = os.makedirs

        os.mkdir = MagicMock(return_value=True)
        os.makedirs = MagicMock(return_value=True)

    def write(self, obj):
        m = mock_open()
        with patch('__builtin__.open', mock_open(read_data='Dummy Data'), create=True) as m:
            obj.write()

            # Write File Handle
            wfh = m.return_value.__enter__.return_value
            self.results = wfh.write.call_args_list

    def tearDown(self):
        print "Calling teardown"
        os.mkdir = self.mkdir
        os.makedirs = self.makedirs
        del(self.zp)


class TestZenPackInitialize(unittest.TestCase):
    #@unittest.skip("Skipping")
    def test_installRequires(self):
        self.assertEqual(ZenPack('a.a.a', install_requires='foo').install_requires, ['foo'])
        self.assertEqual(ZenPack('a.a.b', install_requires=['foo']).install_requires, ['foo'])

    def test_zProperties(self):
        zp = ZenPack('a.a.c', zProperties=[ { "type": "boolean", "default": True, "Category": "NetBotz", "name": "zNetBotzExample" }, { "name": "e1" } ])
        self.assertEqual(zp.zproperties, {'e1': ('e1', "''", 'string', None), 'zNetBotzExample': ('zNetBotzExample', True, 'boolean', 'NetBotz')})

    def test_deviceClasses(self):
        zp = ZenPack('a.a.d', deviceClasses=[{"path": "Device/Snmp"} ])
        self.assertEqual(zp.deviceClasses.keys(), ['/zport/dmd/Device/Snmp'])

    def test_relationships(self):
        zp = ZenPack('a.a.e', deviceClasses=[{"path": "Device/Snmp", "componentTypes": [ { "name": "Enclosure"}, { "name": "TemperatureSensor"}, { "name": "Fan"}]}],
                              relationships=[{"ComponentA": "Enclosure", "ComponentB": "Fan", "Contained": False} ])
        self.assertEqual(zp.relationships.keys(), ['Products.ZenModel.Device.Device a.a.e.TemperatureSensor',
                                                   'a.a.e.Enclosure a.a.e.Fan',
                                                   'Products.ZenModel.Device.Device a.a.e.Enclosure',
                                                   'Products.ZenModel.Device.Device a.a.e.Fan'])


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
        c1 = self.zp.addComponentType('Foo')
        self.assertIsInstance(c1, Component)

    def test_addMemoizedComponent(self):
        c1 = self.zp.addComponentType('Component')
        c2 = self.zp.addComponentType('Component')
        self.assertIs(c1, c2)

    def test_ComponentId(self):
        c1 = self.zp.addComponentType('Component')
        self.assertEqual(c1.id, 'a.b.c.Component')


class TestZenPackRelationships(SimpleSetup):
    def test_oneToManyCont(self):
        self.zp.addRelation('Device', 'Vservers')
        self.zp.addRelation('Device', 'SystemNodes')
        self.zp.addRelation('Device', 'ClusterPeers')


class TestzProperties(SimpleSetup):
    def test_quotes(self):
        self.zp.addZProperty('foo', default='\'')
        self.assertEqual(self.zp.zproperties['foo'][1], '\'')

        self.zp.addZProperty('bar', default='\'bar')
        self.assertEqual(self.zp.zproperties['bar'][1], '\'bar\'')

        self.zp.addZProperty('baz', default='baz')
        self.assertEqual(self.zp.zproperties['baz'][1],'\'baz\'')


class TestZenPack(SimpleSetup):
    def testRepr(self):
        self.assertEqual(repr(self.zp), 'a.b.c \n\tAUTHOR: ZenossLabs <labs@zenoss.com>\n\tVERSION: 0.0.1\n\tLICENSE: gpl')

class TestWriteZenPack(WriteBase):

    def MyUpdateGitTemplatesMock(self):
        pass

    def testWrite(self):
        self.zp.updateGitTemplates = self.MyUpdateGitTemplatesMock
        dc = self.zp.addDeviceClass('Devices/Storage')
        dc.addComponentType('Component')
        self.write(self.zp)


if __name__ == '__main__':
        unittest.main()
