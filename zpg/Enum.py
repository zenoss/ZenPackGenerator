#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

from .colors import error, warn, debug, info, green, red, yellow


class Enum(object):
    ''' Enum Object '''

    Enums = {}

    def __init__(self,
                 zenpack,
                 name,
                 values,
                 *args,
                 **kwargs
                 ):
        """Args:
             zenpack: the containing zenpack
        """
        for key in kwargs:
            do_not_warn = False
            clsname = self.__class__.__name__
            layer = "%s:%s" % (clsname, self.name)
            msg = "WARNING: [%s] unknown keyword ignored in file: '%s'"
            margs = (layer, key)
            if not do_not_warn:
                warn(self.logger, yellow(msg) % margs)

        self.zenpack = zenpack
        self.id = name
        self.values = {}

        if isinstance(values, list):
            if isinstance(values[0], list):
                for value in values:
                    self.values[value[0]] = str(value[1])
            else:
                for i, value in enumerate(values):
                    self.values[i+1] = str(value)

        elif isinstance(values, dict):
            self.values = values

        # Create a string representation
        self.value = "%s = {}\n" % self.id
        for key in self.values.keys():
            val = self.values[key]
            if isinstance(val, basestring):
                self.value += "%s[%s] = '%s'\n" % (self.id, key, val)
            else:
                self.value += "%s[%s] = %s\n" % (self.id, key, val)

        Enum.Enums[self.id] = self
        self.zenpack.registerEnum(self)
