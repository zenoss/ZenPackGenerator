#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################

import unittest

class Relationship(object):
    '''ZenPack Relationship Management'''

    relationships = {}

    def __init__(self, ZenPack, ComponentA, ComponentB, Type='1-M', Contained=True):
        """Args:
                ZenPack:  A ZenPack Class instance
                ComponentA: Parent Component instance
                ComponentB: Child Component instance
                Type: Relationship Type.  Valid inputs [1-1,1-M,M-M]
                Contained: ComponentA contains ComponentB True or False
        """
        self.ZenPack = ZenPack
        from Component import Component
        lookup = Component.lookup
        self.components = lookup(ZenPack, ComponentA), lookup(ZenPack, ComponentB)
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
    def find(self, component, Contained=None, First=None, Types=None):
        '''return all the relationships that match the input request.

           Args:
              component: A parent or child component in this relationship
              Contained: True/False containment relationship
              First: True/False  True if we are searching for the Parent Component
                                 in the relationship.

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


#Unit tests Start here
class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from ZenPack import ZenPack
        self.zp = ZenPack('a.b.c')


class TestRelationshipCreate(SimpleSetup):
    def test_RelationshipCreate_Defaults(self):
        '''test the defaults when creating a relationship.'''
        r = Relationship(self.zp, 'CiscoDevice', 'VRF')
        self.assertIsInstance(r, Relationship)

    def test_RelationshipCreate_Overrides(self):
        '''test the defaults when creating a relationship.'''
        r = Relationship(self.zp, 'CiscoDevice', 'VRF', Contained=False)
        self.assertIsInstance(r, Relationship)

        r = Relationship(self.zp, 'CiscoDevice', 'VRF', Type='1-1')
        self.assertIsInstance(r, Relationship)


class TestRelationship_HasComponent(SimpleSetup):
    def test_HasComponent_True(self):
        from Component import Component
        c = Component('SampleComponent', self.zp)
        r = Relationship(self.zp, 'SampleDevice', 'SampleComponent')
        self.assertEqual(True, r.hasComponent(c))

    def test_HasComponent_False(self):
        from Component import Component
        c = Component('SampleComponent', self.zp)
        r = Relationship(self.zp, 'SampleDevice', 'SampleComponent2')
        self.assertEqual(False, r.hasComponent(c))


class TestRelationship_FindComponents(SimpleSetup):
    def test_ReturnsCorrectRelationships(self):
        from Component import Component
        c = Component('SampleComponent', self.zp)
        r = Relationship(self.zp, 'SampleDevice', 'SampleComponent')
        self.assertEqual([r], Relationship.find(c))

    def test_ReturnsNoRelationships(self):
        from Component import Component
        c2 = Component('SampleComponent2', self.zp)
        Relationship(self.zp, 'SampleDevice', 'SampleComponent')
        self.maxDiff = None
        self.assertEqual([], Relationship.find(c2))


class TestRelationship_FindComponentsContainment(SimpleSetup):
    def test_ReturnsContainedRelationships(self):
        from Component import Component
        c = Component('SampleComponent', self.zp)
        c3 = Component('SampleComponent3', self.zp)
        r = Relationship(self.zp, 'SampleDevice', 'SampleComponent')
        r3 = Relationship(self.zp, 'SampleComponent3', 'SampleComponent4', Contained=False)
        Relationship(self.zp, 'SampleComponent4', 'SampleComponent5')
        self.maxDiff = None
        self.assertEqual([r], Relationship.find(c, Contained=True))
        self.assertEqual([r3], Relationship.find(c3, Contained=False))


class TestRelationship_stringoutput(SimpleSetup):
    def test_returnsOneToManyCont(self):
        from Component import Component
        d = Component('Device', self.zp)
        c = Component('Component', self.zp)
        r = Relationship(self.zp, 'Device', 'Component')
        self.assertEqual("('components', ToManyCont(ToOne, 'a.b.c.Component', 'device',)),", r.toString(d))
        self.assertEqual("('device', ToOne(ToManyCont, 'a.b.c.Device', 'components',)),", r.toString(c))

    def test_returnsOneToMany(self):
        from Component import Component
        d2 = Component('Device2', self.zp)
        c2 = Component('Component2', self.zp)
        r2 = Relationship(self.zp, 'Device2', 'Component2', Contained=False)
        self.assertEqual("('component2s', ToMany(ToOne, 'a.b.c.Component2', 'device2',)),", r2.toString(d2))
        self.assertEqual("('device2', ToOne(ToMany, 'a.b.c.Device2', 'component2s',)),", r2.toString(c2))

    def test_returnsOneToOne(self):
        from Component import Component
        d3 = Component('Device3', self.zp)
        c3 = Component('Component3', self.zp)
        r3 = Relationship(self.zp, 'Device3', 'Component3', Contained=False, Type='1-1')
        self.assertEqual("('component3', ToOne(ToOne, 'a.b.c.Component3', 'device3',)),", r3.toString(d3))
        self.assertEqual("('device3', ToOne(ToOne, 'a.b.c.Device3', 'component3',)),", r3.toString(c3))

    def test_returnsManyToManyCont(self):
        from Component import Component
        d4 = Component('Device4', self.zp)
        c4 = Component('Component4', self.zp)
        r4 = Relationship(self.zp, 'Device4', 'Component4', Type='M-M')
        self.assertEqual("('component4s', ToMany(ToManyCont, 'a.b.c.Component4', 'device4s',)),", r4.toString(d4))
        self.assertEqual("('device4s', ToManyCont(ToMany, 'a.b.c.Device4', 'component4s',)),", r4.toString(c4))

    def test_returnsManyToMany(self):
        from Component import Component
        d5 = Component('Device5', self.zp)
        c5 = Component('Component5', self.zp)
        r5 = Relationship(self.zp, 'Device5', 'Component5', Contained=False, Type='M-M')
        self.assertEqual("('component5s', ToMany(ToMany, 'a.b.c.Component5', 'device5s',)),", r5.toString(d5))
        self.assertEqual("('device5s', ToMany(ToMany, 'a.b.c.Device5', 'component5s',)),", r5.toString(c5))


if __name__ == "__main__":
    unittest.main()

