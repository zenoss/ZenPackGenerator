#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################


from Component import Component
from Relationship import Relationship
from DeviceClass import DeviceClass
from Defaults import Defaults
from License import License
from utils import prepId
from Configure import Configure
from ComponentJS import ComponentJS
from Setup import Setup
from ZenPackUI import ZenPackUI
from RootInit import RootInit
from DirLayout import DirLayout
from git import Repo

#from UI import UI
from memoize import memoize
import unittest

defaults = Defaults()


class Opts(object):
    def __init__(self):
        self.skip = False
        self.prefix = '/tmp/zpg'


class ZenPack(object):

    def __init__(self,
                 id,
                 author=defaults.author,
                 version=defaults.version,
                 license=License(defaults.license),
                 install_requires=None,
                 compat_zenoss_vers=">=4.2",
                 prev_zenpack_name="",
                 zProperties=None,
                 deviceClasses=None,
                 relationships=None,
                 opts=Opts(),
                 ):

        self.id = id
        self.opts = opts
        self.destdir  = DirLayout(self, opts.prefix )
        self.namespace = id
        self.deviceClasses = {}
        self.components = {}
        self.relationships = {}
        self.componentJSs = {}
        self.zproperties = {}
        self.author = author
        self.version = version
        self.license = license

        self.prepname = prepId(id).replace('.', '_')
        if install_requires:
            if isinstance(install_requires, basestring):
                self.install_requires = [install_requires]
            else:
                self.install_requires = list(install_requires)
        else:
            self.install_requires = []
        self.compat_zenoss_vers = compat_zenoss_vers
        self.prev_zenpack_name = prev_zenpack_name

        packages = []
        parts = self.id.split('.')
        for i in range(len(parts)):
            packages.append('.'.join(parts[:i+1]))
        self.packages = packages
        self.namespace_packages = packages[:-1]

        self.configure_zcml = Configure(self)
        self.setup = Setup(self)
        self.rootinit = RootInit(self)
        self.zenpackUI = ZenPackUI(self)

        if zProperties:
            for zp in zProperties:
                self.addZProperty(**zp)

        if deviceClasses:
            for dc in deviceClasses:
                self.addDeviceClass(**dc)

        if relationships:
            for rel in relationships:
                self.addRelation(**rel)

    @memoize
    def addDeviceClass(self, *args, **kwargs):
        #if not 'ZenPack' in kwargs:
        #    kwargs['ZenPack'] = self
        dc = DeviceClass(self, *args, **kwargs)
        return dc

    @memoize
    def addComponentType(self, *args, **kwargs):
        #if not 'zenpack' in kwargs:
        #    kwargs['zenpack'] = self
        c = Component(self, *args, **kwargs)
        return c

    @memoize
    def addRelation(self, *args, **kwargs):
        #if not 'ZenPack' in kwargs:
        #    kwargs['ZenPack'] = self

        r = Relationship(self, *args, **kwargs)
        return r

    def addZProperty(self, name, type='string', default='', Category=None):
        if type == 'string':
            if not default.startswith('\''):
                default = '\'' + default
                if len(default) == 1:
                    default = default + '\''
            if not default.endswith('\''):
                default = default + '\''

        self.zproperties[name] = (name, default, type, Category)

    def registerComponent(self, component):
        self.components[component.id] = component

    def registerRelationship(self, relationship):
        self.relationships[relationship.id] = relationship

    def registerDeviceClass(self, deviceClass):
        self.deviceClasses[deviceClass.id] = deviceClass
        #Add the ComponentJS pieces when we are at it.
        cjs = ComponentJS(deviceClass)
        self.componentJSs[cjs.name] = cjs

    def __repr__(self):
        return "%s \n\tAUTHOR: %s\n\tVERSION: %s\n\tLICENSE: %s" \
               % (self.id, self.author, self.version, self.license)

    def updateGitTemplates(self):
        # Create the git repo
        repo = Repo.init(self.destdir .path)
        try:
            repo.commit()
        except:
            repo.index.commit('Initial Commit from zpg')

        #Update the repo
        repo.index.add([self.destdir .path+'/Templates'])

        if repo.is_dirty():
            repo.index.commit('zpg: Committed Template changes')

    def write(self):
        # Write the destination folders
        self.destdir .write()

        # Write the base setup.py
        self.setup.write()

        # Write configure.zcml
        self.configure_zcml.write()

        # Create the components
        for component in self.components.values():
            component.write()

        for cjs in self.componentJSs.values():
            cjs.write()

        self.zenpackUI.write()

        #Create the root level __init__.py file
        self.rootinit.write()

        self.updateGitTemplates()


if __name__ == "__main__":
    zp = ZenPack('ZenPacks.training.NetBotz')
    zp.addZProperty('zNetBotzExampleProperty', 'boolean', True, 'NetBotz')
    zp.addZProperty('e1')

    dc = zp.addDeviceClass('Device/Snmp', zPythonClass='NetBotzDevice')
    e = dc.addComponentType('Enclosure')
    e.addProperty('enclosure_status')
    e.addProperty('error_status')
    e.addProperty('parent_id')
    e.addProperty('docked_id')

    ts = e.addComponentType('TemperatureSensor')
    ts.addProperty('port')

    dc.deviceType.addProperty('temp_sensor_count', Type='int')

    zp.write()
