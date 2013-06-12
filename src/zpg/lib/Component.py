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
                 zenpack,
                 name,
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
        '''Args:
                 name: Component Name
                 names: Plural form of the Component Name [None]
                 zenpack: ZenPack class instance
                 klasses: list of base classes for this component [None]
                 imports: list of imports for this component [None]
                 meta_type: the component meta_type
                 device: Device Component is True or False [False]
                 namespace: python search namespace [None]
                            This will default to the zenpack id
                 panelSort: the default property to sort by
                 panelSortDirection: Direction to sort either 'asc' or 'dsc'
                 properties: an array of dictionaries of property information which will
                             create property objects
                 componentTypes: an array of dictionaries of component information which will
                             create componentType objects

        '''

        super(Component, self).__init__(zenpack)
        self.source_template = 'component.tmpl'

        self.name = name.split('.')[-1]
        self.names = names
        self.klass = self.name

        self.zenpack = zenpack
        self.id = KlassExpand(self.zenpack, name)

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

        self.components = {}
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
        
        self.updateComponents = {}

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
        '''return the type Device/Component'''
        if self.device:
            return 'Device'
        else:
            return 'Component'

    @property
    def unique_name(self):
        '''Return the unique_name'''
        return self.__unique_name

    @unique_name.setter
    def unique_name(self, value):
        ''' set the unique name to the short klass unless overridden '''
        if not value:
            self.__unique_name = self.shortklass
        else:
            self.__unique_name = value

    @property
    def portal_type(self):
        '''The portal_type is the same as the unique name'''
        return self.__unique_name

    @property
    def meta_type(self):
        '''The meta_type is the same as the unique name'''
        return self.__unique_name

    @property
    def names(self):
        '''Return the names'''
        return self.__names

    @names.setter
    def names(self, value):
        '''return the plural of name unless overridden'''
        if value:
            self.__names = value
        else:
            self.__names = plural(self.name)

        self.__names = self.__names.split('.')[-1]

    @property
    def klasses(self):
        '''return the Classes that are the basis for this component.'''
        return self._classes

    @klasses.setter
    def klasses(self, value):
        '''return the classes
           short classes are expanded to the full zenpack namespace.
           eg Foo -> ZenPacks.example.Demo.Foo

           also the imports automatically extend to include these classes.
        '''

        classes = []
        for Klass in value:
            if len(Klass.split('.')) == 1:
                results = self.lookup(self.zenpack, Klass, create=False)
                if results:
                    Klass = results.id
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
        '''short version of the classes in an array.'''
        return [c.split('.')[-1] for c in self.klasses]

    def addProperty(self, *args, **kwargs):
        prop = Property(*args, **kwargs)
        self.properties[prop.id] = prop

    def relations(self):
        '''Find all the relationships that contain this component'''
        #return self.zenpack.relationshipLookup(self)
        return Relationship.find(self)

    def custompaths(self):
        '''for non-contained child components return a dict
           {Type: component, parent component of the parent components}
        '''
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

        return custompaths
        """obj = self.context.${first_component}()
           if obj:
              paths.extend(relPath(${first_component, '${prel.components[0]}'))
        """

    def findUpdateComponents(self):
        '''return a dictionary of components used in the updateToOne or
        updateToMany Methods.'''

        results = {}
        rels = Relationship.find(self, Contained=False)
        for rel in rels:
            if rel.components[0].id != self.id:
                component = rel.components[0]
                Type = rel.Type.split('-')[0]
            else:
                component = rel.components[1]
                Type = rel.Type.split('-')[1]

            if Type in results:
                results[Type].append(component)
            else:
                results[Type] = [component]

        imports = []
        if '1' in results:
            imports.append('updateToOne')
        if 'M' in results:
            imports.append('updateToMany')

        self.imports.append('from %s.utils import %s' % (self.zenpack.id, ",".join(sorted(imports))))
        self.updateComponents = results


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
        '''return an array of relationship strings'''
        rels = []
        for rel in self.relations():
            rels.append(rel.toString(self))
        return sorted(rels)

    def displayInfo(self):
        '''return True if we should build the Info Class'''
        # TODO improve this method to include scenarios when
        # we are adding one to many non-container relationships etc.
        if self.properties:
            return True
        if self.ManyRelationships():
            return True
        return False

    def displayIInfo(self):
        '''return True if we should build the IInfo Class'''
        for p in self.properties.values():
            if p.detailDisplay:
                return True
        if self.ManyRelationships():
            return True
        return False

    @classmethod
    def lookup(self, zenpack, component_id, create=True):
        '''find a component by its id'''

        if component_id in Component.components:
            return Component.components[component_id]

        component = "{0}.{1}".format(zenpack.namespace, component_id)
        if component in Component.components:
            return Component.components[component]

        component = "{0}.{1}".format('Products.ZenModel', component_id)

        if create:
            return Component(zenpack, component_id)
        else:
            return None

    def addComponentType(self, *args, **kwargs):
        '''add a subcomponent'''
        if 'zenpack' in kwargs:
            del(kwargs['zenpack'])
        c = Component(self.zenpack, *args, **kwargs)
        self.components[c.id] = c

        Relationship(self.zenpack, self.id, c.id)
        return c

    def updateImports(self):
        '''Append the relationship imports'''
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
        '''Write the component files'''
        self.updateImports()
        self.findUpdateComponents()
        self.processTemplate()
