#!/usr/bin/env python
from Cheetah.Template import Template
import pydata
import pprint

if __name__ == "__main__":
   
    config = pydata.config 
    for key in config['component'].keys():
        #t = Template(file="../../templates/4/component.tmpl", searchList=component)
        component = config['component'][key]
        imports = ['from zope.interface import implements',
                   'from Products.ZenModel.DeviceComponent import DeviceComponent',
                   'from Products.ZenModel.ManagedEntity import ManagedEntity',
                   'from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE',
                   'from Products.ZenRelations.RelSchema import ToManyCont, ToOne',
                   'from Products.Zuul.form import schema',
                   'from Products.Zuul.infos import ProxyProperty',
                   'from Products.Zuul.infos.component import ComponentInfo',
                   'from Products.Zuul.interfaces.component import IComponentInfo',
                   'from Products.Zuul.utils import ZuulMessageFactory as _t',
                  ]
        component['imports'] = imports
        component['componentclasses'] = 'foo, bar'
        t = Template(file="component.tmpl", searchList=[component,{'title':key}])
        print t.respond() 
