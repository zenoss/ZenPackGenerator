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
from zpg.License import License


class SimpleSetup(unittest.TestCase):

    def setUp(self):
        from zpg.ZenPack import ZenPack
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
