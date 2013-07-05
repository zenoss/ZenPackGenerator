#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#


class Relationship(object):

    '''ZenPack Relationship Management'''

    relationships = {}

    def __init__(self,
                 ZenPack,
                 ComponentA,
                 ComponentB,
                 Type='1-M',
                 Contained=True):
        """Args:
                ZenPack:  A ZenPack Class instance
                ComponentA: Parent Component string id
                ComponentB: Child Component string id
                Type: Relationship Type.  Valid inputs [1-1,1-M,M-M]
                Contained: ComponentA contains ComponentB True or False
        """
        self.ZenPack = ZenPack
        from Component import Component
        lookup = Component.lookup
        self.components = lookup(
            ZenPack, ComponentA), lookup(ZenPack, ComponentB)
        self.id = '%s %s' % (self.components[0].id, self.components[1].id)
        self.Type = Type
        self.Contained = Contained

        # Register the relationship on a zenpack so we can find it later.
        self.ZenPack.registerRelationship(self)

        Relationship.relationships[self.id] = self

    def hasComponent(self, component):
        '''Return True if this relationship has this component inside.'''
        for c in self.components:
            if component.id == c.id:
                return True
        return False

    @classmethod
    def findMatchingComponents(self, componentA, componentB):
        '''return all the relationships that match the input request.'''
        rels = []

        for rel in Relationship.relationships.values():
            if rel.hasComponent(componentA) and rel.hasComponent(componentB):
                rels.append(rel)
        return sorted(rels)

    @classmethod
    def find(self, component, Contained=None, First=None, Types=None):
        '''return all the relationships that match the input request.

           Args:
              component: A parent or child component in this relationship
              Contained: True/False containment relationship
              First: True/False  True if we are searching for the Parent
                                 Component in the relationship.

              Types: 1-1, 1-M, M-M are valid relationship types.
                     1-1: One to One
                     1-M: One to Many
                     M-M: Many to Many
        '''

        rels = []
        for rel in Relationship.relationships.values():
            if rel.hasComponent(component):
                if not Contained is None:
                    if not rel.Contained == Contained:
                        continue
                if not First is None:
                    if not rel.first(component) == First:
                        continue
                if not Types is None:
                    if isinstance(Types, basestring):
                        if rel.Type == Types:
                            continue
                    else:
                        if not rel.Type in Types:
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

    def toString(self, component):
        '''Write the relationship into a string format based on the component
           as a frame of reference. This is a 3.X and 4.X string format.'''

        if self.first(component):
            compA = self.components[1]
            compB = self.components[0]
        else:
            compA = self.components[0]
            compB = self.components[1]

        if self.Contained:
            contained = 'Cont'
        else:
            contained = ''

        if self.Type == '1-1':
            direction = 'ToOne(ToOne'
            return "('{0}', {1}, '{2}', '{3}',)),".format(compA.relname,
                                                          direction,
                                                          compA.id,
                                                          compB.relname)
        elif self.Type == '1-M':
            if self.first(component):
                direction = 'ToMany{0}(ToOne'.format(contained)
                return "('{0}', {1}, '{2}', '{3}',)),".format(compA.relnames,
                                                              direction,
                                                              compA.id,
                                                              compB.relname)
            else:
                direction = 'ToOne(ToMany{0}'.format(contained)
                return "('{0}', {1}, '{2}', '{3}',)),".format(compA.relname,
                                                              direction,
                                                              compA.id,
                                                              compB.relnames)
        elif self.Type == 'M-M':
            if self.first(component):
                direction = 'ToMany(ToMany{0}'.format(contained)

            else:
                direction = 'ToMany{0}(ToMany'.format(contained)

            return "('{0}', {1}, '{2}', '{3}',)),".format(compA.relnames,
                                                          direction,
                                                          compA.id,
                                                          compB.relnames)
