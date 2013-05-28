#!/usr/bin/env python
import unittest
import os
from mock import mock_open, patch, call, MagicMock
from zpg.lib.Template import Template
import inspect
import zpg


class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from zpg.lib.ZenPack import ZenPack
        self.zp = ZenPack('a.a.Template')

    def tearDown(self):
        del(self.zp)


class WriteTemplatesBase(unittest.TestCase):
    def setUp(self):
        from zpg.lib.ZenPack import ZenPack
        self.zp = ZenPack('a.b.c')
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
        self.assertEqual(t.TemplateCacheLocation(), '/tmp/zpg/a.a.Template/Templates/foo.py.tmpl')


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
        self.assertEqual(wfh.write.call_args_list, [call('## Source Template foo.py.tmpl \n'), call('Source Template')])


class FindTemplate(SimpleSetup):
    def test_findingTemplate(self):
        t = Template(self.zp)
        t.dest_file = 'foo.py'
        t.tfile = 'foo.py.tmpl'
        self.source_template = 'foo.tmpl'
        t.findTemplate()
        self.assertEqual(t.tfile, "%s/Templates/%s" % ("/".join(inspect.getfile(zpg).split('/')[:-1]), t.source_template))

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
    #@unittest.skip("Skipping")
    def test_processTemplate(self):
        t = Template(self.zp)
        self.write(t, '${zenpack.id}\n${zenpack.version}\n')
        self.assertEqual(self.results[-1], call(u'a.b.c\n0.0.1\n'))


if __name__ == '__main__':
    unittest.main()
