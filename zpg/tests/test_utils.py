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

from zpg._zenoss_utils import prepId, KlassExpand, zpDir
from zpg.ZenPack import ZenPack


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.zp = ZenPack('a.b.c')

    def tearDown(self):
        del(self.zp)

    def test_prepId(self):
        self.assertEqual(prepId('foo'), 'foo')
        self.assertNotEqual(prepId('foo'), 'foo1')

        self.assertEqual(prepId('a b'), 'a b')
        self.assertEqual(prepId('a\\b'), 'a_b')
        self.assertEqual(prepId('/a/b'), 'a_b')
        self.assertEqual(prepId('/a/\/b'), 'a___b')
        self.assertEqual(prepId('[a]'), 'a')
        self.assertEqual(prepId('/'), '-')
        self.assertEqual(prepId(u'abc'), 'abc')
        self.assertEqual(prepId(0), '0')
        with self.assertRaises(ValueError):
            prepId(None)

    def test_KlassExpand(self):
        self.assertEqual(KlassExpand(self.zp, 'Device'), 'a.b.c.Device')
        self.assertNotEqual(KlassExpand(self.zp, 'Device'), 'Device')
        self.assertEqual(KlassExpand(self.zp, 'a.b.c.Device'), 'a.b.c.Device')
        self.assertNotEqual(KlassExpand(self.zp, 'a.b.c.Device'), 'Device')
        self.assertEqual(
            KlassExpand(self.zp, 'Products.ZenModel.Device.Device'), 'Products.ZenModel.Device.Device')
        self.assertNotEqual(
            KlassExpand(self.zp, 'Products.ZenModel.Device.Device'), 'a.b.c.Device')

    def test_zpDir(self):
        self.assertEqual(zpDir(self.zp), 'a/b/c')
        self.assertNotEqual(zpDir(self.zp), 'Netapp/a/b/c')

if __name__ == '__main__':
        unittest.main()
