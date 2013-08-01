#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#
from ._defaults import Defaults, user_zpg_license_dir
from .colors import error, warn, debug, info, green, red, yellow, disable_color
import logging
import os
import shutil

log = logging.getLogger('License')
defaults = Defaults()


def find_subdir(path):
    if os.path.exists(path):
        return [name for name in os.listdir(path)
                if os.path.isdir(os.path.join(path, name))]
    else:
        return []


def load_header(path, id_):

    license_dir = os.path.join(path, id_)
    header_file = os.path.join(license_dir, 'header.txt')
    header = ""
    if os.path.isfile(header_file):
        with open(header_file, 'r') as hf:
            header = hf.read()

    if header == "":
        debug(log,
              yellow("License header failed to load, using blank header."))

    return header


def load_license(path, id_):
    license_dir = os.path.join(path, id_)
    license_file = os.path.join(license_dir, 'LICENSE.txt')
    license = ""
    if os.path.isfile(license_file):
        with open(license_file, 'r') as lf:
            license = lf.read()
    else:
        debug(log, yellow("LICENSE.txt failed to load. Skipping.."))

    return license


class License(object):

    """
    Each ZenPack may be licensed individually.  Generally, the two formats are
    either GPLv2+ or Commercial.
    """

    def __init__(self, zenpack, id_):
        self.zenpack = zenpack
        user_licenses = []
        dflt_licenses = []

        if os.path.isdir(user_zpg_license_dir):
                debug(log, 'Found user license folder.')
                user_licenses = find_subdir(user_zpg_license_dir)
                if user_licenses:
                    debug(log, '  Loaded User Licenses.')

        if os.path.exists('Licenses') and os.path.isdir('Licenses'):
            dflt_licenses = find_subdir('Licenses')

        if id_ in user_licenses:
            self.id = id_
            self.header = load_header(user_zpg_license_dir, self.id)
            self.license = load_license(user_zpg_license_dir, self.id)

        elif id_ in dflt_licenses:
            self.id = id_
            self.header = load_header('Licenses', self.id)
            self.license = load_license('Licenses', self.id)
        else:
            # Default GPlv2
            info(log,
                 red('Specified License [%s] not known. Defaulting to GPLv2.'
                     % id_))
            self.id = 'GPLv2'
            self.header = load_header('Licenses', self.id)
            self.license = load_license('Licenses', self.id)

    def header(self):
        return self.header

    def write(self):
        """
        Write the License file into the ZenPack.
        """
        self.dest_file = "%s/%s" % (self.zenpack.destdir.path, 'LICENSE.txt')
        if self.license:
            with open(self.dest_file, 'w') as dlf:
                debug(log, '  Writing LICENSE.txt')
                dlf.write(self.license)

    def __repr__(self):
        return self.id
