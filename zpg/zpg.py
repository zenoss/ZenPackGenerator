#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#


import os
import sys
import json
import logging

from options import ZpgOptionParser
from ZenPack import ZenPack

logging.basicConfig()
log = logging.getLogger('ZenPack Generator')
log.setLevel(level=logging.INFO)

__all__  = ['main']

def main():
    log.info('ZenPack Generator Starting')
    parser = ZpgOptionParser()
    (opts, args) = parser.parse_args()

    if not opts.json:
        log.info("Required json input file missing.  exiting...")
        sys.exit(1)

    if opts.debug:
        log.setLevel(level=logging.DEBUG)
        log.debug('Turned on Debug Output')

    f = open(opts.json, 'r')
    jsi = json.load(f)
    jsi['opts'] = opts
    zp_json = ZenPack(**jsi)
    zp_json.write()

if __name__ == "__main__":
    main()
