import unittest
from zpg.lib.Component import Component


class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from zpg.lib.ZenPack import ZenPack
        self.zp = ZenPack('a.b.c')


class TestComponentCreate(SimpleSetup):
    #@unittest.skip("Skipping")
    def test_ComponentCreate(self):
        c = Component('Component', self.zp)
        self.assertIsInstance(c, Component)


class TestNames(SimpleSetup):
    def test_name_default(self):
        c = Component('Component', self.zp)
        self.assertEqual(c.names, 'Components')

    def test_name_overridden(self):
        c = Component('Component', self.zp, names='names')
        self.assertEqual(c.names, 'names')


class TestComponentUniqueName(SimpleSetup):
    def test_uniquename_default(self):
        c = Component('Component', self.zp)
        self.assertEqual(c.portal_type, 'Component')
        self.assertEqual(c.meta_type, 'Component')
        self.assertEqual(c.unique_name, 'Component')

    def test_meta_type_Overridden(self):
        c = Component('Component', self.zp, meta_type='unique')
        self.assertNotEqual(c.portal_type, 'Component')
        self.assertNotEqual(c.meta_type, 'Component')
        self.assertNotEqual(c.unique_name, 'Component')
        self.assertEqual(c.portal_type, 'unique')
        self.assertEqual(c.meta_type, 'unique')
        self.assertEqual(c.unique_name, 'unique')


class TestComponentClasses(SimpleSetup):
    def test_classes_default(self):
        c = Component('Component', self.zp)
        self.assertEqual(c.klasses, ['Products.ZenModel.DeviceComponent.DeviceComponent',
                                     'Products.ZenModel.ManagedEntity.ManagedEntity'])

    def test_classes_shorthand(self):
        c = Component('Component', self.zp, klasses=['DeviceComponent',
                                                     'ManagedEntity'])
        self.assertEqual(c.klasses, ['Products.ZenModel.DeviceComponent.DeviceComponent',
                                     'Products.ZenModel.ManagedEntity.ManagedEntity'])

    def test_classes_NonDefault(self):
        c = Component('Component', self.zp, klasses=['zenpacks.zenoss.Test.Test'])
        self.assertEqual(c.klasses, ['zenpacks.zenoss.Test.Test'])

    def test_classes_NonArray(self):
        c = Component('Component', self.zp, klasses='zenpacks.zenoss.Test.Test')
        self.assertEqual(c.klasses, ['zenpacks.zenoss.Test.Test'])


class TestComponentImports(SimpleSetup):
    def test_imports_default(self):
        c = Component('Component', self.zp)
        self.assertEqual(c.imports, ['from zope.interface import implements',
                                     'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
                                     'from Products.Zuul.decorators import info',
                                     'from Products.Zuul.form import schema',
                                     'from Products.Zuul.infos import ProxyProperty',
                                     'from Products.Zuul.utils import ZuulMessageFactory as _t',
                                     'from Products.ZenModel.DeviceComponent import DeviceComponent',
                                     'from Products.ZenModel.ManagedEntity import ManagedEntity'])

    def test_imports_overridden(self):
        c = Component('Component', self.zp, imports=['from zope.interface import implements'])
        self.assertEqual(c.imports, ['from zope.interface import implements',
                                     'from Products.ZenModel.DeviceComponent import DeviceComponent',
                                     'from Products.ZenModel.ManagedEntity import ManagedEntity'])

    def test_imports_string(self):
        c = Component('Component', self.zp, imports='from zope.interface import implements')
        self.assertEqual(c.imports, ['from zope.interface import implements',
                                     'from Products.ZenModel.DeviceComponent import DeviceComponent',
                                     'from Products.ZenModel.ManagedEntity import ManagedEntity'])

    def test_imports_with_classes(self):
        c = Component('Component', self.zp,
                      klasses=['Products.ZenModel.OSComponent.OSComponent',
                               'Products.ZenModel.Linkable.Layer2Linkable'
                               ]
                      )

        c2 = Component('Component2', self.zp,
                       klasses=['Products.ZenModel.Software.Software',
                                ]
                       )

        self.maxDiff = None
        self.assertEqual(c.imports, ['from zope.interface import implements',
                                     'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
                                     'from Products.Zuul.decorators import info',
                                     'from Products.Zuul.form import schema',
                                     'from Products.Zuul.infos import ProxyProperty',
                                     'from Products.Zuul.utils import ZuulMessageFactory as _t',
                                     'from Products.ZenModel.OSComponent import OSComponent',
                                     'from Products.ZenModel.Linkable import Layer2Linkable',
                                     ])

        self.assertEqual(c2.imports, ['from zope.interface import implements',
                                      'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
                                      'from Products.Zuul.decorators import info',
                                      'from Products.Zuul.form import schema',
                                      'from Products.Zuul.infos import ProxyProperty',
                                      'from Products.Zuul.utils import ZuulMessageFactory as _t',
                                      'from Products.ZenModel.Software import Software',
                                      ])
# custom path reporter test setup  (1-M)
#    zp = ZenPack('ZenPacks.zenoss.NetAppMonitor')
#    v = zp.addComponent('Volume')
#    vs = zp.addComponent('VServer')
#    zp.addComponent('Device')
#    zp.addRelation('VServer', 'Volume', Type='1-M', Contained=False)
#    zp.addRelation('Filer', 'VServer')
#    zp.addRelation('Device', 'VServer')
## Should generate something like this
#    obj = self.context.vserver()
#    if obj:
#        paths.extend(relPath(obj,'filer'))


class TestComponentProperties(SimpleSetup):
    def test_Property_default(self):
        c = Component('Component', self.zp)
        c.addProperty('oids')
        self.assertEqual(c.properties.keys(), ['oids'])

    def test_Property_extraParams(self):
        c = Component('Component', self.zp)
        c.addProperty('oids', Type='int', value=2)
        self.assertEqual(c.properties['oids'].Type, 'int')
        self.assertEqual(c.properties['oids'].value, 2)
