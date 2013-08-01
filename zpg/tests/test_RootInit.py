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
import os

from mock import mock_open, patch, call, MagicMock

from zpg import ZenPack, defaults

DEFAULT_NAME = 'a.b.c'


class WriteTemplatesBase(unittest.TestCase):

    def setUp(self):
        self.zp = ZenPack(DEFAULT_NAME)
        self.makedirs = os.makedirs

        os.makedirs = MagicMock(return_value=True)

    def write(self, obj, template):
        m = mock_open()
        with patch('__builtin__.open', mock_open(read_data=template), create=True) as m:
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

    def test_processTemplate(self):
        self.write(self.zp.rootinit, '${zenpack.id}\n${zenpack.version}\n')
        name = DEFAULT_NAME
        version = defaults.get('version')
        self.assertEqual(self.results[-1], call(u'%s\n%s\n' % (name, version)))


if __name__ == '__main__':
    unittest.main()
