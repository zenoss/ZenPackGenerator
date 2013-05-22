import unittest
from zpg.lib.Relationship import Relationship


class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from zpg.lib.ZenPack import ZenPack
        self.zp = ZenPack('a.a.Configure')

    def tearDown(self):
        print "Calling teardown"
        del(self.zp)


class TestCustomPaths(SimpleSetup):
    def test_findCustomPathsTrue(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        dc.addComponentType('Enclosure')
        dc.addComponentType('Blade')
        dc.addComponentType('Fan')

        Relationship(self.zp, 'Enclosure', 'Fan', Type='1-M', Contained=False)
        Relationship(self.zp, 'Enclosure', 'Blade', Type='1-M', Contained=False)
        self.assertTrue(self.zp.configure_zcml.customPathReporters())

    def test_findCustomPathsFalse(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='Device')
        dc.addComponentType('Enclosure')
        dc.addComponentType('Blade')
        dc.addComponentType('Fan')
        self.assertFalse(self.zp.configure_zcml.customPathReporters())

if __name__ == '__main__':
    unittest.main()
