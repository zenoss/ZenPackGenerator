#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################
from Property import Property
from lxml import etree
from utils import KlassExpand
import sys
import logging
log = logging.getLogger('Organizer')

class Organizer(object):
    "Placeholder for Organizer types."

    def __init__(self,
                 zenpack,
                 name,
                 Type,
                 properties = None
                 ):
        '''Args:
                 name: Organizer Name in the form of a Slash separated path.
                 properties: an array of dictionaries of property information which will
                             create property objects

        '''
        self.zenpack = zenpack
        self.name = name
        self.id = name
        self.Type = Type
        if properties:
            self.properties = properties
        else:
            self.properties = {}

        #Dict loading
        if properties:
            for p in properties:
                self.addProperty(**p)
      
        # Lookup the zPythonClass out of our DeviceClasses 
        dc_search = '/zport/dmd/%s' % name 
        if dc_search in self.zenpack.deviceClasses:
            p = { 'name': 'zPythonClass',
                  'Type': 'string',
                  'value': self.zenpack.deviceClasses[dc_search].zPythonClass
                 }
            self.addProperty(**p)

        self.zenpack.registerOrganizer(self)

    def addProperty(self, *args, **kwargs):
        prop = Property(*args, **kwargs)
        self.properties[prop.id] = prop

    def to_objects_xml(self):
        if self.Type == 'DeviceClass':
	    o=etree.Element("object", module="Products.ZenModel.DeviceClass", id="/zport/dmd/%s" % self.name) 
            
            # Cant set special keyword class in the constructor so do it in a second step.
            o.set('class', 'DeviceClass')

            # Append Property object.xml
            for property in self.properties.values():
                o.append(property.to_objects_xml())
            return o
