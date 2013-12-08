# -*- coding: utf-8 -*-

"""
zpg.api
~~~~~~~

This module implements zpg's API.

:copyright: (c) 2013 Zenoss, Inc. 2013, all rights reserved.
:license: This content is made available according to terms specified in the
LICENSE file at the top-level directory of this package.

"""

from argparse import ArgumentParser, FileType
import json
import logging
import os
import sys
import re

import inflect

from .colors import error, warn, debug, info, green, red, disable_color
from .ZenPack import ZenPack

__all__ = ['generate']

from ._defaults import Defaults
defaults = Defaults()

logger = logging.getLogger('ZenPack Generator')


class ZpgOptionParser(ArgumentParser):

    """
    This Program builds zenpacks from templates.
    """

    def __init__(self):
        description = self.__class__.__doc__
        super(ZpgOptionParser, self).__init__(description=description)
        prefix = defaults.get("prefix", os.getcwd())
        group1 = self.add_argument_group('standard arguments')
        group2 = self.add_argument_group('special arguments')
        group1.add_argument("input", type=str,  # FileType('rt'),
                            default='', nargs="?",
                            help="input file")
        group1.add_argument("dest", type=str, nargs="?",
                            default=prefix,
                            help="Output dest for the zenpack. [%(default)s]")
        group1.add_argument('-Z', "--zenoss_version",
                            dest="zenoss_version", default="4",
                            help="Zenoss version compatability [%(default)s]")
        group1.add_argument('-s', "--skip", action='store_true',
                            dest="skip", default=False,
                            help="Do not use cached Templates.")
        group1.add_argument('-ng', "--no-git", action='store_false',
                            dest="git", default=True,
                            help="Do not great/update git repo.")
        group1.add_argument("-C", "--no-color", action='store_false',
                            dest="color", default=True,
                            help="Remove color from standard output")
        group1.add_argument("-q", "--quiet", action="count",
                            dest="quiet", default=0,
                            help="Decrease output verbosity")
        group1.add_argument("-v", "--verbose", action="count",
                            dest="verbose", default=0,
                            help="Increase output verbosity")
        group1.add_argument("-c", "--clean", action="store_true",
                            dest="clean", default=False,
                            help="Cleans destination path before generating")
        group2.add_argument('-V', "--version", action="store_true",
                            dest="version", default=False,
                            help="Display version of %(prog)s")


def replacer(match):
    new_string = matched = match.group(0)
    if matched.startswith('/') or matched.startswith("#"):
        new_string = ''
    return new_string


def remove_comments(text):
    """Removes the comments from a JSON, YAML or Python file
    """
    pattern = r'#.*?$|//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"'
    flags = re.DOTALL | re.MULTILINE
    engine = re.compile(pattern, flags)
    lines = re.sub(engine, replacer, text).split("\n")
    return "\n".join(line for line in lines if line.strip())


def remove_folder(fpath):
    removed = []
    if os.path.exists(fpath):
        for root, folders, files in os.walk(fpath, topdown=False):
            for file in files:
                filepath = os.path.join(root, file)
                os.remove(filepath)
                removed.append(filepath)
            for folder in folders:
                folderpath = os.path.join(root, folder)
                if os.path.exists(folderpath):
                    os.removedirs(folderpath)
                    removed.append(folderpath)


class TemplateJSONDecoder(json.JSONDecoder):
    def decode(self, json_string):
        """
        json_string is basically string that you give to json.loads method
        """
        json_string = remove_comments(json_string)
        default_obj = super(TemplateJSONDecoder, self).decode(json_string)
        return default_obj


def determine_file_type(filename):
    filetype = None
    if filename.endswith('.json'):
        filetype = 'json'
    elif filename.endswith('.yaml'):
        filetype = 'yaml'
    elif filename.endswith('.xml'):
        filetype = 'xml'
    return filetype


def generate(filename=None):
    """Constructs a ZenPack based upon an input file.

    Usage::

        >>> import zpg
        >>> zpg.generate(filename='/path/to/json_file.json')
        ...

    Note::

        This function will parse the commandline if the filename
        is not included.

        Currently only parses JSON files.
    """

    # commandline parsing probably should happen somewhere else...
    #  keeping this here until a better spot opens up
    parser = ZpgOptionParser()
    (opts, args) = parser.parse_known_args()
    opts.dest = os.path.abspath(opts.dest)
    if not opts.color:
        disable_color()
    opts.verbose = 20 + opts.quiet * 10 - opts.verbose * 10
    opts.verbose = 1 if opts.verbose <= 0 else opts.verbose

    # Reset the root logger logging level based on options
    root_logger = logging.getLogger()
    root_logger.setLevel(level=opts.verbose)

    if opts.version:
        msg = "%s Version: %s" % ('ZenPackGenerator', defaults.get('version'))
        info(logger, msg)
        sys.exit(0)

    if not filename or not os.path.exists(filename):
        filename = opts.input
        # Make sure filename is an expanded, absolute path
        if filename.startswith('~'):
            filename = os.path.expanduser(filename)
        elif filename.startswith('.'):
            filename = os.path.abspath(filename)
        if not filename or not os.path.exists(filename):
            err_msg = "Required input file missing.  Exiting...\n"
            error(logger, err_msg)
            sys.exit(1)

    if not os.path.exists(filename):
        err_msg = "Input file does not exist! %s" % filename
        error(logger, err_msg)
        sys.exit(1)

    filetype = determine_file_type(filename)
    if filetype is None:
        err_msg = "Could not determine file type: %s" % filename
        error(logger, err_msg)
        sys.exit(1)

    info(logger, 'ZenPack Generator Starting')
    with open(filename, 'r') as f:
        debug(logger, 'Loading input file: %s...' % filename)
        if filetype == 'json':
            try:
                jsi = json.load(f, cls=TemplateJSONDecoder)
                jsi['opts'] = opts
            except Exception as e:
                warn(logger, 'Failed to parse input json.')
                warn(logger, e.message)
                warn(logger, 'Common problems include: ')
                warn(logger, '\t 1. Using single ticks (rather than quotes)')
                warn(logger, '\t 2. An extra comma after the last item of a series of entries.')
                sys.exit(1)
               
        else:
            err_msg = "File Type not supported: %s" % filename
            error(logger, err_msg)
            sys.exit(1)
        debug(logger, '  Loaded.')
        debug(logger, 'Populating ZenPack...')
        zp_json = ZenPack(**jsi)
        fpath = os.path.join(opts.dest, zp_json.id)
        debug(logger, 'Done ZenPack populating.')
        debug(logger, 'Writing output...')
        if opts.clean:
            info(logger, 'Cleaning: %s' % fpath)
            remove_folder(fpath)
        zp_json.write()
        debug(logger, 'Done writing.')

    debug(logger, 'Created ZenPack: %s' % green(zp_json.id))
    fpath = os.path.join(opts.dest, zp_json.id)
    info(logger, 'Files were placed into: %s' % green(fpath))
    info(logger, green('Generation Complete.'))

if __name__ == "__main__":
    generate(opts.json)
