#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

import unittest
import os

from mock import mock_open, patch, MagicMock

from zpg import Component, DeviceClass, License, ZenPack, defaults

DEFAULT_NAME = 'a.b.c'


class SimpleSetup(unittest.TestCase):

    def setUp(self):
        self.zp = ZenPack(DEFAULT_NAME)

    def tearDown(self):
        del(self.zp)


class WriteBase(unittest.TestCase):

    def setUp(self):
        self.zp = ZenPack(DEFAULT_NAME)
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
        os.mkdir = self.mkdir
        os.makedirs = self.makedirs
        del(self.zp)


class TestZenPackInitialize(unittest.TestCase):
    #@unittest.skip("Skipping")

    def test_installRequires(self):
        self.assertEqual(
            ZenPack('a.a.a', install_requires='foo').install_requires, ['foo'])
        self.assertEqual(
            ZenPack('a.a.b', install_requires=['foo']).install_requires, ['foo'])

    def test_zProperties(self):
        zp = ZenPack('a.a.c', zProperties=[
                     {"type_": "boolean", "default": True, "Category": "NetBotz", "name": "zNetBotzExample"}, {"name": "e1"}])
        self.assertEqual(
            zp.zproperties, {'e1': ('e1', "''", 'string', None), 'zNetBotzExample': ('zNetBotzExample', True, 'boolean', 'NetBotz')})

    def test_deviceClasses(self):
        zp = ZenPack('a.a.d', deviceClasses=[{"path": "Device/Snmp"}])
        self.assertEqual(zp.deviceClasses.keys(), ['/zport/dmd/Device/Snmp'])

    def test_relationships(self):
        zp = ZenPack(
            'a.a.e', deviceClasses=[{"path": "Device/Snmp", "componentTypes": [{"name": "Enclosure"}, {"name": "TemperatureSensor"}, {"name": "Fan"}]}],
            relationships=[{"componentA": "Enclosure", "componentB": "Fan", "contained": False}])
        self.assertEqual(
            zp.relationships.keys(
            ), ['Products.ZenModel.Device.Device a.a.e.TemperatureSensor',
                        'a.a.e.Enclosure a.a.e.Fan',
                        'Products.ZenModel.Device.Device a.a.e.Enclosure',
                        'Products.ZenModel.Device.Device a.a.e.Fan'])


class TestZenPackLicense(SimpleSetup):

    def test_default(self):
        package_license = str(self.zp.license)
        defaults_license = str(License(self.zp, defaults.get("license", '')))
        self.assertEqual(package_license, defaults_license)


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
        self.assertEqual(self.zp.zproperties['baz'][1], '\'baz\'')


class TestZenPack(SimpleSetup):

    def testRepr(self):
        self.assertEqual(
            repr(self.zp), "\n".join([
                '%s ' % DEFAULT_NAME,  # the space is important at the end
                '\tAUTHOR: %s' % defaults.get('author'),
                '\tVERSION: %s' % defaults.get('version'),
                '\tLICENSE: %s' % defaults.get('license', 'GPL')]))


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
