#!/usr/bin/env python
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

import unittest
import os

from mock import mock_open, patch, call, MagicMock

from zpg.ZenPack import ZenPack, defaults


class SimpleSetup(unittest.TestCase):

    def setUp(self):
        from zpg.ZenPack import ZenPack
        self.zp = ZenPack('a.a.Template')

    def tearDown(self):
        del(self.zp)


class WriteTemplatesBase(unittest.TestCase):

    def setUp(self):
        self.zp = ZenPack('a.b.c')
        self.makedirs = os.makedirs
        os.makedirs = MagicMock(return_value=True)

    def write(self, obj, template):
        m = mock_open()
        cmd = '__builtin__.open'
        with patch(cmd, mock_open(read_data=template), create=True) as m:
            obj.dest_file = 'dummy_dest_file.py'
            obj.tfile = 'dummy_tfile'
            obj.source_template = 'dummy_source_template.tmpl'
            obj.write()

            # Write File Handle
            wfh = m.return_value.__enter__.return_value
            self.results = wfh.write.call_args_list

    def tearDown(self):
        os.makedirs = self.makedirs
        del(self.zp)


class TestWriteTemplate(WriteTemplatesBase):
    #@unittest.skip("Skipping")

    def test_processTemplate(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        dc.addComponentType('Enclosure')
        self.write(self.zp.zenpackUI, '${zenpack.id}\n${zenpack.version}\n')
        version = defaults.get('version')
        self.assertEqual(self.results[-1], call(u'a.b.c\n%s\n' % version))


if __name__ == '__main__':
    unittest.main()
