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


class DeviceClass(object):
    def __init__(self, path, ZenPack, prefix='/zport/dmd'):
        self.ZenPack = ZenPack
        self.path = '/'.join([prefix, path.lstrip('/')])
        self.subClasses = {}

    @property
    def id(self):
        return self.path

    @property
    def portal_type(self):
        return self.unique_name

    @property
    def meta_type(self):
        return self.unique_name

    def addProperty(self, id, type, default):
        pass

    #memoize
    def addSubClass(self,path):
        return DeviceClass(path=path, prefix=self.path)

    def __repr__(self):
        return "DeviceClass @ <%s>" % self.path


# Unit Tests Start here
class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from ZenPack import ZenPack
        self.zp = ZenPack('a.b.c')


class TestDeviceClassCreate(SimpleSetup):
    def test_addDeviceClass(self):
        dc1 = DeviceClass('Devices/Storage/DC1', self.zp)
        self.assertIsInstance(dc1, DeviceClass)

if __name__ == "__main__":
    unittest.main()
