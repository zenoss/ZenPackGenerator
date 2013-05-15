#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################


class License(object):
    def __init__(self, id):
        self.id = id

    def header(self):
        return "#LICENSE HEADER SAMPLE"

    def __repr__(self):
        return self.id
