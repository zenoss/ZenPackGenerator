#!/usr/bin/env python
import logging
import os
logging.basicConfig()
log = logging.getLogger('DirLayout')

def initpy(source):
    return "/".join([source,'__init__.py'])

class DirLayout(object):
    type = 'layout'
    def __init__(self,config,basedir):
        self.config = config
        self.basedir = basedir

    def run(self):
        destDir = os.path.join(self.basedir, self.config['NAME'])
        parts = self.config['NAME'].split('.')
        subdirs = "/".join(parts)
        workingDir = '/'.join([destDir,subdirs])
        if not os.path.exists(destDir):
            os.makedirs(destDir, 0750)

        # Create subdirectories
        base = destDir
        for part in parts[:-1]:
            base = os.path.join(base, part)
            if not os.path.exists(base):
                os.mkdir(base)
            f = open(os.path.join(base, '__init__.py'), 'w')
            f.write("__import__('pkg_resources').declare_namespace(__name__)\n")
            f.close()
        base = os.path.join(base, parts[-1])

        # Write the manifest ( Not a template because I dont think we have ever modified this file)
        f = open(os.path.join(destDir, 'MANIFEST.in'), 'w')
        f.write("graft ZenPacks\n")
        f.close()
