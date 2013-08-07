#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

data = {'id': 'ZenPacks.training.ExampleImpact',
        'organizers': [{"name": "Devices/Example",
                        "Type": "DeviceClass",
                        }],
        'deviceClasses': [{'path': 'Devices/Example',
                           'zPythonClass': 'ExampleDevice',
                           'componentTypes': [{'name': 'Enclosure',
                                               'impacts': ['TemperatureSensor'],
                                               'impactedBy': ['TemperatureSensorController']
                                               },
                                              {'name': 'TemperatureSensor'},
                                              {'name': 'TemperatureSensorController'},
                                              {'name': 'Cpu'}
                                              ],
                           'deviceType': {'name': 'ExampleDevice'}}],
        'relationships': [{"componentA": 'Enclosure', "componentB": 'TemperatureSensor', "Contained": False}]
        }

import json
print json.dumps(data, sort_keys=True, indent=1, separators=(',', ': '))
