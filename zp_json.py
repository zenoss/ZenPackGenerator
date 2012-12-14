#!/usr/bin/env python
import json
from collections import defaultdict

config = defaultdict(dict)
config['zp']['NAME']="ZenPack.zenoss.Generated"
config['zp']['VERSION']="1.0"
config['zp']['AUTHOR']="Zenoss"
config['zp']['LICENSE']="1.0"
config['zp']['INSTALL_REQUIRES']= ["ZenPacks.zenoss.PyCollector",
                                   "ZenPacks.zenoss.PyWBEM",
                                   "ZenPacks.zenoss.StorageBase"]

config['zp']['COMPAT_ZENOSS_VERS']= ">=4.1.70"
config['zp']['PREV_ZENPACK_NAME']= ""



# components (Array)
config['component'].setdefault('Array', {})
config['component']['Array']['name'] = 'Array'
config['component']['Array']['class'] = [('DeviceComponent','Products.ZenModel.DeviceComponent'), 
                                          'Hardware', 'Products.ZenModel.Hardware')]
config['component']['Array']['meta_type'] = 'EMCArray'
# May want to investigate collapsing the defaults?
config['component']['Array']['attributes'] = [('ArrayVendor','string','w', None),
                                              ('ArrayVersion','string','w', None),
                                              ('ArrayName','string','w', None),
                                              ('ArrayChassisType','string','w', None),
                                              ('BlockSWVersion','string','w', None),
                                              ('fileSWVersion','string','w', None),
                                              ('wbemClassName','string','w', ""),
                                              ('wbemIdentifyingNumber','string','w', ""),
                                              ('wbemTag','string','w',""),
                                              ('wbemStatsInstanceId','string','w', None,

config['component']['Array']['base_properties'] = ['Hardware']
config['component']['Array']['base_relations'] = ['Hardware']
config['component']['Array']['display_template'] = True
config['component']['Array']['relations'] = "TODO"
config['component']['Array']['custom_class_methods'] = "TODO"

# components (Battery)
config['component'].setdefault('Battery', {})
config['component']['Battery']['name'] = 'Battery'
config['component']['Battery']['class'] = [('HWComponent','Products.ZenModel.HWComponent')]
config['component']['Battery']['meta_type'] = 'Battery'

config['component']['Battery']['attributes'] = [('encId','string','r', ""),
                                                ('batterystatus','string','r', ""),
                                                ('batteryID','string','r', ""),
                                                ('arrayID','string','w', ""),
                                                ('manufacturer','string','r', ""),
                                                ('wbemClassName','string','r', ""),
                                                ('wbemTag','string','r', "")]


config['component']['Battery']['base_relations'] = ['HWComponent']
config['component']['Battery']['display_template'] = True
config['component']['Battery']['custom_class_methods'] = "TODO"

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
c=component(config['component']['PowerSupply'])
c.generate_output()
c.output()

#from pprint import pprint
#pprint(json.loads(json.dumps(config)))



# setup.py
