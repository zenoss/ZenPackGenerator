#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
#
import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase

import sys
import logging
from StringIO import StringIO
from Products.ZenModel.ZenPack import eliminateDuplicates

log = logging.getLogger("zen.ObjectsXmlExporter")


class ExportObjectsXml(ZenScriptBase):

    def buildOptions(self):
        ZenScriptBase.buildOptions(self)
        self.parser.add_option("-f", "--file", dest="filename",
                               help="write objects to FILE", metavar="FILE")
        self.parser.add_option("-z", "--zenpack", dest="zenpack",
                               help="ZenPack to Dump objects.xml From", metavar="ZenPack")

    def parseOptions(self):
        ZenScriptBase.parseOptions(self)
        if not self.options.filename:
            print "Required option output file is missing. Exiting..."
            sys.exit(1)

        if not self.options.zenpack:
            print "Required option source zenpack is missing. Exiting..."
            sys.exit(1)

    def run(self):
        if self.options.zenpack:
            self.zenpack = self.dmd.ZenPackManager.packs._getOb(
                self.options.zenpack, None)
            if not self.zenpack:
                print "%s is not a valid Zenpack. Exiting...." % self.options.zenpack
                sys.exit(1)

        xml = StringIO()

        # Write out packable objects
        # TODO: When the DTD gets created, add the reference here
        xml.write("""<?xml version="1.0"?>\n""")
        xml.write("<objects>\n")

        packables = eliminateDuplicates(self.zenpack.packables())
        for obj in packables:
            # obj = aq_base(obj)
            xml.write('<!-- %r -->\n' % (obj.getPrimaryPath(),))
            obj.exportXml(xml, ['devices', 'networks', 'pack'], True)
        xml.write("</objects>\n")
        objects = file(self.options.filename, 'w')
        objects.write(xml.getvalue())
        objects.close()

if __name__ == "__main__":
    eo = ExportObjectsXml(connect=True)
    eo.run()
