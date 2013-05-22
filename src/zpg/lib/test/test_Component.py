import unittest
from zpg.lib.Component import Component
from zpg.lib.Relationship import Relationship

class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from zpg.lib.ZenPack import ZenPack
        self.zp = ZenPack('a.b.c')

    def teardown(self):
        print "Calling teardown"
        del(self.zp)


class TestComponentCreate(SimpleSetup):
    #@unittest.skip("Skipping")
    def test_ComponentCreate(self):
        c = Component(self.zp, 'Component')
        self.assertIsInstance(c, Component)


class TestNames(SimpleSetup):
    def test_name_default(self):
        c = Component(self.zp, 'Component')
        self.assertEqual(c.names, 'Components')

    def test_name_overridden(self):
        c = Component(self.zp, 'Component', names='names')
        self.assertEqual(c.names, 'names')


class TestComponentUniqueName(SimpleSetup):
    def test_uniquename_default(self):
        c = Component(self.zp, 'Component')
        self.assertEqual(c.portal_type, 'Component')
        self.assertEqual(c.meta_type, 'Component')
        self.assertEqual(c.unique_name, 'Component')

    def test_meta_type_Overridden(self):
        c = Component(self.zp, 'Component', meta_type='unique')
        self.assertNotEqual(c.portal_type, 'Component')
        self.assertNotEqual(c.meta_type, 'Component')
        self.assertNotEqual(c.unique_name, 'Component')
        self.assertEqual(c.portal_type, 'unique')
        self.assertEqual(c.meta_type, 'unique')
        self.assertEqual(c.unique_name, 'unique')


class TestComponentClasses(SimpleSetup):
    def test_classes_default(self):
        c = Component(self.zp, 'Component')
        self.assertEqual(c.klasses, ['Products.ZenModel.DeviceComponent.DeviceComponent',
                                     'Products.ZenModel.ManagedEntity.ManagedEntity'])

    def test_classes_shorthand(self):
        c = Component(self.zp, 'Component', klasses=['DeviceComponent',
                                                     'ManagedEntity'])
        self.assertEqual(c.klasses, ['Products.ZenModel.DeviceComponent.DeviceComponent',
                                     'Products.ZenModel.ManagedEntity.ManagedEntity'])

    def test_classes_NonDefault(self):
        c = Component(self.zp, 'Component', klasses=['zenpacks.zenoss.Test.Test'])
        self.assertEqual(c.klasses, ['zenpacks.zenoss.Test.Test'])

    def test_classes_NonArray(self):
        c = Component(self.zp, 'Component', klasses='zenpacks.zenoss.Test.Test')
        self.assertEqual(c.klasses, ['zenpacks.zenoss.Test.Test'])

    def test_classes_zenpack_namespace(self):
        Component(self.zp, 'Test')
        c = Component(self.zp, 'Component', klasses=['Test'])
        self.assertEqual(c.klasses, ['a.b.c.Test'])

    def test_classes_zenpack_outside_namespace(self):
        c = Component(self.zp, 'Component', klasses=['OperatingSystem'])
        self.assertEqual(c.klasses, ['Products.ZenModel.OperatingSystem.OperatingSystem'])


