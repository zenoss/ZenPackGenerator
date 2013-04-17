def KlassExpand(config, id, klasses=None):
    classes = []
    if klasses == None:
        component = config['component'][id]
        klasses = component['class']

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
