#!/usr/bin/env zendmd
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""
Build zenpack based on a YAML input file.
"""

try:
    import yaml
    import yaml.constructor
except:
    print "Yaml not found, try running easy_install PyYaml"
    sys.exit(1)

import re
import sys
import types

# http://jira.zenoss.com/jira/browse/ZEN-5017
from Products.Zuul import info as ZuulInfo

from Products.Zuul.facades import ObjectNotFoundException

try:
    # included in standard lib from Python 2.7
    from collections import OrderedDict
except ImportError:
    # try importing the backported drop-in replacement
    # it's available on PyPI
    from ordereddict import OrderedDict

class OrderedDictYAMLLoader(yaml.Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """

    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                'expected a mapping node, but found %s' % node.id, node.start_mark)

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError, exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping',
                    node.start_mark, 'found unacceptable key (%s)' % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping


def main():
    # sys.argv[0] is zendmd. Pop it so the script can use normal conventions.
    sys.argv.pop(0)
    if len(sys.argv) < 2:
        data = yaml.load(sys.stdin.read(), OrderedDictYAMLLoader)
    else:
        with open(sys.argv[1], 'r') as yaml_file:
            data = yaml.load(yaml_file, OrderedDictYAMLLoader)
    if data:
        import pdb;pdb.set_trace()

        # commit comes from the zendmd interpreter.
        print "Yaml files loaded successfully."
        commit()
    else:
        print "No Yaml found... exiting..."
        sys.exit(0)


def die(msg, *args):
    print >> sys.stderr, msg % args
    sys.exit(1)

if __name__ == '__main__':
    main()
