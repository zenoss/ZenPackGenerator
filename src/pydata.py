#!/usr/bin/env python
import json
from collections import defaultdict

try:
    from yaml import dump
except:
    print "Yaml not found, try running easy_install PyYaml"
    sys.exit(1)

config = defaultdict(dict)
'''Setup.py'''
config['NAME']="ZenPacks.training.NetBotz"
config['VERSION']="1.0.0"
config['AUTHOR']="ZenossLabs <labs@zenoss.com>"
config['LICENSE']="All Rights Reserved"
config['INSTALL_REQUIRES']= []
config['COMPAT_ZENOSS_VERS']= ">=4.2"
config['PREV_ZENPACK_NAME']= ""
'''End Setup.py'''

config['zproperties'] = {'NetBotz':[('zNetBotzProperty', False, 'boolean')]}
'''
config['Relations'] = [
                      [('sensor_device', 'NetBotzDevice'), '1-MC', ('enclosures', 'Enclosure') ],
                      [('enclosure', 'Enclosure'), '1-MC', ('temperature_sensors', 'TemperatureSensor') ],
                      ]
'''
config['Relations'] = [
                      [('sensor_device', 'Device'), '1-MC', ('enclosures', 'Enclosure') ],
                      [('enclosure', 'Enclosure'), '1-MC', ('temperature_sensors', 'TemperatureSensor') ],
                      ]

config['ZPROPERTY_CATEGORY'] = 'NetBotz'
config['ZPROPERTIES'] = [
                         "('zNetBotzExampleProperty', 300, 'int'),",
                         "('zNetBotzExampleProperty2', '', 'string'),",
                         "('zNetBotzExampleProperty3', True, 'boolean'),",
                         "('zNetBotzExampleProperty4', '', 'password'),",
                        ]

# components (Enclosure)
config['component'].setdefault('Enclosure', {})
config['component']['Enclosure']['name'] = 'NetBotz Enclosure'
config['component']['Enclosure']['names'] = 'NetBotz Enclosures'
config['component']['Enclosure']['class'] = 'Component'
config['component']['Enclosure']['unique_name'] = 'NetBotzEnclosure'
#config['component']['Enclosure']['imports'] = ''
config['component']['Enclosure']['PanelSort'] = [ 'name', 'ASC' ]
config['component']['Enclosure']['attributes'] = [
                                                  {'Name': 'Enclosure Status', 
                                                  'Names': 'Enclosure Status', 
                                                  'default': None,
                                                  'DetailDisplay': True,
                                                  'PanelDisplay': True,
                                                  'PanelWidth': 30,
                                                  'PanelSortable': True,
                                                  'type': 'string',
                                                  'id': 'enclosure_status'},
                                                  {'Name': 'Error Status', 
                                                  'Names': 'Error Status', 
                                                  'default': None,
                                                  'DetailDisplay': True,
                                                  'PanelDisplay': True,
                                                  'PanelWidth': 30,
                                                  'PanelSortable': True,
                                                  'type': 'string',
                                                  'id': 'error_status'},
                                                  {'Name': 'Parent Id', 
                                                  'Names': 'Parent Ids', 
                                                  'default': None,
                                                  'DetailDisplay': True,
                                                  'PanelDisplay': True,
                                                  'PanelWidth': 30,
                                                  'PanelSortable': True,
                                                  'type': 'string',
                                                  'id': 'parent_id'},
                                                  {'Name': 'Docked Id', 
                                                  'Names': 'Docked Ids', 
                                                  'default': None,
                                                  'DetailDisplay': True,
                                                  'PanelDisplay': True,
                                                  'PanelWidth': 30,
                                                  'PanelSortable': True,
                                                  'type': 'string',
                                                  'id': 'docked_id'},
                                                  ]

# components (Temperature Sensor)
config['component'].setdefault('TemperatureSensor', {})
config['component']['TemperatureSensor']['name'] = 'Temperature Sensor'
config['component']['TemperatureSensor']['names'] = 'Temperature Sensor'
config['component']['TemperatureSensor']['class'] = 'Component'
config['component']['TemperatureSensor']['unique_name'] = 'NetBotzTemperatureSensor'
config['component']['TemperatureSensor']['attributes'] = [
                                                          {'Name': 'Port',
                                                           'Names': 'Ports', 
                                                           'default': None,
                                                           'DetailDisplay': True,
                                                           'PanelDisplay': True,
                                                           'PanelWidth': 30,
                                                           'PanelSortable': False,
                                                           'type': 'string',
                                                           'id': 'port'},
                                                         ]

# components (Device)
config['component'].setdefault('NetBotzDevice', {})
config['component']['NetBotzDevice']['name'] = 'NetBotz Device'
config['component']['NetBotzDevice']['names'] = 'NetBotz Device'
config['component']['NetBotzDevice']['Device'] = True
config['component']['NetBotzDevice']['class'] = 'Device'
config['component']['NetBotzDevice']['unique_name'] = 'NetBotzDevice'
#config['component']['NetBotzDevice']['imports'] = ''
config['component']['NetBotzDevice']['attributes'] = [
                                                          {'Name': 'Number of Temperature Sensors', 
                                                           'Names': 'Number of Temperature Sensors', 
                                                           'default': None,
                                                           'DetailDisplay': True,
                                                           'PanelDisplay': True,
                                                           'PanelWidth': 30,
                                                           'PanelSortable': False,
                                                           'type': 'int',
                                                           'id': 'temp_sensor_count'},
                                                         ]
