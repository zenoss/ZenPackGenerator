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
    def __init__(self,config,opts):

        self.config = config
        self.basedir = opts.dest
        self.opts = opts
        self.name = config['NAME']
        self.source_template = None
        self.dest_file = None
        self.dest_tfile = None
        self.searchList = []
        self.subdir = "/".join(self.config['NAME'].split('.'))
        self.create_inits = False

    def run(self):
        pass

    def findTemplate(self):
        if not self.opts.skip:
            basedir=self.dest_file.split(self.config['NAME'])[0]+'/%s/Templates' % self.config['NAME']
            self.tfile=basedir+self.dest_file.split(self.config['NAME'])[1]+'.tmpl'
            self.dest_tfile=self.tfile
            if not os.path.exists(self.tfile):
                self.tfile = "%s/Templates/%s" % ("/".join(inspect.getfile(zpg).split('/')[:-1]),self.source_template)
        else:
            self.tfile = "%s/Templates/%s" % ("/".join(inspect.getfile(zpg).split('/')[:-1]),self.source_template)
        log.info('Using template %s' % self.tfile)
       
    def buildSearch(self):
        self.searchList = self.config

    def write_tfile(self): 
        dirpart = os.path.dirname(self.dest_tfile)
        if not os.path.exists(dirpart):
            os.makedirs(dirpart)
        if not os.path.exists(self.dest_tfile):
            tf = open(os.path.join(self.tfile), 'r')
            dtf = open(os.path.join(self.dest_tfile), 'w')
            dtf.write('## Source Template %s \n' % self.tfile)
            dtf.write(tf.read())
            tf.close()
            dtf.close()

    def write(self):
        self.findTemplate()
        self.buildSearch()
        dirpart = os.path.dirname(self.dest_file)
        if not os.path.exists(dirpart):
            os.makedirs(dirpart)

        t = cTemplate(file=self.tfile, searchList=self.searchList)
        f = open(os.path.join(self.dest_file), 'w')
        f.write(t.respond())
        f.close()
        if not self.opts.skip:
            self.write_tfile()

if __name__ == "__main__":
    #config = pydata.config
    cf = ComponentFactory(config)
    for component in cf.create():
        component.write()
    
