#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
#
import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase

import sys
import json
import logging
from Products.Zuul import IInfo
from Products.Zuul import getFacade
from Products.ZenModel.ZenPack import eliminateDuplicates
from Products.ZenModel.DeviceClass import DeviceClass
from Products.ZenModel.RRDTemplate import RRDTemplate

log = logging.getLogger("zen.JsonTemplateLoader")


def ExportProps(obj, primaryKey='uid', excludes=[]):
    lcl_data = {}
    for prop in dir(obj):
        if prop.startswith('_') or prop.startswith('set') or prop in excludes \
           or prop == primaryKey or prop in ['rename', 'meta_type', 'inspector_type']:
            continue
        try:
            value = getattr(obj, prop)
        except AttributeError:
            continue
        try:
            value = value()
        except:
            pass
        lcl_data[prop] = value
    return lcl_data


def TemplatesToJSONFile(dmd, templates, filename):
    tf = getFacade('template', dmd)
    data = {}
    for template in templates:
        rrdTemplate = IInfo(template)
        id_ = "%s|%s" % (rrdTemplate.uid.split(
            '/rrdTemplates')[0], rrdTemplate.name)
        data[id_] = {}
        data[id_]['description'] = rrdTemplate.description
        data[id_]['targetPythonClass'] = rrdTemplate.targetPythonClass

        # Find the datasources
        data_ds = {}
        for ds in tf.getDataSources(rrdTemplate.uid):
            ds = tf.getDataSourceDetails(ds.uid)
            data_ds[ds.name] = ExportProps(
                ds, excludes=['id', 'getName', 'getDescription',
                              'name', 'newId', 'source', 'testable',
                              'availableParsers'])
            # Find the datapoints
            data_dp = {}
            for dp in tf.getDataSources(ds.uid):
                data_dp[dp.newId] = ExportProps(
                    dp, excludes=['aliases', 'isrow', 'leaf',
                                  'availableRRDTypes', 'getDescription',
                                  'id', 'getName', 'name', 'newId', 'type'])
                # Find the aliases
                data_dp_alias = {}
                for alias in dp.aliases:
                    data_dp_alias[alias.name] = ExportProps(
                        alias, excludes=['id', 'name', 'getName',
                                         'getDescription', 'description'])

                    # Setinfo would prefer the Nones be emptry strings here.
                    if data_dp_alias[alias.name]['formula'] is None:
                        data_dp_alias[alias.name]['formula'] = ""

                data_dp[dp.newId]['aliases'] = data_dp_alias
            data_ds[ds.name]['datapoints'] = data_dp
        data[id_]["datasources"] = data_ds

    # Find the thresholds
    data_thresh = {}
    for threshold in tf.getThresholds(rrdTemplate.uid):
        data_thresh[threshold.name] = ExportProps(
            threshold, excludes=['getDescription', 'eventClass', 'dsnames',
                                 'getName', 'getDescription', 'id',
                                 'name', 'newId'])
        data[id_]["thresholds"] = data_thresh

    # Find the graphs
    data_graph = {}
    for graph in tf.getGraphs(rrdTemplate.uid):
        data_graph[graph.name] = ExportProps(
            graph, excludes=['getDescription', 'getName', 'id',
                             'name', 'newId', 'graphPoints',
                             'rrdVariables', 'fakeGraphCommands'])

        # Find the graph points
        data_graph_point = {}
        for graph_point in tf.getGraphPoints(graph.uid):
            data_graph_point[graph_point.name] = ExportProps(
                graph_point, excludes=['getDescription', 'getName',
                                       'id', 'name', 'newId', 'rrdVariables'])

        data_graph[graph.name]["graphpoints"] = data_graph_point

    data[id_]["graphs"] = data_graph
    with open(filename, 'w') as outputfile:
        json.dump(data, outputfile, indent=1,
                  sort_keys=True, separators=(',', ': '))


class ExportTemplate(ZenScriptBase):

    def buildOptions(self):
        ZenScriptBase.buildOptions(self)
        self.parser.add_option("-f", "--file", dest="filename",
                               help="write json to FILE", metavar="FILE")
        self.parser.add_option("-z", "--zenpack", dest="zenpack",
                               help="ZenPack to Dump Templates From", metavar="ZenPack")

    def parseOptions(self):
        ZenScriptBase.parseOptions(self)
        if not self.options.filename:
            print "Required option output file is missing. Exiting..."
            sys.exit(1)

    def run(self):
        rrdTemplates = []
        self.zenpack = None
        if self.options.zenpack:
            self.zenpack = self.dmd.ZenPackManager.packs._getOb(
                self.options.zenpack, None)
            if not self.zenpack:
                print "%s is not a valid Zenpack. Exiting...." % self.options.zenpack
                sys.exit(1)

        if not self.zenpack:
            packs = self.dmd.ZenPackManager.packs()
            for i, pack in enumerate(packs):
                print "\t %s: %s" % (i + 1, pack.id)
            input = raw_input("Which zenpack would you like to export? ")
            input = int(input)
            if (0 < input < len(packs) + 1):
                self.zenpack = packs[input - 1]
            else:
                print "Please select an integer between 1 and %s" % len(packs)
                sys.exit(1)

        packables = eliminateDuplicates(self.zenpack.packables())
        for packable in packables:
            if isinstance(packable, DeviceClass):
                for rrdTemplate in packable.getAllRRDTemplates():
                    rrdTemplates.append(rrdTemplate)

            elif isinstance(packable, RRDTemplate):
                rrdTemplates.append(packable)
        TemplatesToJSONFile(self.dmd, rrdTemplates, self.options.filename)

if __name__ == "__main__":
    et = ExportTemplate(connect=True)
    et.run()
