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
config['NAME']="ZenPacks.zenoss.Foo"
config['VERSION']="1.0"
config['AUTHOR']="ZenossLabs <labs@zenoss.com>"
config['LICENSE']="gpl"
config['INSTALL_REQUIRES']= ["ZenPacks.zenoss.PyCollector <=1.0.1",
                                   "ZenPacks.zenoss.PyWBEM",
                                   "ZenPacks.zenoss.StorageBase"]

config['COMPAT_ZENOSS_VERS']= ">=4.1.70"
config['PREV_ZENPACK_NAME']= ""
# packages and name_spaces are calculated on the name
'''End Setup.py'''

config['answers']['readme'] = True

# components (Array)
config['component'].setdefault('Array', {})
config['component']['Array']['name'] = 'Array'
config['component']['Array']['names'] = 'Arrays'
config['component']['Array']['class'] = ['Component']   #Aka import the things for them if using this
config['component']['Array']['class'] = ['TemperatureSensor']   #assume its under Products.ZenModel  with TS.TS
config['component']['Array']['class'] = ['ZenPacks.zenoss.Foo.Foo']  #== set the imports and then replace with just Foo 
config['component']['Array']['class'] = ['Battery'] #if Battery then if we find this in the component config set the imports to import that file.
config['component']['Array']['class'] = ['Component'] 

# Assume we dont need to this but provide if needed.
config['component']['Array']['imports'] = ['import json',
                                           'import lxml']

config['component']['Array']['meta_type'] = 'EMCArray'   # Aka unique name    # assume portal_type = meta_type
config['component']['Array']['unique_name'] = 'EMCArray'   

                                             # Name, details, grid, id, type, defaultValue
config['component']['Array']['attributes'] = [ 
                                               {'Name': 'WBEM Tag', 
                                               'Names': 'WBEM Tags', 
                                               'default': None,
                                               'DetailDisplay': True,
                                               'PanelDisplay': True,
                                               'PanelWidth': 30,
                                               'PanelSortable': False,
                                               'type': 'string',
                                               'id': 'wbemTag'},

                                               {'Name': 'Cycle Count', 
                                               'Names': 'Cycle Counts', 
                                               'default': None,
                                               'DetailDisplay': False,
                                               'PanelDisplay': True,
                                               'PanelWidth': 10,
                                               'PanelRenderer': 'Zenoss.render.severity',
                                               'PanelSortable': True,
                                               'type': 'int',
                                               'id': 'cycles'},

                                               {'Name': 'Vendor', 
                                               'Names': 'Vendors', 
                                               'DetailDisplay': True,
                                               'PanelDisplay': True,
                                               'PanelWidth': 10,
                                               'PanelSortable': True,
                                               'default': 'Zenoss, Inc.',
                                               'type': 'string',
                                               'id': 'vendor'},
                                             ]

config['component']['Array']['PanelSort'] = [ 'name', 'ASC' ]
config['component']['Array']['PanelDropDown'] = [ ('Battery', 'Battery Description'),
                                                ]


# mixins for defining the properties (optional)
config['component']['Array']['base_properties'] = ['Hardware', 'Class2' ]
# mixins for defining the relations (optional)
config['component']['Array']['base_relations'] = ['Hardware']

# Chet thinks we should always show the template on a component ( always add factory_type stanza )
# config['component']['Array']['display_template'] = True   

# probably just reference file snippet locations
config['component']['Array']['custom_class_methods'] = "TODO"

config['Relations'] = [
                      [('device', 'ZenPacks.zenoss.Foo.Device'), '1-MC', ('arrays', 'ZenPacks.zenoss.Foo.Array') ],
                      [('battery', 'ZenPacks.zenoss.Foo.Battery'), '1-MC', ('arrays', 'ZenPacks.zenoss.Foo.Array') ],
                      [('device', 'ZenPacks.zenoss.Foo.Device'), '1-MC', ('batteries', 'ZenPacks.zenoss.Foo.Battery') ],
                      [('device', 'Device'), '1-MC', ('batteries', 'Battery') ],
                      [('arrays', 'ZenPacks.zenoss.Foo.Array'), 'M-M', ('disks', 'ZenPacks.zenoss.Foo.Disk') ],
                      [('array', 'ZenPacks.zenoss.Foo.Array'), '1-M', ('batteries', 'Battery') ],
                      [('device', 'ZenPacks.zenoss.Foo.Device'), '1-MC', ('disks', 'ZenPacks.zenoss.Foo.Disk') ],
                      [('array', 'ZenPacks.zenoss.Foo.Array'), '1-1', ('fan', 'ZenPacks.zenoss.Foo.Fan') ],
                     ]

# components (Battery)
config['component'].setdefault('Battery', {})
config['component']['Battery']['name'] = 'Battery'
config['component']['Battery']['names'] = 'Batteries'
config['component']['Battery']['unique_name'] = 'Battery'
config['component']['Battery']['class'] = ['Battery'] #if Battery then if we find this in the component config set the imports to import that file.
config['component']['Battery']['attributes'] = [ ]
