#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

import logging

import inflect

from .colors import error, warn, debug, info, green, red, yellow
from ._defaults import Defaults
from ._zenoss_utils import KlassExpand, zpDir
from .Property import Property
from .Relationship import Relationship
from .Template import Template

plural = inflect.engine().plural
defaults = Defaults()


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
                 abstract=False,
                 namespace=None,
                 panelSort='name',
                 panelSortDirection='asc',
                 properties=None,
                 componentTypes=None,
                 impacts=None,
                 impactedBy=None,
                 *args,
                 **kwargs
                 ):
        """Args:
                 name: Component Name
                 names: Plural form of the Component Name [None]
                 zenpack: ZenPack class instance
                 klasses: list of base classes for this component [None]
                 imports: list of imports for this component [None]
                 meta_type: the component meta_type
                 device: Device Component is True or False [False]
                 abstract: Component is abstract base class for other
                           components, not meant to be instantiated directly,
                           and not shown in the UI [False]
                 namespace: python search namespace [None]
                            This will default to the zenpack id
                 panelSort: the default property to sort by
                 panelSortDirection: Direction to sort either 'asc' or 'dsc'
                 properties: an array of dictionaries of property information
                             which will create property objects
                 componentTypes: an array of dictionaries of component
                             information which will create componentType
                             objects
                 impacts: an array of components that this component impacts.
                 impactedBy: an array of components that impact this component.
        '''

        """
        super(Component, self).__init__(zenpack)
        self.logger = logger = logging.getLogger('ZenPack Generator')
        for key in kwargs:
            do_not_warn = False
            clsname = self.__class__.__name__
            layer = "%s:%s" % (clsname, name)
            msg = "WARNING: [%s] unknown keyword ignored in file: '%s'"
            margs = (layer, key)
            if not do_not_warn:
                warn(self.logger, yellow(msg) % margs)
        self.source_template = 'component.tmpl'
        self.name = name.split('.')[-1]
        self.names = names
        self.klass = self.name
        self.zenpack = zenpack
        self.id = KlassExpand(self.zenpack, name)
        self.device = device
        self.abstract = abstract
        self.panelSort = panelSort
        self.panelSortDirection = panelSortDirection
        if not imports:
            if not device:
                self.imports = defaults.get('component_imports')
            else:
                self.imports = defaults.get('device_imports')
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
        self.dest_file = "%s/%s.py" % (zpDir(zenpack), self.shortklass)
        if not klasses:
            if not device:
                self.klasses = defaults.get('component_classes')
            else:
                self.klasses = defaults.get('device_classes')
        # Copy the input array, don't hang on to a reference.
        elif isinstance(klasses, basestring):
            self.klasses = [klasses]
        else:
            self.klasses = list(klasses)
        self.properties = {}
        self.components = {}
        self.zenpack.registerComponent(self)
        Component.components[self.id] = self
        # Dict loading
        if properties:
            for p in properties:
                self.addProperty(**p)
        # Dict loading
        if componentTypes:
            for component in componentTypes:
                self.addComponentType(**component)

        self.updateComponents = {}

        self.impacts = impacts if impacts is not None else []
        self.impactedBy = impactedBy if impactedBy is not None else []

    def __lt__(self, other):
        """Implemented for sort operations"""
        return self.id < other.id

    def type_(self):
        """return the type Device/Component"""
        if self.device:
            return 'Device'
        else:
            return 'Component'

    def Type(self):
        return self.type_()

    @property
    def unique_name(self):
        """Return the unique_name"""
        return self.__unique_name

    @unique_name.setter
    def unique_name(self, value):
        """ set the unique name to the short klass unless overridden """
        if not value:
            self.__unique_name = self.shortklass
        else:
            self.__unique_name = value

    @property
    def portal_type(self):
        """The portal_type is the same as the unique name"""
        return self.__unique_name

    @property
    def meta_type(self):
        """The meta_type is the same as the unique name"""
        return self.__unique_name

    @property
    def names(self):
        """Return the names"""
        return self.__names

    @names.setter
    def names(self, value):
        """return the plural of name unless overridden"""
        if value:
            self.__names = value
        else:
            self.__names = plural(self.name)

        self.__names = self.__names.split('.')[-1]

    @property
    def klasses(self):
        """return the Classes that are the basis for this component."""
        return self._classes

    @klasses.setter
    def klasses(self, value):
        """return the classes
           short classes are expanded to the full zenpack namespace.
           eg Foo -> ZenPacks.example.Demo.Foo

           also the imports automatically extend to include these classes.
        """
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
        """short version of the classes in an array."""
        return [c.split('.')[-1] for c in self.klasses]

    def addProperty(self, *args, **kwargs):
        prop = Property(*args, **kwargs)
        self.properties[prop.id] = prop

    def relations(self):
        """Find all the relationships that contain this component"""
        # return self.zenpack.relationshipLookup(self)
        return Relationship.find(self)

    def custompaths(self):
        """for non-contained child components return a dict
           {Type: component, parent component of the parent components}
        """
        custompaths = {}
        rels = Relationship.find(self, contained=False, first=False)
        for rel in rels:
            for component in rel.components:
                if component == self:
                    continue
                prel = Relationship.find(
                    component, contained=True, first=False)
                if prel:
                    prel = prel[0]
                    if not rel.type_ in custompaths.keys():
                        custompaths[rel.type_] = [
                            (component, prel.components[0])]
        if custompaths:
            imports = "from Products.Zuul.catalog.paths "
            imports += "import DefaultPathReporter, relPath"
            self.imports.append(imports)
        if custompaths:
            paths = "Products.Zuul.catalog.paths"
            imports = "from %s import DefaultPathReporter, relPath" % paths
            self.imports.append(imports)
        return custompaths

    def findUpdateComponents(self):
        """return a dictionary of components used in the updateToOne or
        updateToMany Methods."""
        results = {}
        rels = Relationship.find(self, contained=False)
        for rel in rels:
            if rel.components[0].id != self.id:
                component = rel.components[0]
                type_ = rel.type_.split('-')[0]
            else:
                component = rel.components[1]
                type_ = rel.type_.split('-')[1]
            if type_ in results:
                results[type_].append(component)
            else:
                results[type_] = [component]
        imports = []
        if '1' in results:
            imports.append('updateToOne')
        if 'M' in results:
            imports.append('updateToMany')
        if results:
            self.imports.append('from %s.utils import %s' %
                                (self.zenpack.id, ",".join(sorted(imports))))
        self.updateComponents = results

    def dropdowncomponents(self):
        """return the component objects that this should contain a
        dropdown link to this component."""
        results = []
        custompaths = self.custompaths()
        for values in custompaths.values():
            for path in values:
                results.append(path[0])
        return results

    def ManyRelationships(self):
        """return all of the ManyRelationships related to this component."""
        rels = Relationship.find(self, first=True, types=['1-M', 'M-M'])
        return rels

    def relationstoArrayofStrings(self, indent=""):
        """return an array of relationship strings"""
        rels = []
        for rel in self.relations():
            relString = "\n".join([indent + x for x in
                        rel.toString(self).split("\n")])
            rels.append(relString)
        return sorted(rels)

    def displayInfo(self):
        """return True if we should build the Info Class"""
        # TODO improve this method to include scenarios when
        # we are adding one to many non-container relationships etc.

        if self.abstract:
            return False

        if self.device:
            imports = "from Products.Zuul.infos.device import DeviceInfo"
        else:
            imports = "from Products.Zuul.infos.component import ComponentInfo"
        if self.componentInZenPackNameSpace():
            if self.properties:
                self.imports.append(imports)
                return True
            if self.ManyRelationships():
                self.imports.append(imports)
                return True
        return False

    def displayIInfo(self):
        """return True if we should build the IInfo Class"""
        name = "Products.Zuul.interfaces"

        if self.abstract:
            return False

        if self.device:
            imports = "from %s import IDeviceInfo" % name
        else:
            imports = "from %s.component import IComponentInfo" % name
        if self.componentInZenPackNameSpace():
            for p in self.properties.values():
                if p.detailDisplay:
                    self.imports.append(imports)
                    return True
            if self.ManyRelationships():
                self.imports.append(imports)
                return True
        return False

    @classmethod
    def lookup(self, zenpack, component_id, create=True):
        """find a component by its id"""
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
        """add a subcomponent"""
        type_ = '1-M'
        contained = True
        if 'zenpack' in kwargs:
            del(kwargs['zenpack'])
        if 'type_' in kwargs:
            type_ = kwargs['type_']
            del(kwargs['type_'])
        if 'contained' in kwargs:
            type_ = kwargs['contained']
            del(kwargs['contained'])
        c = Component(self.zenpack, *args, **kwargs)
        self.components[c.id] = c
        Relationship(self.zenpack, self.id, c.id, type_=type_,
                     contained=contained)
        return c

    def updateImports(self):
        # Call these three functions to update some imports.
        self.displayInfo()
        self.displayIInfo()
        self.custompaths()
        # Append the relationship imports
        Types = {}
        for relationship in self.zenpack.relationships.values():
            if relationship.hasComponent(self):
                if '-M' in relationship.type_:
                    if relationship.contained:
                        Types['ToManyCont'] = 1
                    else:
                        Types['ToMany'] = 1
                if '1' in relationship.type_:
                    Types['ToOne'] = 1
                if 'M-' in relationship.type_:
                    Types['ToMany'] = 1
        if len(Types.keys()) > 0:
            imports = "from Products.ZenRelations.RelSchema import %s" %\
                      ", ".join(sorted(Types.keys()))
            self.imports.append(imports)

        def f7(seq):
            seen = set()
            seen_add = seen.add
            return [x for x in seq if x not in seen and not seen_add(x)]
        # Remove duplicates
        self.imports = f7(self.imports)

    def convertImpactStringsToRealComponents(self):
        # Convert the component strings to real component objects.
        impacts = self.impacts
        impactedBy = self.impactedBy

        self.impacts = []
        if impacts:
            for obj in impacts:
                real_obj = self.lookup(self.zenpack, obj, create=False)
                if real_obj:
                    for rel in Relationship.find(real_obj):
                        if rel.hasComponent(self):
                            self.impacts.append(real_obj)

        self.impactedBy = []
        if impactedBy:
            for obj in impactedBy:
                real_obj = self.lookup(self.zenpack, obj, create=False)
                if real_obj:
                    for rel in Relationship.find(real_obj):
                        if rel.hasComponent(self):
                            self.impactedBy.append(real_obj)

    def hasImpact(self):
        # Return true if we have an impact relationship
        if self.impacts:
            return True
        if self.impactedBy:
            return True
        return False

    def impactedBySingle(self, impactor):
        'if the relationship should be a single relname return true.'
        for rel in Relationship.find(impactor, first=True,
                                     types=['1-1', '1-M']):
            if rel.hasChild(self):
                return True
        return False

    def impactSingle(self, impactee):
        'if the relationship should be a single relname return true.'
        for rel in Relationship.find(impactee, first=False,
                                     types=['1-1', '1-M']):
            if rel.hasChild(self):
                return True
        return False

    def componentInZenPackNameSpace(self):
        'return true if the component id startswith the zenpack id'
        return self.id.startswith(self.zenpack.id)

    def write(self):
        """Write the component files"""
        self.updateImports()
        self.findUpdateComponents()
        self.convertImpactStringsToRealComponents()

        # Only write components that are prefixed in this zenpacks namespace.
        if self.componentInZenPackNameSpace():
            self.processTemplate()
