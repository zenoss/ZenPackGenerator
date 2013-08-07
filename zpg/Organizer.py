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
import sys

from lxml import etree

from .colors import error, warn, debug, info, green, red, yellow
from .Property import Property
from ._zenoss_utils import KlassExpand


class Organizer(object):

    "Placeholder for Organizer types."

    def __init__(self,
                 zenpack,
                 name,
                 type_,
                 properties=None,
                 *args,
                 **kwargs
                 ):
        """Args:
            name: Organizer Name in the form of a Slash separated path.
            properties: an array of dictionaries of property
                         information which will create property objects
        """
        self.zenpack = zenpack
        self.name = name
        self.id = name
        self.type_ = type_
        self.properties = {}
        self.logger = logger = logging.getLogger('ZenPack Generator')
        for key in kwargs:
            do_not_warn = False
            layer = self.__class__.__name__
            msg = "WARNING: JSON keyword ignored in layer '%s': '%s'"
            margs = (layer, key)
            if key == "Type":
                msg = "WARNING: JSON keyword deprecated in '%s' layer. "\
                      "'%s' is now '%s'."
                margs = (layer, key, key.lower())
                self.type_ = kwargs[key]
            elif key == "type":
                self.type_ = type_ = kwargs[key]
                do_not_warn = True
            elif key == "Contained":
                msg = "WARNING: JSON keyword deprecated in '%s' layer. "\
                      "'%s' is now '%s'."
                margs = (layer, key, key.lower())
                self.contained = kwargs[key]
            if not do_not_warn:
                warn(self.logger, yellow(msg) % margs)
        # Dict loading
        if properties:
            for p in properties:
                self.addProperty(**p)
        # Lookup the zPythonClass out of our DeviceClasses
        dc_search = '/zport/dmd/%s' % name
        dev_classes = self.zenpack.deviceClasses
        if dc_search in dev_classes:
            p = {'name': 'zPythonClass',
                 'type_': 'string',
                 'value': dev_classes[dc_search].zPythonClass
                 }
            self.addProperty(**p)
        self.zenpack.registerOrganizer(self)

    def addProperty(self, *args, **kwargs):
        """Creates a new Property for the Organizer instance"""
        prop = Property(*args, **kwargs)
        self.properties[prop.id] = prop

    def to_objects_xml(self):
        """Returns an xml tree if the Organizer is a Device Class"""
        if self.type_ == 'DeviceClass':
            o = etree.Element("object",
                              module="Products.ZenModel.DeviceClass",
                              id="/zport/dmd/%s" % self.name)
            # Cant set special keyword class in the constructor so do it
            #  in a second step.
            o.set('class', 'DeviceClass')
            # Append Property object.xml
            for property in self.properties.values():
                o.append(property.to_objects_xml())
            return o
