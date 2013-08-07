#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

data = {'id': 'ZenPacks.training.ExampleNestedComponent',
        'organizers': [{"name": "Devices/Example",
                        "Type": "DeviceClass",
                        }],
        'deviceClasses': [{'path': 'Devices/Example',
                           'zPythonClass': 'ExampleNestedComponent',
                           'componentTypes': [{'name': 'Enclosure',
                                               'componentTypes': [{'name': 'Shelf',
                                                                   'componentTypes': [{'name': 'Disk'}]
                                                                   }]
                                              }],
                           'deviceType': {'name': 'ExampleNestedDevice'}}],
        }

import json
print json.dumps(data, sort_keys=True, indent=1, separators=(',', ': '))
