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

import inflect
import textwrap

from ._defaults import defaults
from .colors import error, warn, debug, info, green, red, OUTPUT_COLORS
from .ZenPack import ZenPack

__all__ = ['generate']


class ZpgOptionParser(ArgumentParser):

    """
    This Program builds zenpacks from templates.
    """

    def __init__(self):
        description = self.__class__.__doc__
        # description = textwrap.dedent(description)
        super(ZpgOptionParser, self).__init__(description=description)
        prefix = defaults.get("prefix", os.getcwd())
        self.add_argument("input", type=str, #FileType('rt'),
                          default=sys.stdin,
                          help="input file")
        self.add_argument("dest", type=str, nargs="?",
                          default=prefix,
                          help="Output folder for the zenpack. [%(default)s]")
        self.add_argument('-Z', "--zenpack-version",
                          dest="zenpack_version", default="4",
                          help="Zenpack type to build [%(default)s]")
        self.add_argument('-s', "--skip", action='store_true',
                          dest="skip", default=False,
                          help="Do Not use cached Templates.")
        self.add_argument("-C", "--no-color", action='store_false',
                          dest="color", default=True,
                          help="Remove color from standard output")
        self.add_argument("-q", "--quiet", action="count",
                          dest="quiet", default=0,
                          help="Decrease output verbosity")
        self.add_argument("-v", "--verbose", action="count",
                          dest="verbose", default=0,
                          help="Increaes output verbosity")


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
    logger = logging.getLogger('ZenPack Generator')

    # commandline parsing probably should happen somewhere else...
    #  keeping this here until a better spot opens up
    parser = ZpgOptionParser()
    (opts, args) = parser.parse_known_args()
    OUTPUT_COLORS = opts.color
    opts.verbose = 20 + opts.quiet * 10 - opts.verbose * 10
    opts.verbose = 1 if opts.verbose <= 0 else opts.verbose
    logger.setLevel(level=opts.verbose)

    if not filename or not os.path.exists(filename):
        print opts.input
        if not opts.input or not os.path.exists(str(opts.input)):
            err_msg = "Required input file missing.  exiting...\n"
            error(logger, err_msg)
            sys.exit(1)
        filename = opts.input

    if not os.path.exists(filename):
        err_msg = "Input file does not exist! %s" % filename
        error(logger, err_msg)
        sys.exit(1)

    info(logger, 'ZenPack Generator Starting')
    with open(filename, 'r') as f:
        debug(logger, 'Loading input file: %s...' % filename)
        jsi = json.load(f)
        jsi['opts'] = opts
        debug(logger, '  Loaded.')
        debug(logger, 'Populating ZenPack...')
        zp_json = ZenPack(**jsi)
        debug(logger, '  Done populating.')
        debug(logger, 'Writing output...')
        zp_json.write()
        debug(logger, '  Done writing.')

    debug(logger, 'Created ZenPack: %s' % green(zp_json.id))
    fpath = os.path.join(opts.dest, zp_json.id)
    info(logger, 'Files were placed into: %s' % green(fpath))
    info(logger, green('Generation Complete.'))

if __name__ == "__main__":
    generate(opts.json)
