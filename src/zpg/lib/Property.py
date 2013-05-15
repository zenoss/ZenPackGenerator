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
import inflect

plural = inflect.engine().plural


class Property(object):
    def __init__(self,
                 id,
                 value=None,
                 Type=None,
                 width=10,
                 detailDisplay=True,
                 gridDisplay=True,
                 sortable=True,
                 panelRenderer=None):

        self.id = id
        self.name = id
        self.names = plural(id)
        self.mode = 'w'
        self.value = value
        self.detailDisplay = detailDisplay
        self.gridDisplay = gridDisplay
        self.sortable = True
        self.width = width
        self.panelRenderer = panelRenderer

        if Type:
            self.Type = Type
        else:
            self.Type = value

        self.value = value

    def Schema(self):
        if self.Type in ['int']:
            return 'Int'
        elif self.Type in ['string', 'text', 'lines']:
            return 'TextLine'
        elif self.Type in ['bool']:
            return 'Bool'
        else:
            return 'TextLine'

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = None

        # Zope Types we are supporting
        ValidTypes = ['string', 'text', 'lines',
                      'int', 'bool', 'long', 'boolean',
                      'float', 'password']

        # All Zope types
        #boolean,date,float,int,lines,
        #long,string,text,tokens,selection,multiple_selection

        if Type and Type in ValidTypes:
            self._Type = Type
        else:
            if isinstance(Type, str):
                self._Type = 'string'

            elif isinstance(Type, bool):
                self._Type = 'boolean'

            elif isinstance(Type, int):
                self._Type = 'int'

            elif isinstance(Type, float):
                self._Type = 'float'

            elif isinstance(Type, list):
                self._Type = 'lines'

        # Default return of string
        if not self._Type:
            self._Type = 'string'

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # Valid values can be implemented later.
        if value is None:
            self._value = 'None'
        else:
            self._value = value

    def __call__(self):
        return self.value


class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from ZenPack import ZenPack
        self.zp = ZenPack('a.b.c')


class TestPropertyCreate(SimpleSetup):
    def test_addProperty(self):
        cp1 = Property('blocksize', Type='string')
        cp2 = Property('raid_size', Type='int')
        cp3 = Property('checksum_enabled', Type='boolean')
        self.assertIsInstance(cp1, Property)
        self.assertIsInstance(cp2, Property)
        self.assertIsInstance(cp3, Property)

    def test_addPropertyDefaultValues(self):
        cp1 = Property('blocksize', Type='string')
        cp2 = Property('raid_size', Type='int')
        cp3 = Property('checksum_enabled', Type='boolean')
        self.assertEqual(cp1.value, 'None')
        self.assertEqual(cp2.value, 'None')
        self.assertEqual(cp3.value, 'None')

    def test_addPropertyTypes(self):
        cp1 = Property('blocksize', Type='string')
        cp2 = Property('raid_size', Type='int')
        cp3 = Property('checksum_enabled', Type='boolean')
        cp4 = Property('string', value='a')
        cp5 = Property('int', value=1)
        cp6 = Property('float', value=1.0)
        cp7 = Property('lines', value=['a', 'b'])
        self.assertEqual(cp1.Type, 'string')
        self.assertEqual(cp2.Type, 'int')
        self.assertEqual(cp3.Type, 'boolean')
        self.assertEqual(cp4.Type, 'string')
        self.assertEqual(cp5.Type, 'int')
        self.assertEqual(cp6.Type, 'float')
        self.assertEqual(cp7.Type, 'lines')

    def test_addPropertyValuesInit(self):
        cp1 = Property('blocksize', Type='string', value='3')
        cp2 = Property('raid_size', Type='int', value=2)
        cp3 = Property('checksum_enabled', Type='boolean', value=True)
        cp4 = Property('checksum_enabled', Type='lines', value=['a', 'b'])
        self.assertEqual(cp1.value, '3')
        self.assertEqual(cp2.value, 2)
        self.assertEqual(cp3.value, True)
        self.assertEqual(cp4.value, ['a', 'b'])

if __name__ == "__main__":
    unittest.main()
