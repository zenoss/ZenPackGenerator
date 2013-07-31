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
from zpg.ZenPack import ZenPack
from zpg.Property import Property


class SimpleSetup(unittest.TestCase):

    def setUp(self):
        self.zp = ZenPack('a.b.c')

    def tearDown(self):
        del(self.zp)


class TestPropertyCreate(SimpleSetup):

    def test_addProperty(self):
        cp1 = Property('blocksize', type_='string')
        cp2 = Property('raid_size', type_='int')
        cp3 = Property('checksum_enabled', type_='boolean')
        self.assertIsInstance(cp1, Property)
        self.assertIsInstance(cp2, Property)
        self.assertIsInstance(cp3, Property)

    def test_addPropertyDefaultValues(self):
        cp1 = Property('blocksize', type_='string')
        cp2 = Property('raid_size', type_='int')
        cp3 = Property('checksum_enabled', type_='boolean')
        self.assertEqual(cp1.value, 'None')
        self.assertEqual(cp2.value, 'None')
        self.assertEqual(cp3.value, 'None')

    def test_addPropertyTypes(self):
        cp1 = Property('blocksize', type_='string')
        cp2 = Property('raid_size', type_='int')
        cp3 = Property('checksum_enabled', type_='boolean')
        cp4 = Property('string', value='a')
        cp5 = Property('int', value=1)
        cp6 = Property('float', value=1.0)
        cp7 = Property('list', value=['a', 'b'])
        cp8 = Property('checksum_enabled', value=True)
        self.assertEqual(cp1.type_, 'string')
        self.assertEqual(cp2.type_, 'int')
        self.assertEqual(cp3.type_, 'boolean')
        self.assertEqual(cp4.type_, 'string')
        self.assertEqual(cp5.type_, 'int')
        self.assertEqual(cp6.type_, 'float')
        self.assertEqual(cp7.type_, 'list')
        self.assertEqual(cp8.type_, 'boolean')

    def test_addPropertyValuesInit(self):
        cp1 = Property('blocksize', type_='string', value='3')
        cp2 = Property('raid_size', type_='int', value=2)
        cp3 = Property('checksum_enabled', type_='boolean', value=True)
        cp4 = Property('checksum_enabled', type_='list', value=['a', 'b'])
        self.assertEqual(cp1.value, '3')
        self.assertEqual(cp2.value, 2)
        self.assertEqual(cp3.value, True)
        self.assertEqual(cp4.value, ['a', 'b'])


class TestPropertySchema(SimpleSetup):

    def testInt(self):
        cp1 = Property('Int', type_='int')
        self.assertEqual(cp1.Schema(), 'Int')

    def testText(self):
        string1 = Property('String', type_='string')
        text1 = Property('Text', type_='text')
        list1 = Property('Lines', type_='list')
        self.assertEqual(string1.Schema(), 'TextLine')
        self.assertEqual(text1.Schema(), 'TextLine')
        self.assertEqual(list1.Schema(), 'TextLine')

    def testBool(self):
        bool1 = Property('Bool', type_='bool')
        self.assertEqual(bool1.Schema(), 'Bool')

    def testFallthrough(self):
        ft = Property('FallThrough', type_='long')
        self.assertEqual(ft.Schema(), 'TextLine')

if __name__ == '__main__':
    unittest.main()
