# MAybe replace this with a setup tools implementation

import os
import imp
import zpg
import inspect
class PluginMgr:
    def __init__(self,version,PluginFolder=None):
        # load the defaults
        # then major 
        # then minor
        self.version = version
        if not PluginFolder:
            self.PluginFolder = "/".join(inspect.getfile(zpg).split('/')[:-1]) + "/plugins"
        self.plugins = []

    def getSubFolders(self):
        PluginFolder = self.PluginFolder
        subfolders = []
        varr = self.version.split('.')
        for i,val in enumerate(varr):
            subfolders.append(".".join(varr[:i+1]))

        subfolders = list(reversed(sorted(map(lambda x: '/'.join([PluginFolder,x]), subfolders))))
        subfolders.append('/'.join([PluginFolder,'default']))
        self.subfolders = subfolders

    def getPlugins(self):
        self.getSubFolders()
        for folder in self.subfolders:
            if os.path.isdir(folder):
                possibleplugins = [x for x in os.listdir(folder) if x.endswith('.py')]
                for plugin in possibleplugins:
                    self.plugins.append(self.load_from_file("%s/%s" % (folder,plugin)))

    def load_from_file(self,filepath):
        class_inst = None
        expected_class = 'MyClass'

        mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
        py_mod = imp.load_source(mod_name, filepath)
        klass = getattr(py_mod, mod_name, None)
        return klass
   
 

'''
for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        plugins.append({"name": i, "info": info})
    return plugins
'''
"""
def getPlugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        plugins.append({"name": i, "info": info})
    return plugins
"""       
