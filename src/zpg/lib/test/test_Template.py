import unittest
from zpg.lib.Template import Template
from mock import mock_open, patch

class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from zpg.lib.ZenPack import ZenPack
        self.zp = ZenPack('a.a.Template')

    def tearDown(self):
        del(self.zp)

class TestTemplateCacheLocation(SimpleSetup):
    def test_templateCacheLocation(self):
        t=Template(self.zp)
        t.dest_file='foo.py'
        self.assertEqual(t.TemplateCacheLocation(), '/tmp/zpg/a.a.Template/Templates/foo.py.tmpl')

#class TestCacheTemplate(SimpleSetup):
#    def testCaching(self):
#        m = mock_open()
#        with patch('__main__.open', m, create=True):
#            with open('foo.py.tmpl', 'w') as f:
#                f.write('#Foo Template')
#
#        t = Template(self.zp)
#        t.dest_file='foo.py'
#        t.tfile='foo.py.tmpl'
##        t.cacheTemplate()


if __name__ == '__main__':
    unittest.main()
