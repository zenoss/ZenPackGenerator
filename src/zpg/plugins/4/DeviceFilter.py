#!/usr/bin/env python
import logging
import os
logging.basicConfig()
log = logging.getLogger('Device Filter')
from zpg.utils import KlassExpand

class DeviceFilter(object):
    type = 'filter'
    def __init__(self,config,opts):
        self.config = config
        self.opts = opts.dest

        if 'NEW_COMPONENT_TYPES' not in self.config:
            self.config['NEW_COMPONENT_TYPES'] = []

        if 'NEW_DEVICE_RELATIONS' not in self.config:
            self.config['NEW_DEVICE_RELATIONS'] = []

    def updateRelations(self):
        for relation in self.config['Relations']:
            if relation[1] == '1-MC':
                Klasses = KlassExpand(self.config,None,[relation[0][1],relation[2][1]])
                if Klasses[0] == ('Products.ZenModel', 'Device'):
                    self.config['NEW_COMPONENT_TYPES'].append("{0}.{1}.{1}".format(Klasses[1][0],Klasses[1][1]))
                    self.config['NEW_DEVICE_RELATIONS'].append("('{0}', '{1}', '{2}'),".format(relation[2][0],Klasses[1][1],relation[0][0]))
            
    def run(self):
        self.updateRelations()
        return self.config
