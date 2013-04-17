#!/usr/bin/env python
import logging
import os
logging.basicConfig()
log = logging.getLogger('Setup')
from zpg.utils import KlassExpand

class ComponentFilter(object):
    type = 'filter'
    def __init__(self,config,basedir):
        self.config = config
        self.config
        self.basedir = basedir
        self.imports = ['from zope.component import adapts',
                        'from zope.component import implements',
                        'from Products.Zuul.decorators import info',
                        'from Products.Zuul.form import schema',
                        'from Products.Zuul.infos import ProxyProperty',
                        'from Products.Zuul.utils import ZuulMessageFactory as _t',
                       ]
        self.components = self.config['component'].keys()
        self.custom_path = {'M-M': [],
                            '1-M': []}

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
            if 'custom_path' in self.config['component'][component]:
                custom_path = self.config['component'][component]['custom_path']
            else:
                custom_path = self.custom_path

            oneToManyContRelations = [item for item in self.config['Relations'] if item[1] == '1-MC']
            for item in oneToManyContRelations:
                if KlassExpand(self.config,component,[rel[2][1]]) == KlassExpand(self.config,component,[item[2][1]]):
                    if (rel[2][0],item[0][0]) not in custom_path[rel[1]]:
                        custom_path[rel[1]].append((rel[2][0],item[0][0]))
            self.config['component'][component]['custom_path'] = custom_path
        
    def updateImports(self):
        for component in self.components:
            for i in self.imports:
                if 'imports' in self.config['component'][component]:
                    self.config['component'][component]['imports'].append(i) 
                else:
                    self.config['component'][component]['imports'] = [i]

    def updatePathImports(self):
        for component in self.components:
            if 'custom_path' in self.config['component'][component]:
                custom_path = self.config['component'][component]['custom_path']
            else:
                custom_path = self.custom_path

            if self.custom_path['M-M'] or self.custom_path['1-M']:
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
            self.config['component'][component]['relations'] = [] 
            component_classes = KlassExpand(self.config,component)
            
            for relation in self.config['Relations']:
                relationship = None
                classes = KlassExpand(self.config,component,[relation[0][1],relation[2][1]])
                if classes[0] in component_classes:
                    relationship =  "('%s', %s, %s, '%s'))," % \
                        (relation[2][0],self.relationMap(relation[1]),".".join(classes[0]),relation[0][0])
                if classes[1] in component_classes:
                    relationship =  "('%s', %s, %s, '%s'))," % \
                        (relation[2][0],self.relationMap(relation[1],rev=True),".".join(classes[0]),relation[0][0])
                if relationship:
                    self.config['component'][component]['relations'].append(relationship)
                    self.updateCustomPathReporter(relation,component)

    def run(self):
        self.updateRelations()
        self.updateImports()
        self.updateRelImports()
        self.updatePathImports()
        return self.config
