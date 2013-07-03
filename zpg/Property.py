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

plural = inflect.engine().plural


class Property(object):

    """Define a properties capabilities inside a Component."""

    def __init__(self,
                 name,
                 value=None,
                 Type=None,
                 width=10,
                 detailDisplay=True,
                 gridDisplay=True,
                 sortable=True,
                 panelRenderer=None):
        """Args:
             name: Property name
             value: default value [None]
             Type: type of property [None]
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
        self.value = value
        self.detailDisplay = detailDisplay
        self.gridDisplay = gridDisplay
        self.sortable = True
        self.width = width
        self.panelRenderer = panelRenderer
        self.Type = Type if Type else value
        self.value = value

    def Schema(self):
        """Given the type return the correct Schema."""
        if self.Type.lower() in ['int']:
            return 'Int'
        elif self.Type.lower() in ['string', 'text', 'list']:
            return 'TextLine'
        elif self.Type.lower() in ['bool']:
            return 'Bool'
        else:
            return 'TextLine'

    @property
    def Type(self):
        """Return the type"""
        return self._Type

    @Type.setter
    def Type(self, Type):
        """Input validation for the type"""
        self._Type = None
        # Zope Types we are supporting
        valid_zope_types = ['string', 'text', 'list', 'lines', 'int', 'bool',
                            'long', 'boolean', 'float', 'password']
        # All Zope types
        # boolean,date,float,int,list,
        # long,string,text,tokens,selection,multiple_selection
        if Type is not None and Type in valid_zope_types:
            self._Type = Type
            if self._Type == 'lines':
                self._Type = 'list'
        else:
            if isinstance(Type, str):
                self._Type = 'string'
            elif isinstance(Type, bool):
                self._Type = 'boolean'
            elif isinstance(Type, int):
                self._Type = 'int'
            elif isinstance(Type, float):
                self._Type = 'float'
            elif isinstance(Type, list):
                self._Type = 'list'
        # Default return of string
        if not self._Type:
            self._Type = 'string'

    @property
    def value(self):
        """Return the value"""
        return self._value

    @value.setter
    def value(self, value):
        """Input validation for the value"""
        # Valid values can be implemented later.
        self._value = 'None' if value is None else value

    def to_objects_xml(self):
        o = etree.Element("property")
        o.set('id', self.id)
        o.set('type', self.Type)
        if self.id not in ['zendoc', 'description']:
            o.set('visible', 'True')
        try:
            if self.Type == 'list':
                o.text = str(self.value)
            else:
                o.text = self.value
        except Exception:
            import pdb
            pdb.set_trace()
        return o
