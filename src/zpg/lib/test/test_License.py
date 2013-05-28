#!/usr/bin/env python
import unittest
from zpg.lib.License import License

class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from zpg.lib.ZenPack import ZenPack
        self.zp = ZenPack('a.a.Template')

    def tearDown(self):
        del(self.zp)


class TestLicenseHeader(SimpleSetup):
    #@unittest.skip("Skipping")
    def testHeader(self):
        l = License('gpl')
        self.assertEqual(l.header(), '#LICENSE HEADER SAMPLE')


if __name__ == '__main__':
    unittest.main()
