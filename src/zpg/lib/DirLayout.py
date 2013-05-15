#!/usr/bin/env python
import logging
import os
logging.basicConfig()
log = logging.getLogger('DirLayout')

def initpy(source):
    return "/".join([source,'__init__.py'])

class DirLayout(object):
    def __init__(self, zenpack, destdir):
        self.base_destdir = destdir
        self.zenpack = zenpack

    @property
    def path(self):
        destDir = os.path.join(self.base_destdir, self.zenpack.id)
        return destDir

    def write(self):

        parts = self.zenpack.id.split('.')
        if not os.path.exists(self.path):
            os.makedirs(self.path, 0750)

        # Create subdirectories
        base = self.path
        for part in parts[:-1]:
            base = os.path.join(base, part)
            if not os.path.exists(base):
                os.mkdir(base)
            f = open(os.path.join(base, '__init__.py'), 'w')
            f.write("__import__('pkg_resources').declare_namespace(__name__)\n")
            f.close()
        base = os.path.join(base, parts[-1])
        if not os.path.exists(base):
            os.mkdir(base)

        # Write the manifest ( Not a template because I dont think we have ever modified this file)
        f = open(os.path.join(self.path, 'MANIFEST.in'), 'w')
        f.write("graft ZenPacks\n")
        f.close()
