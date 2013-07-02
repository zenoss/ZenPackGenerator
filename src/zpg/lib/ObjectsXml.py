#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################
from lxml import etree
import logging
import os

log = logging.getLogger('ObjectsXml')

class ObjectsXml(object):
    """Build the objects xml file"""

    def __init__(self,
                 zenpack
                 ):
        '''Args:
                 zenpack: ZenPack class instance
        '''
        self.zenpack = zenpack
        self.objects_xml = "%s/%s/objects/%s" % (zenpack.destdir.path, '/'.join(zenpack.id.split('.')), 'objects.xml')


    def to_objects_xml(self):
        root = etree.XML('<?xml version="1.0"?><objects></objects>')
        for organizer in self.zenpack.organizers.values():
	    root.append(organizer.to_objects_xml())
	
        results = etree.tostring(root,
                                 xml_declaration=True,
                                 pretty_print=True)
        return results

    def write(self):
        '''Write the object.xml file'''
        self.to_objects_xml()

        if os.path.exists(self.objects_xml):
            log.info('objects.xml already exists.  Skipping.')
            log.info('Remove the objects.xml if you wish to use the generator to create a new one.')
	else:
	    log.info('Generating base objects.xml file.')

            with open(self.objects_xml, 'w') as obj_xml_file:
                obj_xml_file.write(self.to_objects_xml())


        pass
