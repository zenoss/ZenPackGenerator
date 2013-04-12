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
config['zp']['NAME']="ZenPack.zenoss.Generated"
config['zp']['VERSION']="1.0"
config['zp']['AUTHOR']="ZenossLabs <labs@zenoss.com>"
config['zp']['LICENSE']="gpl"
config['zp']['INSTALL_REQUIRES']= ["ZenPacks.zenoss.PyCollector <=1.0.1",
                                   "ZenPacks.zenoss.PyWBEM",
                                   "ZenPacks.zenoss.StorageBase"]

config['zp']['COMPAT_ZENOSS_VERS']= ">=4.1.70"
config['zp']['PREV_ZENPACK_NAME']= ""
# packages and name_spaces are calculated on the name
'''End Setup.py'''

config['answers']['readme'] = True




# components (Array)
config['component'].setdefault('Array', {})
config['component']['Array']['name'] = 'Array'
config['component']['Array']['names'] = 'Arrays'
config['component']['Array']['class'] = ['Component']   == Aka import the things for them if using this
config['component']['Array']['class'] = ['TemperatureSensor']   == assume its under Products.ZenModel  with TS.TS
config['component']['Array']['class'] = ['ZenPacks.zenoss.Foo.Foo']  == set the imports and then replace with just Foo 
config['component']['Array']['class'] = ['Battery']  == if Battery then if we find this in the component config set the imports to import that file.
config['component']['Array']['class'] = ['Battery','Component'] 

# Assume we dont need to this but provide if needed.
config['component']['Array']['imports'] = ['import json',
                                           'import lxml']

config['component']['Array']['meta_type'] = 'EMCArray'   # Aka unique name    # assume portal_type = meta_type
config['component']['Array']['unique_name'] = 'EMCArray'   

                                             # Name, details, grid, id, type, defaultValue
config['component']['Array']['attributes'] = [ 
                                               {'Name': 'WBEM Tag', 
                                               'Names': 'WBEM Tags', 
                                               'DetailDisplay': True,
                                               'PanelDisplay': True
                                               'PanelWidth': 10,
                                               'id': 'wbemTag'},

                                               {'Name': 'Cycle Count', 
                                               'Names': 'Cycle Counts', 
                                               'DetailDisplay': False,
                                               'PanelDisplay': True
                                               'PanelWidth': 10,
                                               'PanelRenderer': 'Zenoss.render.severity',
                                               'PanelSortable': true,
                                               'type': 'int',
                                               'id': 'cycles'},

                                               {'Name': 'Vendor', 
                                               'Names': 'Vendors', 
                                               'DetailDisplay': True,
                                               'PanelDisplay': True
                                               'PanelWidth': 10,
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

#Todo
config['Relations'] = ['Array', '2MC', 'Device']

# components (Battery)
config['component'].setdefault('Battery', {})
config['component']['Battery']['name'] = 'Battery'

# components (
# components (PowerSupply)
config['component'].setdefault('PowerSupply', {})
config['component']['PowerSupply']['name'] = 'PowerSupply'
config['component']['PowerSupply']['meta_type'] = 'EMCPowerSupply'
config['component']['PowerSupply']['attributes'] = [('serialNumber','string','w'),
                                                    ('emcstatus','string','w') ]

#2nd and third pieces of tuple are optional
config['component']['PowerSupply']['object'] = ('basePowerSupply', 'ZenPacks.zenoss.StorageBase', 'PowerSupply')




#TODO
#config['rel']
#'smis,''1->2MC'  'smis','#ZP#.SMISProvider.SMISProvider','#ZP#.Array.Array'

class component(object):
    def __init__(self,data,copyright="All Rights Reserved"):
        import pdb;pdb.set_trace()
        self.name = data['name']
        self.meta_type = data['meta_type']
        self.attributes = data['attributes']
        self.object = data['object']

    def generate_output(self):
        data="class %s(%s):\n" % (self.name,self.object[0])
        data+="    meta_type = portal_type = \"%s\"\n" % self.meta_type
        for attribute in self.attributes:
            data+="    %s = %s\n" % ( attribute[0],"")
        print data
        return data

    def output(self):
        f=open('component.py', 'w')
        f.write(self.generate_output())
        f.close()


# objects
#      properties
#      attributes
#      factory
#

 

print json.dumps(config,indent=4)
print "JSON END -------------"
print dump(config,width=50,indent=4)
c=component(config['component']['PowerSupply'])
c.generate_output()
c.output()

#from pprint import pprint
#pprint(json.loads(json.dumps(config)))



# setup.py
