#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#


from Template import Template
from Component import Component
from Relationship import Relationship
from utils import zpDir
find = Relationship.find


class UtilsTemplate(Template):

    """ Write the template to a utils.py file
        eg.  Create ZenPacks.zenoss.Foo/ZenPacks/zenoss/Foo/utils.py """

    def __init__(self, zenpack):
        self.zenpack = zenpack
        super(UtilsTemplate, self).__init__(zenpack)
        self.source_template = 'utils.tmpl'
        self.dest_file = "%s/%s" % (zpDir(zenpack), 'utils.py')

    def write(self):
        """Write utils.py"""
        self.processTemplate()
