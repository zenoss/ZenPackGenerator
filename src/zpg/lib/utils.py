#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################
import re
import string

def prepId(id, subchar='_'):
    """
    Make an id with valid url characters. Subs [^a-zA-Z0-9-_,.$\(\) ]
    with subchar.  If id then starts with subchar it is removed.

    @param id: user-supplied id
    @type id: string
    @return: valid id
    @rtype: string
    """
    _prepId = re.compile(r'[^a-zA-Z0-9-_,.$\(\) ]').sub
    _cleanend = re.compile(r"%s+$" % subchar).sub
    if id is None:
        raise ValueError('Ids can not be None')
    if not isinstance(id, basestring):
        id = str(id)
    id = _prepId(subchar, id)
    while id.startswith(subchar):
        if len(id) > 1:
            id = id[1:]
        else:
            id = "-"
    id = _cleanend("", id)
    id = id.lstrip(string.whitespace + '_').rstrip()
    return str(id)

def KlassExpand(zenpack, value):
    """Expand a component
       eg:
          Component expands to ZenPack.example.Com.Component
    """

    if value.startswith(zenpack.namespace):
        return value
    elif '.' in value:
        return value
    else:
        return "%s.%s" % (zenpack.namespace, value)

def zpDir(zenpack):
    """ZenPack.zenoss.Foo returns ZenPack/zenoss/Foo"""
    parts = zenpack.id.split('.')
    subdirs = "/".join(parts)
    return subdirs

if __name__ == '__main__':
    from ZenPack import ZenPack
    print prepId('ZenPacks.zenoss.#@Foo').replace('.', '_')
    zp = ZenPack('a.b.c')
    print KlassExpand(zp, 'Component')
    print KlassExpand(zp, 'a.b.c.Component')
    print KlassExpand(zp, 'b.b.C')