#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################

import unittest
import inflect
from Defaults import Defaults
from Property import Property
from Relationship import Relationship
# from Cheetah.Template import Template as cTemplate
from utils import KlassExpand, zpDir
from Template import Template

plural = inflect.engine().plural


class Component(Template):
    """Build the component object"""

    components = {}

    def __init__(self,
                 name,
                 zenpack,
                 klasses=None,
                 imports=None,
                 names=None,
                 meta_type=None,
                 device=False,
                 namespace=None,
                 panelSort='name',
                 panelSortDirection='asc',
                 properties=None,
                 componentTypes=None
                 ):

        super(Component, self).__init__(zenpack)
        self.source_template = 'component.tmpl'

        self.name = name.split('.')[-1]
        self.names = names
        self.klass = self.name

        self.zenpack = zenpack
        self.id = KlassExpand(self.zenpack, self.name)

        self.device = device
        self.panelSort = panelSort
        self.panelSortDirection = panelSortDirection

        if not imports:
            if not device:
                self.imports = Defaults().component_imports
            else:
                self.imports = Defaults().device_imports
        elif isinstance(imports, basestring):
            self.imports = [imports]
        else:
            # Copy the input array, don't hang on to a reference.
            self.imports = list(imports)

        if namespace:
            self.namespace = namespace
        else:
            self.namespace = self.zenpack.namespace

        self.shortklass = self.id.split('.')[-1]
        self.relname = self.shortklass.lower()
        self.relnames = plural(self.relname)
        self.unique_name = meta_type

        self.dest_file = "%s/%s.py" % (zpDir(zenpack), self.unique_name)

        if not klasses:
            if not device:
                self.klasses = Defaults().component_classes
            else:
                self.klasses = Defaults().device_classes
        # Copy the input array, don't hang on to a reference.
        elif isinstance(klasses, basestring):
            self.klasses = [klasses]
        else:
            self.klasses = list(klasses)

        self.properties = {}

        self.zenpack.registerComponent(self)
        Component.components[self.id] = self

        #Dict loading
        if properties:
            for p in properties:
                self.addProperty(**p)

        #Dict loading
        if componentTypes:
            for component in componentTypes:
                self.addComponentType(**component)

    def __lt__(self, other):
        '''Implemented for sort operations'''
        return self.id < other.id

    # @property
    # def id(self):
    #     return self.__id

    # @id.setter
    # def id(self, value):
    #     if value:
    #         self.__id = value
    #     else:
    #         if "." in self.name:
    #             self.__id = self.name
    #         else:
    #             self.__id = ".".join([self.namespace, self.name])

    def Type(self):
        if self.device:
            return 'Device'
        else:
            return 'Component'

    @property
    def unique_name(self):
        return self.__unique_name

    @unique_name.setter
    def unique_name(self, value):
        if not value:
            self.__unique_name = self.shortklass
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
    def names(self, value):
        if value:
            self.__names = value
        else:
            self.__names = plural(self.name)

        self.__names = self.__names.split('.')[-1]

    @property
    def klasses(self):
        return self._classes

    @klasses.setter
    def klasses(self, value):
        classes = []
        if isinstance(value, basestring):
            value = [value]
        for Klass in value:
            if len(Klass.split('.')) == 1:
                if Klass.split('.')[-1] in self.zenpack.namespace:
                    Klass = '{0}.{1}.{1}'.format(self.zenpack.namespace, Klass)
                else:
                    Klass = 'Products.ZenModel.{0}.{0}'.format(Klass)
            classes.append(Klass)
            Module = ".".join(Klass.split('.')[:-1])
            klass = Klass.split('.')[-1]
            istring = "from {0} import {1}".format(Module, klass)
            if istring not in self.imports:
                self.imports.append(istring)
        self._classes = classes

    def klassNames(self):
        return [c.split('.')[-1] for c in self.klasses]

    def addProperty(self, *args, **kwargs):
        prop = Property(*args, **kwargs)
        self.properties[prop.id] = prop

    def relations(self):
        #return self.zenpack.relationshipLookup(self)
        return Relationship.find(self)

    def custompaths(self):
        custompaths = {}
        rels = Relationship.find(self, Contained=False, First=False)
        for rel in rels:
            for component in rel.components:
                if component == self:
                    continue
                prel = Relationship.find(component, Contained=True, First=False)
                if prel:
                    prel = prel[0]
                    if not rel.Type in custompaths.keys():
                        custompaths[rel.Type] = [(component, prel.components[0])]
                    else:
                        custompaths[rel.Type].append((component, prel.components[0]))

        return custompaths
        """obj = self.context.${first_component}()
           if obj:
              paths.extend(relPath(${first_component, '${prel.components[0]}'))
        """

    def dropdowncomponents(self):
        '''return the component objects that this should contain a dropdown link to this component.'''
        results = []
        custompaths = self.custompaths()
        for values in custompaths.values():
            for path in values:
                results.append(path[0])
        return results

    def ManyRelationships(self):
        """return all of the ManyRelationships related to this component."""
        rels = Relationship.find(self, First=True, Types=['1-M', 'M-M'])
        return rels

    def relationstoArrayofStrings(self):
        rels = []
        for rel in self.relations():
            rels.append(rel.toString(self))
        return rels

    def displayInfo(self):
        # TODO improve this method to include scenarios when
        # we are adding one to many non-container relationships etc.
        if self.properties:
            return True
        if self.ManyRelationships():
            return True
        return False

    def displayIInfo(self):
        for p in self.properties.values():
            if p.detailDisplay:
                return True
        if self.ManyRelationships():
            return True
        return False

    @classmethod
    def lookup(self, zenpack, value):

        if value in Component.components:
            return Component.components[value]

        component = "{0}.{1}".format(zenpack.namespace, value)
        if component in Component.components:
            return Component.components[component]

        component = "{0}.{1}".format('Products.ZenModel', value)
        if component in Component.components:
            return Component.components[component]

        return Component(value, zenpack)

    def addComponentType(self, *args, **kwargs):
        if not 'zenpack' in kwargs:
            kwargs['zenpack'] = self.zenpack
        c = Component(*args, **kwargs)
        Relationship(self.zenpack, self.id, c.id)
        return c

    def updateImports(self):
        Types = {}
        for relationship in self.zenpack.relationships.values():
            if relationship.hasComponent(self):
                if '-M' in relationship.Type:
                    if relationship.Contained:
                        Types['ToManyCont'] = 1
                    else:
                        Types['ToMany'] = 1
                if '1' in relationship.Type:
                    Types['ToOne'] = 1
                if 'M-' in relationship.Type:
                    Types['ToMany'] = 1

        imports = "from Products.ZenRelations.RelSchema import %s" % ",".join(sorted(Types.keys()))
        self.imports.append(imports)


    def write(self):
        self.updateImports()
        self.processTemplate()


#Unit tests Start here
class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from ZenPack import ZenPack
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

if __name__ == "__main__":
    unittest.main()
