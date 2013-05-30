#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################


import inflect

plural = inflect.engine().plural


class Property(object):
    '''Define a properties capabilities inside a Component.'''
    def __init__(self,
                 name,
                 value=None,
                 Type=None,
                 width=10,
                 detailDisplay=True,
                 gridDisplay=True,
                 sortable=True,
                 panelRenderer=None):
        '''Args:
                 name: Property name
                 value: default value [None]
                 Type: type of property [None]
                       valid types: ['string', 'text', 'lines', 'int', 'bool',
                                     'long', 'boolean', 'float', 'password']
                       If a value is set and no type is set the type will be determined
                       from the value'
                 width: pixel width of the column in the ui
                 detailDisplay: Show this property in the details section of the UI [True/False]
                 gridDisplay: Show this property in the grid section of the UI [True/False]
                 sortable: Sortable Property [True/False]
                 panelRenderer: Define a custom panel renderer
        '''

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

        if Type:
            self.Type = Type
        else:
            self.Type = value

        self.value = value

    def Schema(self):
        '''Given the type return the correct Schema.'''

        if self.Type in ['int']:
            return 'Int'
        elif self.Type in ['string', 'text', 'lines']:
            return 'TextLine'
        elif self.Type in ['bool']:
            return 'Bool'
        else:
            return 'TextLine'

    @property
    def Type(self):
        '''Return the type'''
        return self._Type

    @Type.setter
    def Type(self, Type):
        '''Input validation for the type'''

        self._Type = None

        # Zope Types we are supporting
        ValidTypes = ['string', 'text', 'lines',
                      'int', 'bool', 'long', 'boolean',
                      'float', 'password']

        # All Zope types
        #boolean,date,float,int,lines,
        #long,string,text,tokens,selection,multiple_selection

        if Type and Type in ValidTypes:
            self._Type = Type
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
                self._Type = 'lines'

        # Default return of string
        if not self._Type:
            self._Type = 'string'

    @property
    def value(self):
        '''Return the value'''
        return self._value

    @value.setter
    def value(self, value):
        '''Input validation for the value'''

        # Valid values can be implemented later.
        if value is None:
            self._value = 'None'
        else:
            self._value = value

    #def __call__(self):
    #    '''return the value by default from a property instance.'''
    #    return self.value
