#!/usr/bin/env python
import unittest
import os
import operator
from zpg.lib.DirLayout import initpy, DirLayout
from mock import mock_open, patch, call, MagicMock


class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from zpg.lib.ZenPack import ZenPack
        self.zp = ZenPack('a.a.Template')

    def tearDown(self):
        del(self.zp)


class DirectoryLayout(unittest.TestCase):
    def setUp(self):
        from zpg.lib.ZenPack import ZenPack
        self.zp = ZenPack('a.b.c')
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
        file_calls = [x for x in operator.itemgetter(0,3,6,9)(m.mock_calls)]
        self.assertEqual(self.results, [call("__import__('pkg_resources').declare_namespace(__name__)\n"),
                                        call("__import__('pkg_resources').declare_namespace(__name__)\n"),
                                        call("__import__('pkg_resources').declare_namespace(__name__)\n"),
                                        call('graft ZenPacks\n')])

        self.assertEqual(file_calls, [call('/tmp/zpg/a.b.c/a/__init__.py', 'w'),
                                      call('/tmp/zpg/a.b.c/a/b/__init__.py', 'w'),
                                      call('/tmp/zpg/a.b.c/a/b/c/__init__.py', 'w'),
                                      call('/tmp/zpg/a.b.c/MANIFEST.in', 'w')])



if __name__ == '__main__':
    unittest.main()
