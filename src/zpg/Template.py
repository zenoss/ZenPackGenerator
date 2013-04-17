#!/usr/bin/env python
import os
import logging
logging.basicConfig()
log = logging.getLogger('Template')

from Cheetah.Template import Template as cTemplate
import inspect
import zpg
"/".join(inspect.getfile(zpg).split('/')[:-1])

class Template(object):
    def __init__(self,config,basedir):
        self.config = config
        self.basedir = basedir
        self.source_template = None
        self.dest_file = None
        self.searchList = []

    def run(self):
        pass

    def findTemplate(self):
        self.tfile = "%s/Templates/%s" % ("/".join(inspect.getfile(zpg).split('/')[:-1]),self.source_template)
       
    def buildSearch(self):
        self.searchList = self.config
 
    def write(self):
        self.findTemplate()
        self.buildSearch()
        t = cTemplate(file=self.tfile, searchList=self.searchList)
        f = open(os.path.join(self.dest_file), 'w')
        f.write(t.respond())
        f.close()

if __name__ == "__main__":
    #config = pydata.config
    cf = ComponentFactory(config)
    for component in cf.create():
        component.write()
    
