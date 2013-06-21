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
logging.basicConfig()
log = logging.getLogger('DirLayout')


def initpy(source):
    return "/".join([source, '__init__.py'])


class DirLayout(object):

    '''Write the ZenPack directory structure.'''

    def __init__(self, zenpack, prefix):
        '''Args:
                 zenpack: a ZenPack Class instance.
                 prefix: The destination prefix.
        '''
        self.prefix = prefix
        self.zenpack = zenpack

    @property
    def path(self):
        '''Join the prefix and the zenpack id to create the destination path.'''

        destDir = os.path.join(self.prefix, self.zenpack.id)
        return destDir

    def write(self):
        '''Create the directories'''
        parts = self.zenpack.id.split('.')

        if not os.path.exists(self.path):
            os.makedirs(self.path, 0750)

        # Create subdirectories
        base = self.path
        for part in parts:
            base = os.path.join(base, part)
            if not os.path.exists(base):
                os.mkdir(base)

            '''Write nested __init__.py files.'''
            df = os.path.join(base, '__init__.py')
            f = open(df, 'w')
            f.write(
                "__import__('pkg_resources').declare_namespace(__name__)\n")
            f.close()

        # Write the manifest ( Not a template because I dont think we have ever
        # modified this file)
        f = open(os.path.join(self.path, 'MANIFEST.in'), 'w')
        f.write("graft ZenPacks\n")
        f.close()
