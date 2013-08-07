#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

import inflect
from lxml import etree
import re

plural = inflect.engine().plural


class Property(object):

    """Define a properties capabilities inside a Component."""

    def __init__(self,
                 name,
                 value=None,
                 type_=None,
                 width=10,
                 detailDisplay=True,
                 gridDisplay=True,
                 sortable=True,
                 panelRenderer=None):
        """Args:
             name: Property name
             value: default value [None]
             type_: type of property [None]
                   valid types: ['string', 'text', 'list', 'int',
                                 'bool', 'long', 'boolean', 'float',
                                 'password']
                   If a value is set and no type is set the type will be
                   determined from the value'
             width: pixel width of the column in the ui
             detailDisplay: Show this property in the details section of
                            the UI [True/False]
             gridDisplay: Show this property in the grid section of the
                          UI [True/False]
             sortable: Sortable Property [True/False]
             panelRenderer: Define a custom panel renderer
        """
        self.id = name
        self.name = name
        self.names = plural(name)
        self.mode = 'w'
        self.detailDisplay = detailDisplay
        self.gridDisplay = gridDisplay
        self.sortable = True
        self.width = width
        self.panelRenderer = panelRenderer
        self.type_ = type_ if type_ else value
        self.value = value

    def Schema(self):
        """Given the type return the correct Schema."""
        if self.type_.lower() in ['int']:
            return 'Int'
        elif self.type_.lower() in ['string', 'text', 'list']:
            return 'TextLine'
        elif self.type_.lower() in ['bool']:
            return 'Bool'
        else:
            return 'TextLine'

    @property
    def type_(self):
        """Return the type"""
        return self._Type

    @type_.setter
    def type_(self, type_):
        """Input validation for the type"""
        self._Type = None
        # Zope Types we are supporting
        valid_zope_types = ['string', 'text', 'list', 'lines', 'int', 'bool',
                            'long', 'boolean', 'float', 'password']
        # All Zope types
        # boolean,date,float,int,list,
        # long,string,text,tokens,selection,multiple_selection
        if type_ is not None and type_ in valid_zope_types:
            self._Type = type_
            if self._Type == 'lines':
                self._Type = 'list'
        else:
            if isinstance(type_, str):
                self._Type = 'string'
            elif isinstance(type_, bool):
                self._Type = 'boolean'
            elif isinstance(type_, int):
                self._Type = 'int'
            elif isinstance(type_, float):
                self._Type = 'float'
            elif isinstance(type_, list):
                self._Type = 'list'
        # Default return of string
        if not self._Type:
            self._Type = 'string'

    @property
    def Type(self):
        return self.type_

    @Type.setter
    def Type(self, type_):
        self.type_ = type_

    @property
    def value(self):
        """Return the value"""
        return self._value

    @value.setter
    def value(self, value):
        """Input validation for the value"""
        # Valid values can be implemented later.
        if value is not None and self.type_ == 'string':
            if not value.startswith('\''):
                value = '\'' + value 
                if len(value) == 1:
                    value = value + '\''
            if not value.endswith('\''):
                value = value + '\''
        self._value = 'None' if value is None else value

    def to_objects_xml(self):
        o = etree.Element("property")
        o.set('id', self.id)
        o.set('type', self.Type)
        if self.id not in ['zendoc', 'description']:
            o.set('visible', 'True')
        if self.Type == 'list':
            o.text = str(self.value)
        else:
            o.text = self.value
        return o
