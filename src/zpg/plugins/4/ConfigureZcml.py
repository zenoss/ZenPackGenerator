#!/usr/bin/env python
import logging
import os
logging.basicConfig()
log = logging.getLogger('Configure Zcml')
from zpg.Template import Template

class ConfigureZcml(Template):
    type = 'output'
    def __init__(self,config,opts):
        super(ConfigureZcml, self).__init__(config,opts)
        self.source_template = 'configure.zcml.tmpl'
        self.dest_file = "%s/%s/%s/configure.zcml" % \
             (self.basedir, self.name, self.subdir)

    def run(self):
        self.write()