class TestComponentImports(SimpleSetup):
    def test_imports_default(self):
        c = Component(self.zp, 'Component')
        self.assertEqual(c.imports, ['from zope.interface import implements',
                                     'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
                                     'from Products.Zuul.decorators import info',
                                     'from Products.Zuul.form import schema',
                                     'from Products.Zuul.infos import ProxyProperty',
                                     'from Products.Zuul.utils import ZuulMessageFactory as _t',
                                     'from Products.ZenModel.DeviceComponent import DeviceComponent',
                                     'from Products.ZenModel.ManagedEntity import ManagedEntity'])

    def test_imports_overridden(self):
        c = Component(self.zp, 'Component', imports=['from zope.interface import implements'])
        self.assertEqual(c.imports, ['from zope.interface import implements',
                                     'from Products.ZenModel.DeviceComponent import DeviceComponent',
                                     'from Products.ZenModel.ManagedEntity import ManagedEntity'])

    def test_imports_string(self):
        c = Component(self.zp, 'Component', imports='from zope.interface import implements')
        self.assertEqual(c.imports, ['from zope.interface import implements',
                                     'from Products.ZenModel.DeviceComponent import DeviceComponent',
                                     'from Products.ZenModel.ManagedEntity import ManagedEntity'])

    def test_imports_with_classes(self):
        c = Component(self.zp, 'Component',
                      klasses=['Products.ZenModel.OSComponent.OSComponent',
                               'Products.ZenModel.Linkable.Layer2Linkable'
                               ]
                      )

        c2 = Component(self.zp, 'Component2',
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

class TestComponentNameSpace(SimpleSetup):
    def test_namespace_default(self):
        c = Component(self.zp, 'Component')
        self.assertEqual(c.namespace, 'a.b.c')

    def test_namespace_overridden(self):
        c = Component(self.zp, 'Component', namespace='a.a.a')
        self.assertEqual(c.namespace, 'a.a.a')


class TestComponentProperties(SimpleSetup):
    def test_Property_default(self):
        c = Component(self.zp, 'Component')
        c.addProperty('oids')
        self.assertEqual(c.properties.keys(), ['oids'])

    def test_Property_extraParams(self):
        c = Component(self.zp, 'Component')
        c.addProperty('oids', Type='int', value=2)
        self.assertEqual(c.properties['oids'].Type, 'int')
        self.assertEqual(c.properties['oids'].value, 2)

    def test_Property_init_dict(self):
        c = Component(self.zp, 'Component', properties=[{"name": "port"}])
        self.assertEqual(c.properties.keys(), ['port'])

class TestSubComponent(SimpleSetup):
    def test_ComponentType_init_dict(self):
        c = Component(self.zp, 'Component', componentTypes=[{"name": "Blade"}])
        self.assertEqual(c.components.keys(), ['a.b.c.Blade'])

    def test_addComponent(self):
        c = Component(self.zp, 'Component')
        c.addComponentType('SubComponent')
        self.assertEqual(c.components.keys(), ['a.b.c.SubComponent'])

class TestComponentType(SimpleSetup):
    def test_ComponentType_Component(self):
        c = Component(self.zp, 'Component')
        self.assertEqual(c.Type(), 'Component')

        d = Component(self.zp, 'Device', device=True)
        self.assertEqual(d.Type(), 'Device')

class TestKlassNames(SimpleSetup):
    def test_klassNames_Default(self):
        c = Component(self.zp, 'Component')
        self.assertEqual(c.klassNames(), ['DeviceComponent', 'ManagedEntity'])

class TestFindRelationships(SimpleSetup):
    def test_findRelationships(self):
        c = self.zp.addComponentType('Component')
        c.addComponentType('SubComponent')
        self.assertEqual([r.id for r in c.relations()], ['a.b.c.Component a.b.c.SubComponent'])

class TestCustomPaths(SimpleSetup):
    def test_findCustomPaths(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        dc.addComponentType('Enclosure')
        b = dc.addComponentType('Blade')
        f = dc.addComponentType('Fan')

        Relationship(self.zp, 'Enclosure', 'Fan', Type='1-M', Contained=False)
        Relationship(self.zp, 'Enclosure', 'Blade', Type='1-M', Contained=False)

        self.assertEqual([c.id for c in f.custompaths()['1-M'][0]], ['a.b.c.Enclosure', 'a.b.c.d.Device'])
        self.assertEqual([c.id for c in b.custompaths()['1-M'][0]], ['a.b.c.Enclosure', 'a.b.c.d.Device'])

class TestDropDownComponents(SimpleSetup):
    def test_findDropDownComponents(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        dc.addComponentType('Enclosure')
        f = dc.addComponentType('Fan')
        Relationship(self.zp, 'Enclosure', 'Fan', Type='1-M', Contained=False)
        self.assertEqual([c.id for c in f.dropdowncomponents()], ['a.b.c.Enclosure'])

class TestManyRelationships(SimpleSetup):
    def test_findManyRelationships(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e=dc.addComponentType('a.Enclosure')
        e.addComponentType('Drive')
        self.assertEqual([r.id for r in e.ManyRelationships()],['a.Enclosure a.b.c.Drive'])

class TestRelationshipsToStrings(SimpleSetup):
    def test_findManyRelationships(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e=dc.addComponentType('a.Enclosure')
        e.addComponentType('Drive')
        self.assertEqual([r.id for r in e.ManyRelationships()],['a.Enclosure a.b.c.Drive'])

if __name__ == '__main__':
    unittest.main()
