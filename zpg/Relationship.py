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


class Relationship(object):
    '''ZenPack Relationship Management'''

    valid_relationship_types = ['1-M', 'M-M', '1-1']
    relationships = {}

    def __init__(self,
                 ZenPack,
                 componentA,
                 componentB,
                 relnameA=None,
                 relnameB=None,
                 type_=None,
                 contained=True,
                 *args,
                 **kwargs
                 ):
        """Args:
                ZenPack:  A ZenPack Class instance
                componentA: Parent component string id
                componentB: Child component string id
                relnameA: Name of relationship from parent to child (default is
                          based upon componentB)
                relnameB: Name of relationship from child to parent (default is
                          based upon componentA)
                type_: Relationship type_.  Valid inputs [1-1, 1-M, M-M]
                contained: ComponentA contains ComponentB True or False
        """
        self.ZenPack = ZenPack
        from .Component import Component

        self.logger = logger = logging.getLogger('ZenPack Generator')
        name = "-".join([componentA, componentB])
        layer = "%s:%s" % (self.__class__.__name__, name)

        self.type_ = type_
        self.contained = contained
        for key in kwargs:
            do_not_warn = False
            msg = "WARNING: [%s] unknown keyword ignored in file: '%s'"
            margs = (layer, key)
            if key == "Type":
                msg = "WARNING: [%s] keyword deprecated: "\
                      "'%s' is now '%s'."
                margs = (layer, key, key.lower())
                self.type_ = kwargs[key]
            elif key == "type":
                self.type_ = type_ = kwargs[key]
                do_not_warn = True
            elif key == "Contained":
                msg = "WARNING: [%s] keyword deprecated: "\
                      "'%s' is now '%s'."
                margs = (layer, key, key.lower())
                self.contained = kwargs[key]
            if not do_not_warn:
                warn(self.logger, yellow(msg) % margs)
        if type_ not in self.valid_relationship_types:
            msg = "WARNING: [%s] unknown type: '%s'.  Defaulted to '%s'. "
            layer = "%s:%s" % (self.__class__.__name__, name)
            margs = (layer, type, '1-M')
            if type_ == 'M-1':
                a_b = (componentA, componentB)
                msg += "Reversed '%s' and '%s'." % a_b
                swap = componentB
                componentB = componentA
                componentA = swap
            if type_ is not None:
                warn(self.logger, yellow(msg) % margs)
            type_ = '1-M'

        lookup = Component.lookup
        self.components = lookup(
            ZenPack, componentA), lookup(ZenPack, componentB)
        self.id = '%s %s' % (self.components[0].id, self.components[1].id)

        if relnameA is None:
            relnameA = self.relname(lookup(ZenPack, componentB))
        if relnameB is None:
            relnameB = self.relname(lookup(ZenPack, componentA))

        self.relnames = (relnameB, relnameA)

        # Register the relationship on a zenpack so we can find it later.
        self.ZenPack.registerRelationship(self)

        Relationship.relationships[self.id] = self

    def hasComponent(self, component):
        '''Return True if this relationship has this component inside.'''
        for c in self.components:
            if component.id == c.id:
                return True
        return False

    def hasChild(self, component):
        '''Return True if this relationship has this component inside
           in the child position.'''
        if component.id == self.components[1].id:
            return True
        return False

    @classmethod
    def find(self, component, contained=None, first=None, types=None):
        '''return all the relationships that match the input request.

           Args:
              component: A parent or child component in this relationship
              contained: True/False containment relationship
              first: True/False  True if we are searching for the Parent
                                 Component in the relationship.

              types_: 1-1, 1-M, M-M are valid relationship types_.
                     1-1: One to One
                     1-M: One to Many
                     M-M: Many to Many
        '''

        rels = []
        for rel in Relationship.relationships.values():
            if rel.hasComponent(component):
                if not contained is None:
                    if not rel.contained == contained:
                        continue
                if not first is None:
                    if not rel.first(component) == first:
                        continue
                if not types is None:
                    if isinstance(types, basestring):
                        if rel.type_ == types:
                            continue
                    else:
                        if not rel.type_ in types:
                            continue

                rels.append(rel)
        return sorted(rels)

    def first(self, component):
        '''Is this the first component in the relationship'''
        if component.id == self.components[0].id:
            return True
        return False

    def child(self):
        '''Return the child component.'''
        return self.components[1]

    def relname(self, component):
        '''Return the singular or plural form of the relname based on the
        component as the frame of reference'''

        typeTuple = self.type_.split('-')

        if self.first(component):
            type_ = typeTuple[0]
        else:
            type_ = typeTuple[1]

        if type_ == '1':
            return component.relname
        else:
            return component.relnames

    def toString(self, component):
        '''Write the relationship into a string format based on the component
           as a frame of reference. This is a 3.X and 4.X string format.'''

        if self.first(component):
            compA = self.components[1]
            relnameB = self.relnames[1]
            compB = self.components[0]
            relnameA = self.relnames[0]
        else:
            compA = self.components[0]
            relnameB = self.relnames[0]
            compB = self.components[1]
            relnameA = self.relnames[1]            

        if self.contained:
            contained = 'Cont'
        else:
            contained = ''

        if self.type_ == '1-1':
            direction = 'ToOne(ToOne'
            return "('{0}', {1}, '{2}', '{3}',)),".format(relnameB,
                                                          direction,
                                                          compA.id,
                                                          relnameA)
        elif self.type_ == '1-M':
            if self.first(component):
                direction = 'ToMany{0}(ToOne'.format(contained)
                return "('{0}', {1}, '{2}', '{3}',)),".format(relnameB,
                                                              direction,
                                                              compA.id,
                                                              relnameA)
            else:
                direction = 'ToOne(ToMany{0}'.format(contained)
                return "('{0}', {1}, '{2}', '{3}',)),".format(relnameB,
                                                              direction,
                                                              compA.id,
                                                              relnameA)
        elif self.type_ == 'M-M':
            if self.first(component):
                direction = 'ToMany(ToMany{0}'.format(contained)

            else:
                direction = 'ToMany{0}(ToMany'.format(contained)

            return "('{0}', {1}, '{2}', '{3}',)),".format(relnameB,
                                                          direction,
                                                          compA.id,
                                                          relnameA)
