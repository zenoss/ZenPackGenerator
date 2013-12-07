#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

import inspect
import logging
import os

from Cheetah.Template import Template as cTemplate
from .colors import error, warn, debug, info, green, red, disable_color
import zpg


class Template(object):

    """Base Class for Template operations."""

    @property
    def log(self):
        cls_name = self.__class__.__name__
        return logging.getLogger(cls_name)

    def __init__(self, zenpack):
        self.zenpack = zenpack
        self.source_template = 'foo.tmpl'
        self.base_destdir = zenpack.destdir.path
        self.dest_file = None

    def TemplateCacheLocation(self):
        """return the cache location inside the zenpack directories."""
        fpath = "%s.tmpl" % os.path.basename(self.dest_file)
        return os.path.join(self.base_destdir, 'Templates', fpath)

    def cacheTemplate(self):
        """Store the template into the cache."""
        cacheTemplateFile = self.TemplateCacheLocation()
        cache_directory = os.path.dirname(cacheTemplateFile)
        if not self.zenpack.opts.skip:
            import pdb;pdb.set_trace()
            if not os.path.exists(cache_directory):
                os.makedirs(cache_directory)
            if not os.path.exists(cacheTemplateFile):
                with open(os.path.join(self.tfile), 'r') as tf:
                    with open(os.path.join(cacheTemplateFile), 'w') as dtf:
                        dtf.write('## Source Template %s \n' % self.tfile)
                        dtf.write(tf.read())

    def findTemplate(self):
        """Find the template and save its location."""
        cacheTemplateFile = self.TemplateCacheLocation()
        if os.path.exists(cacheTemplateFile) and not self.zenpack.opts.skip:
            self.tfile = str(cacheTemplateFile)
        else:
            sep = os.path.sep
            tpath = sep.join(inspect.getfile(zpg).split(sep)[:-1])
            self.tfile = "%s/Templates/%s" % (tpath, self.source_template)
        debug(self.log, '  Using template %s' % self.tfile)
        # print 'Using template %s' % self.tfile

    def processTemplate(self):
        """Write the templates."""
        self.findTemplate()
        self.cacheTemplate()
        with open(self.tfile, 'r') as tf:
            t = cTemplate(file=tf, searchList=[self])
        # print t.respond()
        dfile = os.path.join(self.base_destdir, self.dest_file)

        dirname = os.path.dirname(dfile)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(dfile, 'w') as f:
            f.write(t.respond())
