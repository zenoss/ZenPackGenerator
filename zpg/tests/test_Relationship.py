#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

import unittest
from zpg.Component import Component
from zpg.ZenPack import ZenPack
from zpg.Relationship import Relationship

# Unit tests Start here


class SimpleSetup(unittest.TestCase):

    def setUp(self):
        self.zp = ZenPack('a.b.c')

    def tearDown(self):
        del(self.zp)


class TestRelationshipCreate(SimpleSetup):

    def test_RelationshipCreate_Defaults(self):
        '''test the defaults when creating a relationship.'''
        r = Relationship(self.zp, 'CiscoDevice', 'VRF')
        self.assertIsInstance(r, Relationship)

    def test_RelationshipCreate_Overrides(self):
        '''test the defaults when creating a relationship.'''
        r = Relationship(self.zp, 'CiscoDevice', 'VRF', contained=False)
        self.assertIsInstance(r, Relationship)

        r = Relationship(self.zp, 'CiscoDevice', 'VRF', type_='1-1')
        self.assertIsInstance(r, Relationship)


class TestRelationship_HasComponent(SimpleSetup):

    def test_HasComponent_True(self):
        c = self.zp.addComponentType('SampleComponent')
        r = Relationship(self.zp, 'SampleDevice', 'SampleComponent')
        self.assertEqual(True, r.hasComponent(c))

    def test_HasComponent_False(self):
        c = self.zp.addComponentType('SampleComponent')
        r = Relationship(self.zp, 'SampleDevice', 'SampleComponent2')
        self.assertEqual(False, r.hasComponent(c))


class TestRelationship_FindComponents(SimpleSetup):

    def test_ReturnsCorrectRelationships(self):
        c = self.zp.addComponentType('SampleComponent')
        r = Relationship(self.zp, 'SampleDevice', 'SampleComponent')
        self.assertEqual([r], Relationship.find(c))
        self.assertEqual([], Relationship.find(c, types='1-M'))
        self.assertEqual([r], Relationship.find(c, types=['1-M', 'M-M']))
        self.assertEqual([], Relationship.find(c, types=['1-1']))

    def test_ReturnsNoRelationships(self):
        c2 = self.zp.addComponentType('SampleComponent2')
        Relationship(self.zp, 'SampleDevice', 'SampleComponent')
        self.maxDiff = None
        self.assertEqual([], Relationship.find(c2))


class TestRelationship_FindComponentsContainment(SimpleSetup):

    def test_ReturnsContainedRelationships(self):
        c = Component(self.zp, 'SampleComponent')
        c3 = Component(self.zp, 'SampleComponent3')
        r = Relationship(self.zp, 'SampleDevice', 'SampleComponent')
        r3 = Relationship(
            self.zp, 'SampleComponent3', 'SampleComponent4', contained=False)
        Relationship(self.zp, 'SampleComponent4', 'SampleComponent5')
        self.maxDiff = None
        self.assertEqual([r], Relationship.find(c, contained=True))
        self.assertEqual([r3], Relationship.find(c3, contained=False))


class TestRelationship_stringoutput(SimpleSetup):

    def test_returnsOneToManyCont(self):
        d = Component(self.zp, 'Device')
        c = Component(self.zp, 'Component')
        r = Relationship(self.zp, 'Device', 'Component')
        self.assertEqual(
            "('components', ToManyCont(ToOne, 'a.b.c.Component', 'device',)),", r.toString(d))
        self.assertEqual(
            "('device', ToOne(ToManyCont, 'a.b.c.Device', 'components',)),", r.toString(c))

    def test_returnsOneToMany(self):
        d2 = Component(self.zp, 'Device2')
        c2 = Component(self.zp, 'Component2')
        r2 = Relationship(self.zp, 'Device2', 'Component2', contained=False)
        self.assertEqual(
            "('component2s', ToMany(ToOne, 'a.b.c.Component2', 'device2',)),", r2.toString(d2))
        self.assertEqual(
            "('device2', ToOne(ToMany, 'a.b.c.Device2', 'component2s',)),", r2.toString(c2))

    def test_returnsOneToOne(self):
        d3 = Component(self.zp, 'Device3')
        c3 = Component(self.zp, 'Component3')
        r3 = Relationship(
            self.zp, 'Device3', 'Component3', contained=False, type_='1-1')
        self.assertEqual(
            "('component3', ToOne(ToOne, 'a.b.c.Component3', 'device3',)),", r3.toString(d3))
        self.assertEqual(
            "('device3', ToOne(ToOne, 'a.b.c.Device3', 'component3',)),", r3.toString(c3))

    def test_returnsManyToManyCont(self):
        d4 = Component(self.zp, 'Device4')
        c4 = Component(self.zp, 'Component4')
        r4 = Relationship(self.zp, 'Device4', 'Component4', type_='M-M')
        self.assertEqual(
            "('component4s', ToMany(ToManyCont, 'a.b.c.Component4', 'device4s',)),", r4.toString(d4))
        self.assertEqual(
            "('device4s', ToManyCont(ToMany, 'a.b.c.Device4', 'component4s',)),", r4.toString(c4))

    def test_returnsManyToMany(self):
        d5 = Component(self.zp, 'Device5')
        c5 = Component(self.zp, 'Component5')
        r5 = Relationship(
            self.zp, 'Device5', 'Component5', contained=False, type_='M-M')
        self.assertEqual(
            "('component5s', ToMany(ToMany, 'a.b.c.Component5', 'device5s',)),", r5.toString(d5))
        self.assertEqual(
            "('device5s', ToMany(ToMany, 'a.b.c.Device5', 'component5s',)),", r5.toString(c5))

if __name__ == '__main__':
    unittest.main()
