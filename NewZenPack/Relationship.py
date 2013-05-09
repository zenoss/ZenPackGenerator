#!/usr/bin/env python
##LICENSE##

import unittest
from Component import Component
lookup = Component.lookup

class Relationship(object):
    """ZenPack Relationship"""

    def __init__(self,ZenPack, ComponentA,ComponentB,Type='1-M',Contained=True):
        self.ZenPack = ZenPack
        self.components = lookup(ZenPack, ComponentA), lookup(ZenPack, ComponentB)
        self.id = (self.components[0].id,self.components[1].id)
        self.Type = Type
        self.Contained = Contained

        # Register the relationship on a zenpack so we can find it later.
        self.ZenPack.registerRelationship(self)

    def hasComponent(self, component):
        for c in self.components:
            if component.id == c.id:
                return True
        return False

    def hasManyChild(self, component):
        if self.components[0].id == component.id and '-M' in self.Type:
            return True
        if self.components[1].id == component.id and 'M-' in self.Type:
            return True
        return False

    def ManyChild(self,component):
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
                    import pdb;pdb.set_trace()
                    if relation.Contained and 'M' in relation.Type:
                        import pdb;pdb.set_trace()
                        for rc in relation.components:
                            if not c.id == rc.id:
                                 return rc.relname
        import pdb;pdb.set_trace()

    def first(self,component):
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
            return "('{0}', ToOne(ToOne, '{1}', '{2}',)),".format(compA.relname,
                                                                 compA.id,
                                                                 compB.relname)
        if self.Type == '1-M':
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
        if self.Type == 'M-M':
            return "('{0}', ToMany(ToMany{1}, '{2}', '{3}',)),".format(compA.relnames,
                                                                      contained,
                                                                      compA.id,
                                                                      compB.relnames)

#Unit tests Start here
class SimpleSetup(unittest.TestCase):
    def setUp(self):
        from ZenPack import ZenPack
        self.zp = ZenPack('a.b.c')

#class TestComponentCreate(SimpleSetup):
#    def test_ComponentCreate(self):
#        c = Component('Component',self.zp)
#        self.assertIsInstance(c, Component)

if __name__ == "__main__":
    from ZenPack import ZenPack
    zp = ZenPack('ZenPacks.zenoss.CiscoMonitor')
    i1 = zp.addComponent('Interface',
                         Classes = ['Products.ZenModel.IpInterface'])
    v1 = zp.addComponent('VRF')
    c1 = zp.addComponent('CiscoDevice')
    vl1 = zp.addComponent('VLAN')
    rel = Relationship(zp,'CiscoDevice','VRF')
    rel = Relationship(zp,'Interface','VLAN')
    rel1 = Relationship(zp,'Interface','VRF', Type='1-M', Contained=False)
    rel2 = Relationship(zp,'Interface','VLAN', Type='M-M', Contained=False)
    
    print 'CiscoDevice'
    print rel.toString(c1)

    print 'VRF'
    print rel.toString(v1)

    print 'Interface'
    print rel1.toString(i1)

    print 'VRF'
    print rel1.toString(v1)

    print 'VLAN'
    print rel2.toString(vl1)

    print "Interface Custom Paths"
    i1.customPaths()

    unittest.main()
