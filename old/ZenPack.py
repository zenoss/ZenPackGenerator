#! /usr/bin/env python
class ZenPack(object):

    def __init__(self,name,
                      version, 
                      Author, 
                      License, 
                      Requires, 
                      Compat, # key off of this for zenpack version?
                      Template):
        self.name = name
        self.version = str(version)
        self.Author = str(Author)
        self.License = License
        self.Requires = Requires
        self.Compat = Compat
        self.outputBaseDir="~"

    def makeOutputDir(self):
        print "I Need to make a dir if it doesnt already exist"

    def generateManifest(self):
        print "graft ZenPacks" 

    def addComponents(self,component)
        pass

    

if __name__ == "__main__":
    zp = ZenPack('ZenPack.zenoss.Generated',1.0,'Zenoss',"GPL","","","")
    import pdb;pdb.set_trace()
    
 
#config['zp']['NAME']="ZenPack.zenoss.Generated"
#config['zp']['VERSION']="1.0"
#config['zp']['AUTHOR']="Zenoss"
#config['zp']['LICENSE']="1.0"
#config['zp']['INSTALL_REQUIRES']= ["ZenPacks.zenoss.PyCollector",
#                                   "ZenPacks.zenoss.PyWBEM",
#                                   "ZenPacks.zenoss.StorageBase"]

#config['zp']['COMPAT_ZENOSS_VERS']= ">=4.1.70"
#config['zp']['PREV_ZENPACK_NAME']= ""

