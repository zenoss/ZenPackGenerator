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

from .colors import error, warn, debug, info, green, red, yellow
from ._zenoss_utils import KlassExpand
from .Relationship import Relationship
find = Relationship.find


class DeviceClass(object):

    '''Device Class Container'''
    deviceClasses = {}

    def __init__(self,
                 ZenPack,
                 path,
                 prefix='/zport/dmd',
                 zPythonClass='Products.ZenModel.Device.Device',
                 componentTypes=None,
                 deviceType=None,
                 *args,
                 **kwargs
                 ):
        '''Args:
                 path: Destination device class path (the prefix is
                        automatically prepended)
                 ZenPack: ZenPack Class Instance
                 prefix: Destination device class prefix [/zport/dmd]
                 zPythonClass: The zPythonClass this Device Class references.
                               [Products.ZenModel.Device]
                 componentTypes: an array of dictionaries used to create
                                  components.
                 deviceType: a dictionary used to create a device component.
        '''

        self.zenpack = ZenPack
        self.path = '/'.join([prefix, path.lstrip('/')])
        self.id = self.path
        self.subClasses = {}
        self.zPythonClass = KlassExpand(self.zenpack, zPythonClass)
        self.logger = logger = logging.getLogger('ZenPack Generator')
        for key in kwargs:
            do_not_warn = False
            layer = self.__class__.__name__
            msg = "WARNING: JSON keyword ignored in layer '%s': '%s'"
            margs = (layer, key)
            if not do_not_warn:
                warn(self.logger, yellow(msg) % margs)
        if deviceType:
            self.DeviceType(**deviceType)
        else:
            self.DeviceType()

        DeviceClass.deviceClasses[self.id] = self
        self.zenpack.registerDeviceClass(self)

        # Dict loading
        if componentTypes:
            for component in componentTypes:
                self.addComponentType(**component)

    def DeviceType(self, *args, **kwargs):
        '''Create a deviceType component from a zPythonClass reference'''
        if 'name' in kwargs:
            self.deviceType = self.zenpack.addComponentType(
                device=True, *args, **kwargs)
        else:
            self.deviceType = self.zenpack.addComponentType(
                self.zPythonClass, device=True, *args, **kwargs)

    def addClass(self, deviceClass, *args, **kwargs):
        '''Create a sub device class'''

        if 'prefix' in kwargs:
            del(kwargs['prefix'])

        if 'zPythonClass' in kwargs:
            return DeviceClass(self.zenpack,
                               deviceClass,
                               prefix=self.path,
                               *args,
                               **kwargs)
        else:
            return DeviceClass(self.zenpack,
                               deviceClass,
                               prefix=self.path,
                               zPythonClass=self.zPythonClass,
                               *args,
                               **kwargs)

    def addComponentType(self, *args, **kwargs):
        '''Add a component to the deviceType component'''

        if 'zenpack' not in kwargs:
            kwargs['zenpack'] = self.zenpack
        c = self.deviceType.addComponentType(*args, **kwargs)
        return c

    @property
    def componentTypes(self):
        '''Return the component types defined inside this deviceClass.
           Including child components.
        '''

        def ComponentFind(child=None):
            components = []
            if child:
                rels = find(child, first=True)
                for rel in rels:
                    newchild = rel.child()
                    components.append(newchild)
                    if newchild != child:
                        rval = ComponentFind(newchild)
                        if rval:
                            components = components + rval
            return components
        components = ComponentFind(self.deviceType)
        return sorted(components)
