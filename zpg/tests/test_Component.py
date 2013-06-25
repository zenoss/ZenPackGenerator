import __builtin__
import os
import unittest

from mock import mock_open, patch, call, MagicMock

from zpg import Component, Relationship, ZenPack, Opts, defaults

DEFAULT_NAME = 'a.b.c'


class SimpleSetup(unittest.TestCase):

    def setUp(self):
        if hasattr(self, 'zp'):
            del(self.zp)
        self.zp = ZenPack(DEFAULT_NAME, opts=Opts())

    def tearDown(self):
        print "Calling teardown"
        del(self.zp)


class WriteTemplatesBase(unittest.TestCase):

    def setUp(self):
        self.zp = ZenPack(DEFAULT_NAME, opts=Opts())
        self.makedirs = os.makedirs

        os.makedirs = MagicMock(return_value=True)

    def write(self, Component, template):
        with patch('__builtin__.open',
                   mock_open(read_data=template), create=True) as m:
            Component.dest_file = 'dummy_dest_file.py'
            Component.tfile = 'dummy_tfile'
            Component.source_template = 'dummy_source_template.tmpl'
            Component.write()

            # Write File Handle
            wfh = m.return_value.__enter__.return_value
            self.results = wfh.write.call_args_list

    def tearDown(self):
        print "Calling teardown"
        os.makedirs = self.makedirs
        del(self.zp)


class TestComponentCreate(SimpleSetup):

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
        self.assertEqual(
            c.klasses, ['Products.ZenModel.DeviceComponent.DeviceComponent',
                        'Products.ZenModel.ManagedEntity.ManagedEntity'])

    def test_classes_shorthand(self):
        c = Component(self.zp, 'Component', klasses=['DeviceComponent',
                                                     'ManagedEntity'])
        self.assertEqual(
            c.klasses, ['Products.ZenModel.DeviceComponent.DeviceComponent',
                        'Products.ZenModel.ManagedEntity.ManagedEntity'])

    def test_classes_NonDefault(self):
        c = Component(self.zp, 'Component',
                      klasses=['zenpacks.zenoss.Test.Test'])
        self.assertEqual(c.klasses, ['zenpacks.zenoss.Test.Test'])

    def test_classes_NonArray(self):
        c = Component(self.zp, 'Component',
                      klasses='zenpacks.zenoss.Test.Test')
        self.assertEqual(c.klasses, ['zenpacks.zenoss.Test.Test'])

    def test_classes_zenpack_namespace(self):
        Component(self.zp, 'Test')
        c = Component(self.zp, 'Component', klasses=['Test'])
        self.assertEqual(c.klasses, ['a.b.c.Test'])

    def test_classes_zenpack_outside_namespace(self):
        c = Component(self.zp, 'Component', klasses=['OperatingSystem'])
        self.assertEqual(
            c.klasses, ['Products.ZenModel.OperatingSystem.OperatingSystem'])


