#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################
from zpg.Template import Template
from Cheetah.Template import Template as cTemplate


class Configure(Template):

    def __init__(self, zenpack):
        self.zenpack = zenpack
        self.components = zenpack.components
        self.deviceClasses = zenpack.deviceClasses
        self.componentJSs = zenpack.componentJSs

    def customPathReporters(self):
        for c in self.components.values():
            if c.custompaths():
                return True
        return False

# TODO
# Router and facade
# custom device loaders
# dynamic view
# datasources
# datapoints

    def write(self):
        t = cTemplate(file='configure.zcml.tmpl', searchList=[self])
        print t

if __name__ == '__main__':
    # from ZenPack import ZenPack
    # zp = ZenPack('ZenPacks.zenoss.NetAppMonitor')
    # dc = zp.addDeviceClass('Storage/NetApp', zPythonClass='Device')
    # dc.addComponentType('DiskShelf')
    # dc.addComponentType('DiskShelves')
    # dc.addComponentType('ClusterPeer')
    # dc.addComponentType('SnapMirror')
    # dc.addComponentType('HardDisk')
    # dc.addComponentType('Interface')
    # dc.addComponentType('RAIDGroup')
    # dc.addComponentType('LUN')
    # dc.addComponentType('Aggregate')
    # dc.addComponentType('SystemNode')
    # dc.addComponentType('Plex')
    # dc.addComponentType('QTree')
    # dc.addComponentType('NetAppFS')
    # dc.addComponentType('VolumeSnap')
    # dc.addComponentType('VServer')
    # dc2 = zp.addDeviceClass('/')
    # sc2 = dc2.addComponentType('RabbitmqQueue')
    # v = dc.addComponentType('Volume')
    # v.addProperty('volume_name')
    # v.addProperty('size_total', Type='int')
    # v.addProperty('dsid', Type='int')
    # v.addProperty('fsid', Type='int')
    # v.addProperty('msid', Type='int')
    # v.addProperty('state')
    # v.addProperty('volume_type')
    # v.addProperty('volume_style')
    # v.addProperty('cluster_volume', Type=bool)
    # v.addProperty('constituent_volume', Type=bool)
    # v.addProperty('export_policy')
    # v.addProperty('junction_active', Type=bool)
    # v.addProperty('junction_parent_name')
    # v.addProperty('junction_path')
    # v.addProperty('cloneSnap', detailDisplay=False, gridDisplay=False)
    # v.addProperty('cloneOf', detailDisplay=False)
    # v.addProperty('uuid', detailDisplay=False)
    # v.addProperty('volType', detailDisplay=False)
    # v.addProperty('flone', detailDisplay=False)
    # v.addProperty('floneOf', detailDisplay=False)
    # v.addProperty('fsid', detailDisplay=False)
    # v.addProperty('owningHost', detailDisplay=False)
    # v.addProperty('volState', detailDisplay=False)
    # v.addProperty('volStatus', detailDisplay=False)
    # v.addProperty('options', detailDisplay=False)
    zp.write()
