#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
##############################################################################

import logging
import os

from git import Repo

from .memoize import memoize

from .colors import error, warn, debug, info, green, red, yellow
from ._defaults import Defaults
from ._zenoss_utils import prepId
from .Component import Component
from .ComponentJS import ComponentJS
from .Configure import Configure
from .DirLayout import DirLayout
from .DiscoveryMapping import DiscoveryMapping
from .DeviceClass import DeviceClass
from .License import License
from .ObjectsXml import ObjectsXml
from .Organizer import Organizer
from .Relationship import Relationship
from .RootInit import RootInit
from .Setup import Setup
from .UtilsTemplate import UtilsTemplate
from .ZenPackUI import ZenPackUI
from .ImpactPy import ImpactPy
from .ImpactZcml import ImpactZcml
from .AutoClassificationZcml import AutoClassificationZcml

defaults = Defaults()


class Opts(object):

    def __init__(self):
        self.skip = False
        self.dest = os.getcwd()


class ZenPack(object):

    def __init__(self,
                 id,
                 author=defaults.get("author"),
                 version=defaults.get("version"),
                 install_requires=None,
                 compat_zenoss_vers=">=4.2",
                 prev_zenpack_name="",
                 license=defaults.get("license"),
                 organizers=None,
                 zProperties=None,
                 deviceClasses=None,
                 relationships=None,
                 discoveryMappings=None,
                 opts=None,
                 *args,
                 **kwargs
                 ):

        self.id = id
        self.opts = Opts() if opts is None else opts
        self.destdir = DirLayout(self, self.opts.dest)
        self.namespace = id
        self.deviceClasses = {}
        self.components = {}
        self.relationships = {}
        self.discoveryMappings = {}
        self.organizers = {}
        self.componentJSs = {}
        self.zproperties = {}
        self.author = author
        self.version = version
        self.license = License(self, license)
        self.prepname = prepId(id).replace('.', '_')
        self.logger = logger = logging.getLogger('ZenPack Generator')
        for key in kwargs:
            do_not_warn = False
            layer = self.__class__.__name__
            msg = "WARNING: JSON keyword ignored in layer '%s': '%s'"
            margs = (layer, key)
            if not do_not_warn:
                warn(self.logger, yellow(msg) % margs)
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
            packages.append('.'.join(parts[:i + 1]))
        self.packages = packages
        self.namespace_packages = packages[:-1]
        self.configure_zcml = Configure(self)
        self.utils = UtilsTemplate(self)
        self.setup = Setup(self)
        self.rootinit = RootInit(self)
        self.zenpackUI = ZenPackUI(self)
        self.objects_xml = ObjectsXml(self)
        self.impact_zcml = ImpactZcml(self)
        self.autoclassification_zcml = AutoClassificationZcml(self)
        self.impact = ImpactPy(self)
        if zProperties:
            for zp in zProperties:
                self.addZProperty(**zp)

        if deviceClasses:
            for dc in deviceClasses:
                self.addDeviceClass(**dc)

        if relationships:
            for rel in relationships:
                self.addRelation(**rel)

        if discoveryMappings:
            for mapping in discoveryMappings:
                self.addDiscoveryMapping(**mapping)

        # Make sure we create the organizers after the deviceClasses
        # because we look up the zPythonClasses out of the deviceClasses
        if organizers:
            if isinstance(organizers, basestring):
                organizers = [organizers]
            else:
                organizers = list(organizers)
        else:
            organizers = []
        for organizer in organizers:
            self.addOrganizer(**organizer)

    @memoize
    def addDeviceClass(self, *args, **kwargs):
        dc = DeviceClass(self, *args, **kwargs)
        return dc

    @memoize
    def addComponentType(self, *args, **kwargs):
        c = Component(self, *args, **kwargs)
        return c

    def addRelation(self, *args, **kwargs):
        r = Relationship(self, *args, **kwargs)
        return r

    def addDiscoveryMapping(self, *args, **kwargs):
        r = DiscoveryMapping(self, *args, **kwargs)
        return r

    def addOrganizer(self, *args, **kwargs):
        o = Organizer(self, *args, **kwargs)
        return o

    def addZProperty(self, name, type_='string', default='',
                     Category=None, **kwargs):
        if type_ == 'string':
            if not default.startswith('\''):
                default = '\'' + default
                if len(default) == 1:
                    default = default + '\''
            if not default.endswith('\''):
                default = default + '\''

        for key in kwargs:
            do_not_warn = False
            layer = self.__class__.__name__
            msg = "WARNING: JSON keyword ignored in layer '%s': '%s'"
            margs = (layer, key)
            if key == "Type":
                msg = "WARNING: JSON keyword deprecated in '%s' layer. "\
                      "'%s' is now '%s'."
                margs = (layer, key, key.lower())
                self.type_ = kwargs[key]
            elif key == "type":
                self.type_ = type_ = kwargs[key]
                do_not_warn = True
            if not do_not_warn:
                warn(self.logger, yellow(msg) % margs)

        self.zproperties[name] = (name, default, type_, Category)

    def registerComponent(self, component):
        self.components[component.id] = component

    def registerRelationship(self, relationship):
        self.relationships[relationship.id] = relationship

    def registerDeviceClass(self, deviceClass):
        self.deviceClasses[deviceClass.id] = deviceClass
        # Add the ComponentJS pieces when we are at it.
        cjs = ComponentJS(deviceClass)
        self.componentJSs[cjs.name] = cjs

    def registerOrganizer(self, organizer):
        self.organizers[organizer.id] = organizer

    def registerDiscoveryMapping(self, discoveryMapping):
        self.discoveryMappings[discoveryMapping.oid] = discoveryMapping

    def __repr__(self):
        return "%s \n\tAUTHOR: %s\n\tVERSION: %s\n\tLICENSE: %s" \
               % (self.id, self.author, self.version, self.license)

    def updateGitTemplates(self):  # pragma: no cover
        # Create the git repo
        repo = Repo.init(self.destdir.path)
        try:
            repo.commit()
        except:
            repo.index.commit('Initial Commit from zpg (%s)' % self.version)
        # Update the repo
        repo.index.add([self.destdir.path + '/Templates'])
        if repo.is_dirty():
            repo.index.commit('zpg: Committed Template changes (%s)'
                              % self.version)

    def write(self, verbose=False):
        # Write the destination folders
        self.destdir.write()

        # Write the LICENSE.txt
        self.license.write()

        # Write the base setup.py
        self.setup.write()

        # Write configure.zcml
        self.configure_zcml.write()

        # Create the components
        for component in self.components.values():
            component.write()
        for cjs in self.componentJSs.values():
            cjs.write()

        # Write the ui elements
        self.zenpackUI.write()

        # Create the root level __init__.py file
        self.rootinit.write()

        # Create a utils file.
        self.utils.write()

        # Create an objects.xml file
        self.objects_xml.write()

        # Create the impact.zcml
        self.impact_zcml.write()

        # Create the impact.py
        self.impact.write()

        # Create the autoclassification.zcml
        self.autoclassification_zcml.write()

        self.updateGitTemplates()
