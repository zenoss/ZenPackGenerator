import unittest
from zpg.lib.ZenPack import ZenPack
from zpg.lib.Property import Property


class SimpleSetup(unittest.TestCase):
    def setUp(self):
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
