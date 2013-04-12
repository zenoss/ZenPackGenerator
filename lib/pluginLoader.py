import glob, imp
from os.path import join, basename, splitext

def importPluginModulesIn(directory):
    import pdb;pdb.set_trace()
    modules = {}
    for path in glob.glob(join(directory,'[!_]*.py')): # list .py files not starting with '_'
        name, ext = splitext(basename(path))
        modules[name] = imp.load_source(name, path)
    return modules
