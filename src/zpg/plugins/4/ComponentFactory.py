#!/usr/bin/env python
import pydata
import Attribute
import logging
logging.basicConfig()
log = logging.getLogger('Component')
from Cheetah.Template import Template

class ComponentFactory(object):
    def __init__(self,config):
        self.config = config
        self.zp_name = config['NAME']

    def create(self):
        self.components = []
        for component in self.config['component'].keys():
            self.components.append(Component(component,
                                             self.config))

        return self.components


class Component(object):
    def __init__(self,id,config):
        self.id = id
        self.config = config
        self.imports = [
                        'from zope.component import adapts',
                        'from zope.component import implements',
                        'from Products.Zuul.decorators import info',
                        'from Products.Zuul.form import schema',
                        'from Products.Zuul.infos import ProxyProperty',
                        'from Products.Zuul.utils import ZuulMessageFactory as _t',
                       ]
        self.one = False
        self.many = False
        self.manycont = False
        self.parent = None
        self.custom_path = {'M-M': [],
                            '1-M': []}


    def relations_imports(self):
        self.relations()
        rel = []
        if self.one:
            rel.append('ToOne')
        if self.many:
            rel.append('ToMany')
        if self.manycont:
            rel.append('ToManyCont')
     
        if rel:
            self.imports.append("from Products.ZenRelations.RelSchema import %s" % ", ".join(sorted(set(rel))))


    def relations(self):
        self.config['component'][self.id]['relations'] = []
        component_classes = self.KlassExpand()
        for relation in self.config['Relations']:
            classes = self.KlassExpand([relation[0][1],relation[2][1]])
            if classes[0] in [(config['NAME'],self.id)]:
                if relation[1] == '1-MC':
                   rel = 'ToOne(ToManyCont'
                   self.one = True
                   self.manycont = True
                if relation[1] == 'M-M':
                   rel = 'ToMany(ToMany'
                   self.many = True
                   # custom_path_reporters
                   for item in [item for item in self.config['Relations'] if item[1] == '1-MC']:
                       if self.KlassExpand([relation[2][1]]) == self.KlassExpand([item[2][1]]):
                           if (relation[2][0],item[0][0]) not in self.custom_path['M-M']:
                               self.custom_path['M-M'].append((relation[2][0],item[0][0]))
  
                if relation[1] == '1-M':
                   rel = 'ToOne(ToMany'
                   self.many = True
                   self.one = True

                   # custom_path_reporters
                   for item in [item for item in self.config['Relations'] if item[1] == '1-MC']:
                       if self.KlassExpand([relation[2][1]]) == self.KlassExpand([item[2][1]]):
                           if (relation[2][0],item[0][0]) not in self.custom_path['1-M']:
                               self.custom_path['1-M'].append((relation[2][0],item[0][0]))

                if relation[1] == '1-1':
                   rel = 'ToOne(ToOne'
                   self.one = True
                relationship =  "('%s', %s, %s, '%s'))," % \
                                        (relation[2][0],rel,".".join(classes[0]),relation[0][0])
                self.config['component'][self.id]['relations'].append(relationship)

            if classes[1] in [(config['NAME'],self.id)]:
                if relation[1] == '1-MC':
                   rel = 'ToManyCont(ToOne'
                   self.one = True
                   self.manycont = True
                   parent = relation[0][0]
                if relation[1] == 'M-M':
                   rel = 'ToMany(ToMany'
                   self.many = True
                if relation[1] == '1-M':
                   rel = 'ToMany(ToOne'
                   self.many = True
                   self.one = True
                if relation[1] == '1-1':
                   rel = 'ToOne(ToOne'
                   self.one = True
                relationship =  "('%s', %s, %s, '%s'))," % \
                                        (relation[0][0],rel,".".join(classes[0]),relation[2][0])
                if not self.parent:
                    self.config['component'][self.id]['relations'].append(relationship)
                else:
                    log.warn("not adding relationship %s to %s" % (relationship,self.id))

                if parent and not self.parent:
                    self.parent = parent
               

    def KlassExpand(self, klasses=None):
        classes = []
        if klasses == None:
             component = self.config['component'][self.id] 
             klasses = component['class']
        for klass in klasses:
            split = klass.split('.')
            if klass.lower() == 'component':
                classes.append(('Products.ZenModel.DeviceComponent','DeviceComponent'))
                classes.append(('Products.ZenModel.ManagedEntity', 'ManagedEntity'))

            elif klass in config['component'].keys():
                classes.append((config['NAME'], klass))

            elif len(split) == 1:
                classes.append(('Products.ZenModel', klass))

            elif len(split) > 0:
                classes.append((".".join(split[0:-1]), split[-1]))
        return classes

    def process(self):
        self.relations_imports()
        self.config['component'][self.id]['imports'] = self.imports

        if self.parent:
            self.config['component'][self.id]['parent'] = self.parent
        else:
            self.config['component'][self.id]['parent'] = None

        self.config['component'][self.id]['custom_path'] = self.custom_path
        if self.custom_path['M-M'] or self.custom_path['1-M']:
            self.imports.append("from Products.Zuul.catalog.paths import DefaultPathReporter, relPath")

    def write(self):
        self.process()
        t = Template(file="component.tmpl", searchList=[self.config['component'][self.id],{'title':self.id}])
        print t.respond()

if __name__ == "__main__":

    config = pydata.config
    cf = ComponentFactory(config)
    for component in cf.create():
        component.write()
    
