#!/usr/bin/env python
import logging
import os
logging.basicConfig()
log = logging.getLogger('Setup')
from zpg.Template import Template

class Setup(Template):
    type = 'output'
    def __init__(self,config,basedir):
        super(Setup, self).__init__(config,basedir)
        self.source_template = 'setup.tmpl'
        self.dest_file = "%s/%s/setup.py" % (basedir, config['NAME'])

    def buildSearch(self):
        packages = []
        parts = self.config['NAME'].split('.')
        for i in range(len(parts)):
            packages.append('.'.join(parts[:i+1]))
        self.config['PACKAGES'] = packages
        self.config['NAMESPACE_PACKAGES'] = packages[:-1]
        self.searchList = self.config

    def run(self):
        self.write()
