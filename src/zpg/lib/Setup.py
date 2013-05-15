##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################


from Template import Template


class Setup(Template):
    def __init__(self, zenpack):
        super(Setup, self).__init__(zenpack)
        self.source_template = 'setup.tmpl'
        self.dest_file = "setup.py"

    def write(self):
        self.processTemplate()
