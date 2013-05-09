#!/usr/bin/env python
##LICENSE##

import unittest
import inflect
from Property import Property
from Cheetah.Template import Template as cTemplate

plural = inflect.engine().plural

class Component(object):
    """Build the component object"""

    components = {}

    def __init__(self,name, 
                      ZenPack, 
                      Classes = [ 'Products.ZenModel.DeviceComponent.DeviceComponent',
                                  'Products.ZenModel.ManagedEntity.ManagedEntity' ],
                      imports = [ 'from zope.component import implements',
                                  'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
                                  'from Products.Zuul.decorators import info',
                                  'from Products.Zuul.form import schema',
                                  'from Products.Zuul.infos import ProxyProperty',
                                  'from Products.Zuul.utils import ZuulMessageFactory as _t',
                                ],
                      names = None, 
                      meta_type = None,
                      device = False,
                      namespace = None
                ):
        '''Args:
                name: The components name is its class name.
                        By Default the name will also be used for the portal_type and meta_type.
                names: The plural form of the components name.  If not provided it will
                       be automatically generated. (Optional)
                ZenPack:  A ZenPack Object is required to use this class
                Classes: The base class or classes that the Component inherits from.  (Array)
                imports: The base set of python imports that this zenpack requires.
                meta_type: Override the meta_type/portal_type variables provided by the default name.
                namespace: Expand the name to use this namespace prefix for class loading.
                           If not provided the namespace will be inherited from the ZenPack object.

        '''

# Display meta_type option
        self.name = name
        self.Class = name
        self.names = names
        self.relname = self.name.lower()
        self.relnames = self.names.lower()
        self.ZenPack = ZenPack
        self.unique_name = meta_type
        self.device = device

        if isinstance(imports, basestring):
            self.imports = [imports]
        else:
            # Copy the input array, don't hang on to a reference.
            self.imports = list(imports)

        if namespace:
            self.namespace = namespace
        else:
            self.namespace = self.ZenPack.namespace
        self.id = "%s.%s" % (self.namespace,self.name)

        # Copy the input array, don't hang on to a reference.
        self.Classes = list(Classes)
        self.properties = {}
        self.ZenPack.registerComponent(self)
        Component.components[self.id] = self

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value:
            self.__id = value
        else:
            if "." in self.name:
                self.__id = self.name
            else:
                self.__id = ".".join([self.namespace, self.name])

    def Type(self):
        if self.device:
            return 'Device'
        else:
            return 'Component'

    @property
    def unique_name(self):
        return self.__unique_name

    @unique_name.setter
    def unique_name(self,value):
        if not value:
            self.__unique_name = self.name
        else:
            self.__unique_name = value

    @property
    def portal_type(self):
        return self.__unique_name

    @property
    def meta_type(self):
        return self.__unique_name

    @property
    def names(self):
        return self.__names

    @names.setter
    def names(self,value):
        if value:
           self.__names = value
        else:
           self.__names = plural(self.name)

    @property
    def Classes(self):
        return self._classes

    @Classes.setter
    def Classes(self,value):
        classes = []
        if isinstance(value, basestring):
            value = [value]
        for Klass in value:
            if len(Klass.split('.'))==1:
                if Klass.split('.')[-1] in self.ZenPack.namespace:
                    Klass = '{0}.{1}.{1}'.format(self.ZenPack.namespace, Klass)
                else:
                    Klass = 'Products.ZenModel.{0}.{0}'.format(Klass)
            classes.append(Klass)
            Module = ".".join(Klass.split('.')[:-1])
            Class = Klass.split('.')[-1]
            istring = "from {0} import {1}".format(Module, Class)
            if istring not in self.imports:
                self.imports.append(istring)
        self._classes = classes

    def ClassNames(self):
        return [c.split('.')[-1] for c in self.Classes]

    def addProperty(self,id,**kwargs):
        prop = Property(id,**kwargs)
        self.properties[id] = prop

    def relations(self):
        return self.ZenPack.relationshipLookup(self)

    def relationstoArrayofStrings(self):
        rels = []
        for rel in self.relations():
            rels.append(rel.toString(self))
        return rels

    def displayInfo(self):
        if self.properties:
            return True
        return False

    def displayIInfo(self):
        for p in self.properties.values():
            if p.detailDisplay:
                return True
        return False

    def hasManyChildRelationship(self):
        for rel in self.relations():
            if rel.hasManyChild(self):
                return True
        return False

    def ManyChildren(self):
        ManyChildren = []
        for rel in self.relations():
            if rel.hasManyChild(self):
                ManyChildren.append(rel.ManyChild(self))
        return ManyChildren

    def customPaths(self):
        paths = []
        for rel in self.relations():
            if not rel.Contained:
                path = rel.getParentPath(self)
                Type = rel.Type
                for c in rel.components:
                    if not c == self:
                       if Type == '1-1':
                           print c.relname, path, Type
                       if Type == '1-M':
                           print c.relname, path, Type
                       if Type == 'M-M':
                           import pdb; pdb.set_trace()
                           print c.relnames, path, Type

    @classmethod
    def lookup(self,ZenPack, value):

        if value in Component.components:
            return Component.components[value]

        component = "{0}.{1}".format(ZenPack.namespace,value)
        if component in Component.components:
            return Component.components[component]

        component = "{0}.{1}".format('Products.ZenModel',value)
        if component in Component.components:
            return Component.components[component]

        return Component(value, ZenPack)

    def write(self):
        t = cTemplate(file='component.tmpl', searchList=[self])
        print t
        print
        print
        #f = open('a.out', 'w')
        #f.write(t.respond())
        #f.close()

