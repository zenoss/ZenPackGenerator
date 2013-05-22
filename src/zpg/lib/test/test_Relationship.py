import unittest
from zpg.lib.Component import Component
from zpg.lib.ZenPack import ZenPack
from zpg.lib.Relationship import Relationship

#Unit tests Start here
class SimpleSetup(unittest.TestCase):
    def setUp(self):
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


class TestRelationship_FindComponentsContainment(SimpleSetup):
    def test_ReturnsContainedRelationships(self):
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
        d = Component('Device', self.zp)
        c = Component('Component', self.zp)
        r = Relationship(self.zp, 'Device', 'Component')
        self.assertEqual("('components', ToManyCont(ToOne, 'a.b.c.Component', 'device',)),", r.toString(d))
        self.assertEqual("('device', ToOne(ToManyCont, 'a.b.c.Device', 'components',)),", r.toString(c))

    def test_returnsOneToMany(self):
        d2 = Component('Device2', self.zp)
        c2 = Component('Component2', self.zp)
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
