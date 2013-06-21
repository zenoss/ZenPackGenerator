import unittest
from zpg.lib.ZenPack import ZenPack
from zpg.lib.Property import Property


class SimpleSetup(unittest.TestCase):
    def setUp(self):
        self.zp = ZenPack('a.b.c')

    def tearDown(self):
        del(self.zp)


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
        cp8 = Property('checksum_enabled', value=True)
        self.assertEqual(cp1.Type, 'string')
        self.assertEqual(cp2.Type, 'int')
        self.assertEqual(cp3.Type, 'boolean')
        self.assertEqual(cp4.Type, 'string')
        self.assertEqual(cp5.Type, 'int')
        self.assertEqual(cp6.Type, 'float')
        self.assertEqual(cp7.Type, 'lines')
        self.assertEqual(cp8.Type, 'boolean')

    def test_addPropertyValuesInit(self):
        cp1 = Property('blocksize', Type='string', value='3')
        cp2 = Property('raid_size', Type='int', value=2)
        cp3 = Property('checksum_enabled', Type='boolean', value=True)
        cp4 = Property('checksum_enabled', Type='lines', value=['a', 'b'])
        self.assertEqual(cp1.value, '3')
        self.assertEqual(cp2.value, 2)
        self.assertEqual(cp3.value, True)
        self.assertEqual(cp4.value, ['a', 'b'])

class TestPropertySchema(SimpleSetup):
    def testInt(self):
        cp1 = Property('Int', Type='int')
        self.assertEqual(cp1.Schema(), 'Int')

    def testText(self):
        string1 = Property('String', Type='string')
        text1 = Property('Text', Type='text')
        lines1 = Property('Lines', Type='lines')
        self.assertEqual(string1.Schema(), 'TextLine')
        self.assertEqual(text1.Schema(), 'TextLine')
        self.assertEqual(lines1.Schema(), 'TextLine')

    def testBool(self):
        bool1 = Property('Bool', Type='bool')
        self.assertEqual(bool1.Schema(), 'Bool')

    def testFallthrough(self):
        ft = Property('FallThrough', Type='long')
        self.assertEqual(ft.Schema(), 'TextLine')

if __name__ == '__main__':
    unittest.main()
