#!/usr/bin/env python
import logging
import os
logging.basicConfig()
log = logging.getLogger('Setup')
from zpg.Template import Template

class RootInit(Template):
    type = 'output'
    def __init__(self,config,basedir):
        super(RootInit, self).__init__(config,basedir)
        self.source_template = 'root_init.tmpl'
        self.dest_file = "%s/%s/%s/__init__.py" % (self.basedir, self.name, self.subdir)

    def run(self):
        self.write()
