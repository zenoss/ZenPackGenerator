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
    """ZenPack Relationship"""

    relationships = {}

    def __init__(self, ZenPack, ComponentA, ComponentB, Type='1-M', Contained=True):

        self.ZenPack = ZenPack
        from Component import Component
        lookup = Component.lookup
        self.components = lookup(ZenPack, ComponentA), lookup(ZenPack, ComponentB)
        self.id = (self.components[0].id, self.components[1].id)
        self.Type = Type
        self.Contained = Contained

        # Register the relationship on a zenpack so we can find it later.
        self.ZenPack.registerRelationship(self)

        Relationship.relationships[self.id] = self

    def hasComponent(self, component):
        for c in self.components:
            if component.id == c.id:
                return True
        return False

    @classmethod
    def find(self, component, Contained=None, First=None, Types=None):
        rels = []
        for rel in Relationship.relationships.values():
            if rel.hasComponent(component):
                if Contained and not rel.Contained == Contained: continue
                if First and not rel.first(component) == First: continue
                if isinstance(Types, basestring):
                    if rel.Type == Types: continue
                else:
                    if Types and not rel.Type in Types: continue
                rels.append(rel)
        return rels

    '''
    def hasManyChild(self, component):
        if self.components[0].id == component.id and '-M' in self.Type:
            return True
        if self.components[1].id == component.id and 'M-' in self.Type:
            return True
        return False


    def ManyChild(self, component):
        if self.components[0].id == component.id and '-M' in self.Type:
            return self.components[1]
        if self.components[1].id == component.id and 'M-' in self.Type:
            return self.components[0]
        return None

    def getParentPath(self, component):
        for c in self.components:
            if not c == component:
                relations = [rel for rel in self.ZenPack.relationships.values() if rel.hasComponent(c)]
                for relation in relations:
                    print relation.id
                    print c.id
                    if relation.Contained and 'M' in relation.Type:
                        for rc in relation.components:
                            if not c.id == rc.id:
                                return rc.relname
    '''

    def first(self, component):
        '''Is this the first component in the relationship'''
        if component.id == self.components[0].id:
            return True
        return False

    def toString(self, component):
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
        c = Component('SampleComponent', self.zp)
        r = Relationship(self.zp, 'SampleDevice', 'SampleComponent')
        self.assertEqual(True, r.hasComponent(c))

    def test_HasComponent_False(self):
        c = Component('SampleComponent', self.zp)
        r = Relationship(self.zp, 'SampleDevice', 'SampleComponent2')
        self.assertEqual(False, r.hasComponent(c))


class TestRelationship_FindComponents(SimpleSetup):
    def test_ReturnsCorrectRelationships(self):
        c = Component('SampleComponent', self.zp)
        r = Relationship(self.zp, 'SampleDevice', 'SampleComponent')
        self.assertEqual([r], Relationship.find(c))

    def test_ReturnsNoRelationships(self):
        c2 = Component('SampleComponent2', self.zp)
        Relationship(self.zp, 'SampleDevice', 'SampleComponent')
        self.maxDiff = None
        self.assertEqual([], Relationship.find(c2))

    def test_ReturnsContainedRelationships(self):
        c = Component('SampleComponent', self.zp)
        c3 = Component('SampleComponent3', self.zp)
        r = Relationship(self.zp, 'SampleDevice', 'SampleComponent')
        r3 = Relationship(self.zp, 'SampleComponent3', 'SampleComponent4', Contained=False)
        Relationship(self.zp, 'SampleComponent3', 'SampleComponent5')
        self.assertEqual([r], Relationship.find(c, Contained=True))
        self.assertEqual([r3], Relationship.find(c3, Contained=False))

class TestRelationship_stringoutput(SimpleSetup):
    def test_returnsOneToManyCont(self):
        d = Component('Device', self.zp)
        c = Component('Component',self.zp)
        r = Relationship(self.zp, 'Device', 'Component')
        self.assertEqual("('components', ToManyCont(ToOne, 'a.b.c.Component', 'device',)),", r.toString(d))
        self.assertEqual("('device', ToOne(ToManyCont, 'a.b.c.Device', 'components',)),", r.toString(c))

    def test_returnsOneToMany(self):
        d2 = Component('Device2', self.zp)
        c2 = Component('Component2',self.zp)
        r2 = Relationship(self.zp, 'Device2', 'Component2', Contained=False)
        self.assertEqual("('component2s', ToMany(ToOne, 'a.b.c.Component2', 'device2',)),", r2.toString(d2))
        self.assertEqual("('device2', ToOne(ToMany, 'a.b.c.Device2', 'component2s',)),", r2.toString(c2))

    def test_returnsOneToOne(self):
        d3 = Component('Device3', self.zp)
        c3 = Component('Component3', self.zp)
        r3 = Relationship(self.zp, 'Device3', 'Component3', Contained=False, Type='1-1')
        self.assertEqual("('component3', ToOne(ToOne, 'a.b.c.Component3', 'device3',)),", r3.toString(d3))
        self.assertEqual("('device3', ToOne(ToOne, 'a.b.c.Device3', 'component3',)),", r3.toString(c3))

    def test_returnsManyToManyCont(self):
        d4 = Component('Device4', self.zp)
        c4 = Component('Component4', self.zp)
        r4 = Relationship(self.zp, 'Device4', 'Component4', Type='M-M')
        self.assertEqual("('component4s', ToMany(ToManyCont, 'a.b.c.Component4', 'device4s',)),", r4.toString(d4))
        self.assertEqual("('device4s', ToManyCont(ToMany, 'a.b.c.Device4', 'component4s',)),", r4.toString(c4))

    def test_returnsManyToMany(self):
        d5 = Component('Device5', self.zp)
        c5 = Component('Component5', self.zp)
        r5 = Relationship(self.zp, 'Device5', 'Component5', Contained=False, Type='M-M')
        self.assertEqual("('component5s', ToMany(ToMany, 'a.b.c.Component5', 'device5s',)),", r5.toString(d5))
        self.assertEqual("('device5s', ToMany(ToMany, 'a.b.c.Device5', 'component5s',)),", r5.toString(c5))


if __name__ == "__main__":
    unittest.main()
