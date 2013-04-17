#!/usr/bin/env python
import logging
import os
logging.basicConfig()
log = logging.getLogger('Ui')
from zpg.Template import Template

class Ui(Template):
    type = 'output'
    def __init__(self,config,basedir):
        super(Ui, self).__init__(config,basedir)
        ui_name = "_".join(self.name.split('.'))
        self.source_template = 'ui.tmpl'
        self.dest_file = "%s/%s/%s/resources/js/%s.js" % \
             (self.basedir, self.name, self.subdir, ui_name)

    def run(self):
        self.write()
