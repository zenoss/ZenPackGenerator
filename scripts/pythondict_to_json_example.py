#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

data = {'id': 'ZenPacks.training.NetBotz',
        'organizers': [{"name": "Devices/Server/Dell/Blade",
                        "Type": "DeviceClass",
                        "properties": [{"name": "zPingMonitorIgnore", "Type": "boolean", "value": "True"},
                                       {"name": "zDeviceTemplates",
                                        "Type": "lines",
                                        "value": ['example.Template']}]
                        }],
        'zProperties': [{'name': 'zNetBotzExample', 'Type': 'boolean', 'default': True, 'group': 'NetBotz'},
                        {'name': 'e1'}
                        ],
        'deviceClasses': [{'path': 'Device/Snmp',
                           'zPythonClass': 'NetBotzDevice',
                           'componentTypes': [{'name': 'Enclosure',
                                               'properties': [{'name': 'enclosure_status'},
                                                              {'name':
                                                                  'error_status'},
                                                              {'name':
                                                                  'parent_id'},
                                                              {'name': 'docked_id'}]},
                                              {'name': 'TemperatureSensor',
                                               'properties': [{'name': 'port'}]},
                                              ],
                           'deviceType': {'name': 'NetBotzDevice',
                                          'properties': [{'name': 'temp_sensor_count',
                                                          'Type': 'int'}]}
                           }],
        'relationships': [{"ComponentA": 'A', "ComponentB": 'B', "Contained": False}]
        }

import json
print json.dumps(data, sort_keys=True, indent=1, separators=(',', ': '))
