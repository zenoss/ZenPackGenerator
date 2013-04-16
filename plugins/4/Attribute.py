#!/usr/bin/env python

class Attribute(object):
    def __init__(self,config):
        import pdb;pdb.set_trace()
"""
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
"""
if __name__ == "__main__":

    config = pydata.config
    co = ComponentFactory(config)
    import pdb;pdb.set_trace()

#    print ComponentExpand('Component',config,'ZenPacks.test.ComponentTest')
#    print ComponentExpand('Device',config,'ZenPacks.test.ComponentTest')
#    print ComponentExpand('ZenPacks.test.ComponentTest.Foo',config,'ZenPacks.test.ComponentTest')
#    print ComponentExpand('Battery',config,'ZenPacks.test.ComponentTest')
