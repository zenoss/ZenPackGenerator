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
from zpg import DeviceClass, Organizer, ZenPack


class SimpleSetup(unittest.TestCase):

    def setUp(self):
        self.zp = ZenPack('a.b.c')

    def tearDown(self):
        del(self.zp)


class TestOrganizerCreate(SimpleSetup):

    def test_addProperty(self):
        org = Organizer(
            self.zp, 'Devices/Server/Organizer', Type='DeviceClass')
        self.assertIsInstance(org, Organizer)

    def test_zPythonClassProperty(self):
        dc = DeviceClass(self.zp, 'Devices/Server/Organizer')
        org = Organizer(
            self.zp, 'Devices/Server/Organizer', Type='DeviceClass')
        self.assertEqual(dc.path, '/zport/dmd/Devices/Server/Organizer')
        self.assertEqual(dc.zPythonClass, 'Products.ZenModel.Device.Device')
        self.assertEqual(
            org.properties['zPythonClass'].value, 'Products.ZenModel.Device.Device')

if __name__ == '__main__':
    unittest.main()
