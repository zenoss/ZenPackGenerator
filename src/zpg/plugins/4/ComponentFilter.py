#!/usr/bin/env python
import logging
import os
logging.basicConfig()
log = logging.getLogger('Component Filter')
from zpg.utils import KlassExpand

class ComponentFilter(object):
    type = 'filter'
    def __init__(self,config,opts):
        self.config = config
        self.basedir = opts.dest
        self.imports = ['from zope.component import implements',
                        'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
                        'from Products.Zuul.decorators import info',
                        'from Products.Zuul.form import schema',
                        'from Products.Zuul.infos import ProxyProperty',
                        'from Products.Zuul.utils import ZuulMessageFactory as _t',
                       ]
        self.components = self.config['component'].keys()

    def relationMap(self,rel,rev=False):
        relation = []
        if rev:
            rel = "-".join(reversed(rel.split('-')))
        for char in rel:
            if char == '1':
                relation.append('ToOne')
            elif char == '-':
                relation.append('(')
            if char == 'M':
                relation.append('ToMany')
            if char == 'C':
                relation.append('Cont')
        return "".join(relation)

    def updateCustomPathReporter(self,rel,component):
        # custom_path_reporters
        if rel[1] in ['1-M','M-M']:
            custom_path = self.config['component'][component]['custom_path']
            oneToManyContRelations = [item for item in self.config['Relations'] if item[1] == '1-MC']
            for item in oneToManyContRelations:
                if KlassExpand(self.config,component,[rel[2][1]]) == KlassExpand(self.config,component,[item[2][1]]):
                    if (rel[2][0],item[0][0]) not in custom_path[rel[1]]:
                        custom_path[rel[1]].append((rel[2][0],item[0][0]))
                        self.config['custom_path_reporter'] = True
            self.config['component'][component]['custom_path'] = custom_path
        
    def updateImports(self):
        def updateImports(i):
            if 'imports' in self.config['component'][component]:
                if i not in self.config['component'][component]['imports']:
                   self.config['component'][component]['imports'].append(i) 
            else:
                self.config['component'][component]['imports'] = [i]

        for component in self.components:
            # Main Imports
            for i in self.imports:
                updateImports(i)

            # Class imports
            klasses = KlassExpand(self.config,component)
            for klass in klasses:
                i = "from %s import %s" % (".".join(klass),klass[1])
                updateImports(i)
  
            #Info and interface imports
            if self.config['component'][component]['Device']:
                updateImports("from Products.Zuul.infos.device import DeviceInfo")
                updateImports("from Products.Zuul.interface.device import IDeviceInfo")
            else:
                updateImports("from Products.Zuul.infos.component import ComponentInfo")
                updateImports("from Products.Zuul.interface.component import IComponentInfo")

    def updatePathImports(self):
        for component in self.components:
            custom_path = self.config['component'][component]['custom_path']
            if custom_path['M-M'] or custom_path['1-M']:
                self.config['component'][component]['imports'].append( \
                    "from Products.Zuul.catalog.paths import DefaultPathReporter, relPath")

    def updateRelImports(self):
        rel = []
        for component in self.components:
            for relation in self.config['component'][component]['relations']:
                if 'ToOne' in relation and 'ToOne' not in rel:
                    rel.append('ToOne')
                if 'ToManyCont' in relation and 'ToManyCont' not in rel:
                    rel.append('ToManyCont')
                if 'ToMany(' in relation and 'ToMany' not in rel:
                    rel.append('ToMany')
                if 'ToMany,' in relation and 'ToMany' not in rel:
                    rel.append('ToMany')

            if rel:
                try:
                    self.config['component'][component]['imports'].append( \
                        "from Products.ZenRelations.RelSchema import %s" %\
                        ", ".join(sorted(set(rel))))
                except Exception:
                    self.config['component'][component]['imports']=[]

    def updateRelations(self):
        for component in self.components:
         
            if 'custom_path' not in self.config['component'][component]:
                self.config['component'][component]['custom_path'] = {'M-M': [], '1-M': []}
            if 'count_rels' not in self.config['component'][component]:
                self.config['component'][component]['count_rels'] = []


            self.config['component'][component]['relations'] = [] 
            unique_name = self.config['component'][component]['unique_name']
            component_classes = KlassExpand(self.config,component,component)
            
            for relation in self.config['Relations']:
                relationship = None
                classes = KlassExpand(self.config,component,[relation[0][1],relation[2][1]])
                if classes[0] in component_classes:
                    relationship =  "('%s', %s, %s, '%s'))," % \
                        (relation[2][0],self.relationMap(relation[1],rev=True),".".join(classes[1]),relation[0][0])
                    # data for relationship count methods
                    if '-M' in relation[1]:
                        self.config['component'][component]['count_rels'].append((relation[2][0],unique_name))

                if classes[1] in component_classes:
                    relationship =  "('%s', %s, %s, '%s'))," % \
                        (relation[0][0],self.relationMap(relation[1]),".".join(classes[0]),relation[2][0])
                    # data for relationship count methods
                    if '1-' not in relation[1]:
                        self.config['component'][component]['count_rels'].append((relation[0][0],unique_name))

                if relationship:
                    self.config['component'][component]['relations'].append(relationship)
                    self.updateCustomPathReporter(relation,component)

 
            for rel in self.config['component'][component]['count_rels']:
                if 'dropdown' not in self.config:
                    self.config['dropdown'] = {}
                
                # skip device components 
                if self.config['component'][component]['Device']:
                    continue 

                if rel[0] not in self.config['dropdown']:
                    self.config['dropdown'][rel[0]] = [rel[1]]
                else:
                    self.config['dropdown'][rel[0]].append(rel[1])
            
    def run(self):
        if 'component' not in self.config:
            self.config['component'] = {}

        for component in self.config['component']:
            # replace the component shorthand
            if self.config['component'][component]['class'].lower() == 'component':
                self.config['component'][component]['class'] = ['DeviceComponent','ManagedEntity']
           
            # Supply default of false if it is not a Device Component
            if 'Device' not in self.config['component'][component]:
                self.config['component'][component]['Device'] = False

        self.updateRelations()
        self.updateImports()
        self.updateRelImports()
        self.updatePathImports()
        return self.config
