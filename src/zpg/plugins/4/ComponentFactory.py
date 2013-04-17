#!/usr/bin/env python
import logging
import os
logging.basicConfig()
log = logging.getLogger('Setup')
from zpg.Template import Template
from zpg.utils import KlassExpand

class ComponentFactory(object):
    type = 'output'
   
    def __init__(self,config,basedir):
        self.config = config
        self.basedir = basedir
 
    def run(self):
        self.components = []
        for component in self.config['component'].keys():
            obj = Component(self.config,self.basedir,component)
            obj.run()

class Component(Template):
    type = 'output'
    def __init__(self,config,basedir,component):
        super(Component, self).__init__(config,basedir)
        self.id = component
        self.source_template = 'component.tmpl'
        self.dest_file = "%s/%s/%s/%s.py" % (self.basedir, self.name, self.subdir, component)
        self.imports = [
                        'from zope.component import adapts',
                        'from zope.component import implements',
                        'from Products.Zuul.decorators import info',
                        'from Products.Zuul.form import schema',
                        'from Products.Zuul.infos import ProxyProperty',
                        'from Products.Zuul.utils import ZuulMessageFactory as _t',
                       ]

    def buildSearch(self):
         self.searchList=[self.config['component'][self.id],{'title':self.id}]

    def run(self):
        self.write()
