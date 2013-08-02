#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

import operator
import os
import unittest

from mock import mock_open, patch, call, MagicMock

from zpg import initpy, DirLayout, Defaults

DEFAULT_NAME = 'a.b.c'
DEFAULT_NAME2 = 'a.a.Template'

def zpg_home(self):
        return '/tests/'
Defaults.zpg_home = zpg_home

defaults = Defaults()

class SimpleSetup(unittest.TestCase):

    def setUp(self):
        from zpg.ZenPack import ZenPack
        self.zp = ZenPack(DEFAULT_NAME2)

    def tearDown(self):
        del(self.zp)


class DirectoryLayout(unittest.TestCase):

    def setUp(self):
        from zpg.ZenPack import ZenPack
        self.zp = ZenPack(DEFAULT_NAME)
        self.makedirs = os.makedirs
        self.mkdir = os.mkdir
        os.makedirs = MagicMock(return_value=True)
        os.mkdir = MagicMock(return_value=True)

    def tearDown(self):
        os.mkdir = self.mkdir
        os.makedirs = self.makedirs
        del(self.zp)


class testInitPy(SimpleSetup):
    #@unittest.skip("Skipping")

    def test_initpy(self):
        results = initpy('/tmp')
        self.assertEqual(results, '/tmp/__init__.py')


class TestDirectoryLayouts(DirectoryLayout):

    def test_directoryLayout(self):
        m = mock_open()
        dl = self.zp.destdir
        with patch('__builtin__.open', mock_open(read_data='fake data'), create=True) as m:
            dl.write()
            # Write File Handle
            wfh = m.return_value.__enter__.return_value
            self.results = wfh.write.call_args_list

            # Get the specific file calls that make up our writes
            top = defaults.get('prefix', os.getcwd())
            name = DEFAULT_NAME
            file_calls = [x
                          for x in m.mock_calls
                          if repr(x)[6:].startswith("%s/%s" % (top, name))]
            self.assertEqual(
                self.results, [
                    call(
                        "__import__('pkg_resources').declare_namespace(__name__)\n"),
                    call(
                        "__import__('pkg_resources').declare_namespace(__name__)\n"),
                    call(
                        "__import__('pkg_resources').declare_namespace(__name__)\n"),
                    call('graft ZenPacks\n')])
            self.assertEqual(
                file_calls, [
                    call('%s/%s/a/__init__.py' % (top, name), 'w'),
                    call('%s/%s/a/b/__init__.py' % (top, name), 'w'),
                    call('%s/%s/a/b/c/__init__.py' % (top, name), 'w'),
                    call('%s/%s/MANIFEST.in' % (top, name), 'w')])

if __name__ == '__main__':
    unittest.main()