class TestComponentImports(SimpleSetup):

    def test_imports_default(self):
        c = Component(self.zp, 'Component')
        expected = ['from zope.interface import implements',
             'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
             'from Products.Zuul.decorators import info',
             'from Products.Zuul.form import schema',
             'from Products.Zuul.infos import ProxyProperty',
             'from Products.Zuul.utils import ZuulMessageFactory as _t',
             'from Products.ZenModel.DeviceComponent import DeviceComponent',
             'from Products.ZenModel.ManagedEntity import ManagedEntity']
        for e in expected:
            self.assertTrue(e in c.imports)

    def test_imports_overridden(self):
        c = Component(self.zp, 'Component', imports=[
                      'from zope.interface import implements'])
        expected = ['from zope.interface import implements',
             'from Products.ZenModel.DeviceComponent import DeviceComponent',
             'from Products.ZenModel.ManagedEntity import ManagedEntity']
        for e in expected:
            self.assertTrue(e in c.imports)

    def test_imports_string(self):
        c = Component(self.zp, 'Component',
                      imports='from zope.interface import implements')
        expected = ['from zope.interface import implements',
             'from Products.ZenModel.DeviceComponent import DeviceComponent',
             'from Products.ZenModel.ManagedEntity import ManagedEntity']
        for e in expected:
            self.assertTrue(e in c.imports)

    def test_imports_with_classes(self):
        import pdb; pdb.set_trace()
        zp = ZenPack('a.b.c')
        c = Component(zp, 'Componentk',
                      klasses=['Products.ZenModel.OSComponent.OSComponent',
                               'Products.ZenModel.Linkable.Layer2Linkable'
                               ]
                      )
        c2 = Component(zp, 'Componentk2',
                       klasses=['Products.ZenModel.Software.Software',
                                ]
                       )

        self.maxDiff = None
        expected = ['from zope.interface import implements',
             'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
             'from Products.Zuul.decorators import info',
             'from Products.Zuul.form import schema',
             'from Products.Zuul.infos import ProxyProperty',
             'from Products.Zuul.utils import ZuulMessageFactory as _t',
             'from Products.ZenModel.OSComponent import OSComponent',
             'from Products.ZenModel.Linkable import Layer2Linkable',
             ]
        for e in expected:
            self.assertTrue(e in c.imports)

        expected = ['from zope.interface import implements',
             'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
             'from Products.Zuul.decorators import info',
             'from Products.Zuul.form import schema',
             'from Products.Zuul.infos import ProxyProperty',
             'from Products.Zuul.utils import ZuulMessageFactory as _t',
             'from Products.ZenModel.Software import Software',
             ]
        for e in expected:
            self.assertTrue(e in c2.imports)

class TestComponentNameSpace(SimpleSetup):

    def test_namespace_default(self):
        c = Component(self.zp, 'Component')
        self.assertEqual(c.namespace, DEFAULT_NAME)

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
        self.assertEqual(c.components.keys(), ['%s.Blade' % DEFAULT_NAME])

    def test_addComponent(self):
        c = Component(self.zp, 'Component')
        c.addComponentType('SubComponent')
        self.assertEqual(
            c.components.keys(), ['%s.SubComponent' % DEFAULT_NAME])


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
        self.assertEqual([r.id for r in c.relations()], [
                         '%s.Component %s.SubComponent' % (DEFAULT_NAME, DEFAULT_NAME)])


