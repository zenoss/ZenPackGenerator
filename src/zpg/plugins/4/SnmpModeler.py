#!/usr/bin/env python
import logging
import os
logging.basicConfig()
log = logging.getLogger('Setup')
from zpg.Template import Template

class SnmpModeler(Template):
    type = 'output'
    def __init__(self,config,opts):
        super(SnmpModeler, self).__init__(config,opts)
        self.source_template = 'snmpmodelplugin.tmpl'
        self.basedir = "%s/%s/%s" % (opts.dest,config['NAME'],self.subdir)

        self.dest_file = "%s/modeler/plugins/training/snmp/NetBotz.py" % (self.basedir)
        self.create_inits = True

    def run(self):
        self.write()
