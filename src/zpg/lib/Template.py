#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################

import os
import logging
logging.basicConfig()
log = logging.getLogger('Template')

from Cheetah.Template import Template as cTemplate
import inspect
import zpg


class Template(object):
    def __init__(self, zenpack):
        self.zenpack = zenpack
        self.source_template = 'foo.tmpl'
        self.base_destdir = zenpack.destdir.path
        self.dest_file = None

    def TemplateCacheLocation(self):
        return os.path.join(self.base_destdir, 'Templates', "%s.tmpl" % os.path.basename(self.dest_file))

    def cacheTemplate(self):
        cacheTemplateFile = self.TemplateCacheLocation()
        cache_directory = os.path.dirname(cacheTemplateFile)
        if not os.path.exists(cache_directory):
            os.makedirs(cache_directory)
        if not os.path.exists(cacheTemplateFile):
            tf = open(os.path.join(self.tfile), 'r')
            dtf = open(os.path.join(cacheTemplateFile), 'w')
            dtf.write('## Source Template %s \n' % self.tfile)
            dtf.write(tf.read())
            tf.close()
            dtf.close()

    def findTemplate(self):
        cacheTemplateFile = self.TemplateCacheLocation()
        if os.path.exists(cacheTemplateFile) and not self.zenpack.opts.skip:
            self.tfile = cacheTemplateFile
        else:
            self.tfile = "%s/Templates/%s" % ("/".join(inspect.getfile(zpg).split('/')[:-1]), self.source_template)
        log.info('Using template %s' % self.tfile)

    def processTemplate(self):
        self.findTemplate()
        self.cacheTemplate()
        t = cTemplate(file=self.tfile, searchList=[self])
        dfile = os.path.join(self.base_destdir, self.dest_file)

        dirname = os.path.dirname(dfile)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        f = open(dfile, 'w')
        f.write(t.respond())
        f.close()