#Unit tests Start here

class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from ZenPack import ZenPack
        self.zp = ZenPack('a.b.c')

class TestComponentCreate(SimpleSetup):
    #@unittest.skip("Skipping")
    def test_ComponentCreate(self):
        c = Component('Component',self.zp)
        self.assertIsInstance(c, Component)

class TestNames(SimpleSetup):
    def test_name_default(self):
        c = Component('Component',self.zp)
        self.assertEqual(c.names, 'Components')

    def test_name_overridden(self):
        c = Component('Component',self.zp, names = 'names')
        self.assertEqual(c.names, 'names')

class TestComponentUniqueName(SimpleSetup):
    def test_uniquename_default(self):
        c = Component('Component',self.zp)
        self.assertEqual(c.portal_type, 'Component')
        self.assertEqual(c.meta_type, 'Component')
        self.assertEqual(c.unique_name, 'Component')

    def test_meta_type_Overridden(self):
        c = Component('Component', self.zp, meta_type = 'unique')
        self.assertNotEqual(c.portal_type, 'Component')
        self.assertNotEqual(c.meta_type, 'Component')
        self.assertNotEqual(c.unique_name, 'Component')
        self.assertEqual(c.portal_type, 'unique')
        self.assertEqual(c.meta_type, 'unique')
        self.assertEqual(c.unique_name, 'unique')

class TestComponentClasses(SimpleSetup):
    def test_classes_default(self):
        c = Component('Component', self.zp)
        self.assertEqual(c.Classes, ['Products.ZenModel.DeviceComponent.DeviceComponent',
                                     'Products.ZenModel.ManagedEntity.ManagedEntity'])

    def test_classes_shorthand(self):
        c = Component('Component', self.zp,Classes = ['DeviceComponent',
                                                      'ManagedEntity'])
        self.assertEqual(c.Classes, ['Products.ZenModel.DeviceComponent.DeviceComponent',
                                     'Products.ZenModel.ManagedEntity.ManagedEntity'])

    def test_classes_NonDefault(self):
        c = Component('Component', self.zp,Classes = ['ZenPacks.zenoss.Test.Test'])
        self.assertEqual(c.Classes, ['ZenPacks.zenoss.Test.Test'])

    def test_classes_NonArray(self):
        c = Component('Component', self.zp,Classes = 'ZenPacks.zenoss.Test.Test')
        self.assertEqual(c.Classes, ['ZenPacks.zenoss.Test.Test'])

