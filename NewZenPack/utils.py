##LICENSE##

def KlassExpand(namespace,Klass)
    if len(Klass.split('.'))>1:

       if isinstance(value, basestring):
            value = [value]
        for Klass in value:
            if len(Klass.split('.'))==1:
                if Klass.split('.')[-1] in self.ZenPack.namespace:
                    Klass = '{0}.{1}.{1}'.format(self.ZenPack.namespace, Klass)
                else:
                    Klass = 'Products.ZenModel.{0}.{0}'.format(Klass)
            classes.append(Klass)
            Module = ".".join(Klass.split('.')[:-1])
            Class = Klass.split('.')[-1]
            Import = "from {0} import {1}".format(Module, Class)

            if Import not in self.imports:
                self.imports.append(Import)

        self._classes = classes


:set
def KlassExpand(
        classes = []
        if isinstance(value, basestring):
            value = [value]
        for Klass in value:
            if len(Klass.split('.'))==1:
                if Klass.split('.')[-1] in self.ZenPack.namespace:
                    Klass = '{0}.{1}.{1}'.format(self.ZenPack.namespace, Klass)
                else:
                    Klass = 'Products.ZenModel.{0}.{0}'.format(Klass)
            classes.append(Klass)
            Module = ".".join(Klass.split('.')[:-1])
            Class = Klass.split('.')[-1]
            Import = "from {0} import {1}".format(Module, Class)

            if Import not in self.imports:
                self.imports.append(Import)

        self._classes = classes


def KlassExpand(config, id, klasses=None):
    classes = []
    if klasses == None:
        component = config['component'][id]
        klasses = component['class']

    if isinstance(klasses,str):
        klasses = [klasses]

    for klass in klasses:
        split = klass.split('.')
        if klass.lower() == 'component':
            classes.append(('Products.ZenModel.DeviceComponent','DeviceComponent'))
            classes.append(('Products.ZenModel.ManagedEntity', 'ManagedEntity'))

        elif klass in config['component'].keys():
            classes.append((config['NAME'], klass))

        elif len(split) == 1:
            classes.append(('Products.ZenModel', klass))

        elif len(split) > 0:
            classes.append((".".join(split[0:-1]), split[-1]))
    return classes
