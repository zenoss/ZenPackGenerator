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
import inspect

from mock import mock_open, patch, call, MagicMock

import zpg
from zpg import Template, ZenPack, defaults

DEFAULT_NAME = 'a.b.c'
DEFAULT_NAME2 = 'a.a.Template'


class SimpleSetup(unittest.TestCase):

    def setUp(self):
        self.zp = ZenPack(DEFAULT_NAME2)

    def tearDown(self):
        del(self.zp)


class WriteTemplatesBase(unittest.TestCase):

    def setUp(self):
        from zpg.ZenPack import ZenPack
        self.zp = ZenPack(DEFAULT_NAME)
        self.makedirs = os.makedirs

        os.makedirs = MagicMock(return_value=True)

    def write(self, obj, template):
        m = mock_open()
        with patch('__builtin__.open', mock_open(read_data=template), create=True) as m:
            obj.dest_file = 'dummy_dest_file.py'
            obj.tfile = 'dummy_tfile'
            obj.source_template = 'dummy_source_template.tmpl'
            obj.processTemplate()

            # Write File Handle
            wfh = m.return_value.__enter__.return_value
            self.results = wfh.write.call_args_list

    def tearDown(self):
        print "Calling teardown"
        os.makedirs = self.makedirs
        del(self.zp)


class TestTemplateCacheLocation(SimpleSetup):

    def test_templateCacheLocation(self):
        t = Template(self.zp)
        t.dest_file = 'foo.py'
        top = defaults.get('prefix', os.getcwd())
        self.assertEqual(t.TemplateCacheLocation(),
                         '%s/%s/Templates/foo.py.tmpl' % (top, DEFAULT_NAME2))


class TestCacheTemplate(SimpleSetup):

    def testCaching(self):
        m = mock_open()
        os.makedirs = MagicMock(return_value=True)
        with patch('__builtin__.open', mock_open(read_data='Source Template'), create=True) as m:
            t = Template(self.zp)
            t.dest_file = 'foo.py'
            t.tfile = 'foo.py.tmpl'
            t.cacheTemplate()

        # Write File Handle
        wfh = m.return_value.__enter__.return_value
        self.assertEqual(wfh.write.call_args_list, [
                         call('## Source Template foo.py.tmpl \n'), call('Source Template')])


class FindTemplate(SimpleSetup):

    def test_findingTemplate(self):
        t = Template(self.zp)
        t.dest_file = 'foo.py'
        t.tfile = 'foo.py.tmpl'
        self.source_template = 'foo.tmpl'
        t.findTemplate()
        self.assertEqual(t.tfile, "%s/Templates/%s" %
                         ("/".join(inspect.getfile(zpg).split('/')[:-1]), t.source_template))

    def test_findCachedLocation(self):
        t = Template(self.zp)
        exists = os.path.exists
        os.path.exists = MagicMock(return_value=True)
        t.dest_file = 'foo.py'
        t.tfile = 'foo.py.tmpl'
        self.source_template = 'foo.tmpl'
        t.findTemplate()
        self.assertEqual(t.tfile, t.TemplateCacheLocation())
        os.path.exists = exists


class TestWriteTemplate(WriteTemplatesBase):

    def test_processTemplate(self):
        t = Template(self.zp)
        self.write(t, '${zenpack.id}\n${zenpack.version}\n')
        name = DEFAULT_NAME
        version = defaults.get('version')
        self.assertEqual(self.results[-1], call(u'%s\n%s\n' % (name, version)))


if __name__ == '__main__':
    unittest.main()
