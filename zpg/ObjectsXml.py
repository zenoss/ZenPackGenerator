#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

import logging
import os

from lxml import etree
from .colors import error, warn, debug, info, green, red, yellow, disable_color

class ObjectsXml(object):

    """Build the objects xml file"""

    @property
    def log(self):
        """Logger for class using class name"""
        clsname = self.__class__.__name__
        return logging.getLogger(clsname)

    def __init__(self, zenpack):
        """Args:
                 zenpack: ZenPack class instance
        """
        self.zenpack = zenpack
        destpath = self.zenpack.destdir.path
        zenpath = '/'.join(self.zenpack.id.split('.'))
        xml_path = "%s/%s/objects/%s"
        self.objects_xml = xml_path % (destpath, zenpath, 'objects.xml')

    def to_objects_xml(self):
        root = etree.XML('<?xml version="1.0"?><objects></objects>')
        for organizer in self.zenpack.organizers.values():
            root.append(organizer.to_objects_xml())
        results = etree.tostring(root, xml_declaration=True,
                                 pretty_print=True)
        return results

    def write(self):
        """Write the object.xml file"""
        self.to_objects_xml()
        if os.path.exists(self.objects_xml):
            msgs = ['  objects.xml already exists.',
                    '         Remove the objects.xml if you wish to use the '
                    'generator to create a new one.']
            warn(self.log, yellow("\n".join(msgs)))
        else:
            self.log.info('Generating base objects.xml file.')
            with open(self.objects_xml, 'w') as obj_xml_file:
                obj_xml_file.write(self.to_objects_xml())
