#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

data = {'id': 'ZenPacks.training.ExampleOrganizer',
        'organizers': [{"name": "Devices/Example",
                        "Type": "DeviceClass",
                        "properties": [{ "name": "zPingMonitorIgnore",
                                         "type": "boolean",
                                         "value": "True"
                                        }, {
                                          "name": "zDeviceTemplates",
                                          "type": "lines",
                                          "value": [ "example.Template" ]
                                        }]
                        }],
        'deviceClasses': [{'path': 'Devices/Example',
                           'zPythonClass': 'ExampleOrganizer',
                           'deviceType': {'name': 'ExampleDevice'}}],
        }

import json
print json.dumps(data, sort_keys=True, indent=1, separators=(',', ': '))