class TestCustomPaths(SimpleSetup):

    def test_findCustomPaths(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        dc.addComponentType('Enclosure')
        b = dc.addComponentType('Blade')
        f = dc.addComponentType('Fan')

        Relationship(self.zp, 'Enclosure', 'Fan', Type='1-M', Contained=False)
        Relationship(self.zp, 'Enclosure',
                     'Blade', Type='1-M', Contained=False)

        self.assertEqual(
            [c.id for c in f.custompaths(
            )['1-M'][0]], ['%s.Enclosure' % DEFAULT_NAME,
                           '%s.d.Device' % DEFAULT_NAME])
        self.assertEqual(
            [c.id for c in b.custompaths(
            )['1-M'][0]], ['%s.Enclosure' % DEFAULT_NAME,
                           '%s.d.Device' % DEFAULT_NAME])


class TestDropDownComponents(SimpleSetup):

    def test_findDropDownComponents(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        dc.addComponentType('Enclosure')
        f = dc.addComponentType('Fan')
        Relationship(self.zp, 'Enclosure', 'Fan', Type='1-M', Contained=False)
        self.assertEqual(
            [c.id for c in f.dropdowncomponents()], ['a.b.c.Enclosure'])


class TestManyRelationships(SimpleSetup):

    def test_findManyRelationships(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e = dc.addComponentType('a.Enclosure')
        e.addComponentType('Drive')
        self.assertEqual(
            [r.id for r in e.ManyRelationships()], ['a.Enclosure a.b.c.Drive'])


class TestDisplayInfo(SimpleSetup):

    def test_properties(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e = dc.addComponentType('a.Enclosure')
        e.addProperty('foo')
        self.assertEqual(e.displayInfo(), True)

    def test_trueManyRelationships(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e2 = dc.addComponentType('a.Enclosure2')
        e2.addComponentType('Drive2')
        self.assertEqual(e2.displayInfo(), True)

    def test_donotdisplayInfo(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e = dc.addComponentType('a.Enclosure')
        self.assertEqual(e.displayInfo(), False)


class TestDisplayIInfo(SimpleSetup):

    def test_properties(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e = dc.addComponentType('a.Enclosure')
        e.addProperty('foo')
        self.assertEqual(e.displayIInfo(), True)

    def test_trueManyRelationships(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e2 = dc.addComponentType('a.Enclosure2')
        e2.addComponentType('Drive2')
        self.assertEqual(e2.displayIInfo(), True)

    def test_donotdisplayIInfo(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e = dc.addComponentType('a.Enclosure')
        self.assertEqual(e.displayIInfo(), False)


class TestRelationshipsToStrings(SimpleSetup):

    def test_findManyRelationships(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e = dc.addComponentType('a.Enclosure')
        e.addComponentType('Drive')
        self.maxDiff = None
        self.assertEqual(e.relationstoArrayofStrings(), [
                         "('device', ToOne(ToManyCont, 'a.b.c.d.Device', 'enclosures',)),", "('drives', ToManyCont(ToOne, 'a.b.c.Drive', 'enclosure',)),"])


class TestUpdatedImports(SimpleSetup):

    def testOnetoManyCont(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e = dc.addComponentType('a.Enclosure')
        e.addComponentType('a.Disk')
        e.updateImports()
        self.assertTrue(
            'from Products.ZenRelations.RelSchema import ToManyCont,ToOne' in e.imports)

    def testOnetoMany(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e = dc.addComponentType('a.Enclosure')
        d = e.addComponentType('a.Disk')
        Relationship(self.zp, 'a.Enclosure',
                     'a.Disk', Type='1-M', Contained=False)
        d.updateImports()
        e.updateImports()
        self.assertTrue(
            'from Products.ZenRelations.RelSchema import ToMany,ToOne'
            in d.imports)

    def testOnetoOne(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.Device')
        e = dc.addComponentType('a.Enclosure')
        Relationship(self.zp, 'a.Enclosure',
                     'a.Disk', Type='1-1', Contained=False)
        d = Component(self.zp, 'a.Disk')
        d.updateImports()
        e.updateImports()
        self.assertTrue(
            'from Products.ZenRelations.RelSchema import ToOne' in d.imports)

    #@unittest.skip("Skipping")
    def testManytoMany(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.e.Device')
        e = dc.addComponentType('a.b.Enclosure')
        Relationship(self.zp, 'a.b.Enclosure',
                     'a.b.Disk', Type='M-M', Contained=False)
        d = Component(self.zp, 'a.b.Disk')
        d.updateImports()
        e.updateImports()
        self.assertTrue(
            'from Products.ZenRelations.RelSchema import ToMany' in d.imports)

    def testManytoManyCont(self):
        dc = self.zp.addDeviceClass('Device', zPythonClass='a.b.c.d.e.Device')
        e = dc.addComponentType('a.b.Enclosure')
        Relationship(self.zp, 'a.b.Enclosure',
                     'a.b.Disk', Type='M-M', Contained=True)
        d = Component(self.zp, 'a.b.Disk')
        d.updateImports()
        e.updateImports()
        self.assertTrue(
            'from Products.ZenRelations.RelSchema import ToMany,ToManyCont'
            in d.imports)


class TestLookups(SimpleSetup):

    def testComponentLookup(self):
        Component(self.zp, 'Disk')
        self.assertEqual(
            Component.lookup(self.zp, 'a.b.c.Disk').id, 'a.b.c.Disk')


class TestWriteTemplates(WriteTemplatesBase):

    def test_WriteBasic(self):
        c = Component(self.zp, 'Component')
        self.write(c, '${zenpack.id}\n${zenpack.version}\n')
        version = defaults.get('version')
        name = DEFAULT_NAME
        self.assertEqual(self.results[-1], call(u'%s\n%s\n' % (name, version)))


class TestWriteTemplatesAgain(WriteTemplatesBase):

    def test_WriteBasicAgain(self):
        d = Component(self.zp, 'Component2')
        name = DEFAULT_NAME
        version = defaults.get('version')
        self.write(
            d, '${zenpack.id}\n${zenpack.version}\n${zenpack.version}\n')
        self.assertEqual(self.results[-1], call(
            u'%s\n%s\n%s\n' % (DEFAULT_NAME, version, version)))

if __name__ == '__main__':
    unittest.main()