class TestComponentClasses(SimpleSetup):
    def test_imports_default(self):
        c = Component('Component', self.zp)
        self.assertEqual(c.imports, ['from zope.component import implements',
            'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
            'from Products.Zuul.decorators import info',
            'from Products.Zuul.form import schema',
            'from Products.Zuul.infos import ProxyProperty',
            'from Products.Zuul.utils import ZuulMessageFactory as _t',
            'from Products.ZenModel.DeviceComponent import DeviceComponent',
            'from Products.ZenModel.ManagedEntity import ManagedEntity'])

    def test_imports_overridden(self):
        c = Component('Component', self.zp, imports = ['from zope.component import implements'])
        self.assertEqual(c.imports, ['from zope.component import implements',
            'from Products.ZenModel.DeviceComponent import DeviceComponent',
            'from Products.ZenModel.ManagedEntity import ManagedEntity'])

    def test_imports_string(self):
        c = Component('Component', self.zp, imports = 'from zope.component import implements')
        self.assertEqual(c.imports, ['from zope.component import implements',
            'from Products.ZenModel.DeviceComponent import DeviceComponent',
            'from Products.ZenModel.ManagedEntity import ManagedEntity'])

    def test_imports_with_classes(self):
        c = Component('Component', self.zp,
                       Classes= ['Products.ZenModel.OSComponent.OSComponent',
                                 'Products.ZenModel.Linkable.Layer2Linkable'
                                ]
                     )

        c2 = Component('Component2', self.zp,
                       Classes= ['Products.ZenModel.Software.Software',
                                ]
                      )
        self.maxDiff = None
        self.assertEqual(c.imports, ['from zope.component import implements',
            'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
            'from Products.Zuul.decorators import info',
            'from Products.Zuul.form import schema',
            'from Products.Zuul.infos import ProxyProperty',
            'from Products.Zuul.utils import ZuulMessageFactory as _t',
            'from Products.ZenModel.OSComponent import OSComponent',
            'from Products.ZenModel.Linkable import Layer2Linkable',
            ])

        self.assertEqual(c2.imports, ['from zope.component import implements',
            'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
            'from Products.Zuul.decorators import info',
            'from Products.Zuul.form import schema',
            'from Products.Zuul.infos import ProxyProperty',
            'from Products.Zuul.utils import ZuulMessageFactory as _t',
            'from Products.ZenModel.Software import Software',
            ])

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

if __name__ == "__main__":
    from ZenPack import ZenPack
    zp = ZenPack('a.b.c')
    c1 = zp.addComponent('Enclosure')
    c1.addProperty('foo')
    #f1 = zp.addComponent('Fan')
    #d1 = zp.addComponent('Device', namespace='Products.ZenModel')
    #rel = zp.addRelation('Device','Enclosure')
    #rel1 = zp.addRelation('Device','Fan', Type='1-1', Contained=False)
    rel2 = zp.addRelation('Enclosure','Fan', Type='M-M', Contained=False)
    #print 'Enclosure'
    #print c1.relationstoArrayofStrings()
    #print rel.hasManyChild(c1)
    #print rel2.hasManyChild(c1)
    #print c1.hasManyChildRelationship()
    #print [c.id for c in c1.ManyChildren()]
    #print
    #print 'Fan'
    #print f1.relationstoArrayofStrings()
    #print rel1.hasManyChild(f1)
    #print rel2.hasManyChild(f1)
    #print f1.hasManyChildRelationship()
    #print [c.id for c in f1.ManyChildren()]
    #print
    #print 'Device'
    #print d1.relationstoArrayofStrings()
    #print d1.hasManyChildRelationship()
    #print [c.id for c in d1.ManyChildren()]
    #print
    c1.write()
    #os.write()
    #interface.write()
    unittest.main()
