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
from transaction import commit

import sys
import json
import collections
import types
import logging
import re

from Products.Zuul import getFacade

# http://jira.zenoss.com/jira/browse/ZEN-5017
from Products.Zuul import info as ZuulInfo
from Products.Zuul.facades import ObjectNotFoundException
from Products.Zuul.infos.graphpoint import DataPointGraphPointInfo, ThresholdGraphPointInfo

log = logging.getLogger("zen.JsonTemplateLoader")
fix_ids = []


def die(message):
    print message
    sys.exit(1)


def JSONFileToTemplates(dmd, jsonFile, ZenPack):
    data = None
    with open(jsonFile, 'r') as jsonFileHandle:
        data = json.load(
            jsonFileHandle, object_pairs_hook=collections.OrderedDict)

    if data:
        for template_path, template_cfg in data.items():
            add_template(dmd, template_path, template_cfg, ZenPack)
        print "Templates loaded successfully."
        commit()

        process_fix_ids()
        commit()
    else:
        print "No template found... exiting..."
        sys.exit(0)


def JSONStringToTemplates(dmd, jsonString, ZenPack):
    global fix_ids

    data = None
    data = json.loads(jsonString, object_pairs_hook=collections.OrderedDict)

    if data:
        fix_ids = []

        for template_path, template_cfg in data.items():
            add_template(dmd, template_path, template_cfg, ZenPack)
        print "Templates loaded successfully."
        commit()

        process_fix_ids()
        commit()
    else:
        print "No template found... exiting..."
        sys.exit(0)

def fix_id(object, newId):
    global fix_ids
    fix_ids.append((object, newId, ))

def process_fix_ids():
    # in some cases, the objects get created with default IDs, and we need to fix them
    # to match the json file.  It seems that we need to wait until the initial version is
    # commit()ed, then rename them.
    if fix_ids:
        print "Renaming objects:"
        for object, newId in fix_ids:
            print "  %s => %s" % (object, newId)
            object.rename(str(newId))

def add_template(dmd, path, cfg, zenpack):
    tf = getFacade('template', dmd)
    if '/' not in path:
        die("%s is not a path. Include device class and template name", path)

    path_parts = path.split('|')
    id_ = path_parts[1]
    cfg['deviceClass'] = path_parts[0]
    try:
        # dmd comes from the zendmd interpreter.
        device_class = tf.getTree(cfg['deviceClass'])
    except ObjectNotFoundException:
        die("%s is not a valid deviceClass.", cfg['deviceClass'])

    existing_template = [t for t in tf.getObjTemplates(
        device_class.uid) if device_class.uid + '/rrdTemplates/' + id_ == t.uid]

    if existing_template:
        tf.deleteTemplate(existing_template[0].uid)

    template = tf.addTemplate(id_, device_class.uid)

    print "Loading template %s in %s" % (id_, device_class.uid)
    if 'targetPythonClass' in cfg:
        template.targetPythonClass = cfg['targetPythonClass']

    if 'description' in cfg:
        template.description = cfg['description']

    if 'datasources' in cfg:
        for datasource_id, datasource_cfg in cfg['datasources'].items():
            add_datasource(dmd, template, datasource_id, datasource_cfg)

    # Define the thresholds first to be available for the graphs
    if 'thresholds' in cfg:
        for threshold_id, threshold_cfg in cfg['thresholds'].items():
            add_threshold(
                dmd, device_class, template, threshold_id, threshold_cfg)

    if 'graphs' in cfg:
        for graph_id, graph_cfg in cfg['graphs'].items():
            add_graph(dmd, device_class, template, graph_id, graph_cfg)

    if zenpack:
        print "Adding template %s in %s to ZenPack %s" % (id_, device_class.uid, zenpack.id)
        dmd.ZenPackManager.addToZenPack(ids=[template.uid], pack=zenpack.id)


def add_datasource(dmd, template, id_, cfg):
    tf = getFacade('template', dmd)
    if 'type' not in cfg:
        die('No type for %s/%s.', template.id, id_)
    datasource_types = [ds_type['type'] for ds_type in tf.getDataSourceTypes()]
    if cfg['type'] not in datasource_types:
        die('%s datasource type is not one of %s.',
            cfg['type'], ', '.join(datasource_types))

    datasource = tf.addDataSource(template.uid, str(id_), cfg['type'])

    # http://jira.zenoss.com/jira/browse/ZEN-5017
    datasource = ZuulInfo(datasource)

    try:
        cfg['severity'] = cfg['severity'].lower()
    except:
        pass

    # Map severity names to values.
    if 'severity' in cfg:
        cfg['severity'] = {
            'critical': 5,
            'error': 4,
            'warning': 3,
            'unknown': 3,
            'info': 2,
            'debug': 1,
            'clear': 0,
        }.get(cfg['severity'], cfg['severity'])

    # Apply cfg items directly to datasource attributes.
    for k, v in cfg.items():
        if k not in ('type', 'datapoints'):
            # need to reference the object because 4.2.3
            # didnt register the commanddatasource properly.
            # http://jira.zenoss.com/jira/browse/ZEN-5303
            setattr(datasource._object, k, v)

    if 'datapoints' in cfg:
        for datapoint_id, datapoint_cfg in cfg['datapoints'].items():
            add_datapoint(dmd, datasource, datapoint_id, datapoint_cfg)


def add_datapoint(dmd, datasource, id_, cfg):
    tf = getFacade('template', dmd)
    datapoint = tf.addDataPoint(datasource.uid, str(id_))

    # http://jira.zenoss.com/jira/browse/ZEN-5017
    datapoint = ZuulInfo(datapoint)

    # Handle cfg shortcuts like DERIVE_MIN_0 and GAUGE_MIN_0_MAX_100.
    if isinstance(cfg, types.StringTypes):
        if 'DERIVE' in cfg.upper():
            datapoint.rrdtype = 'DERIVE'

        min_match = re.search(r'MIN_(\d+)', cfg, re.IGNORECASE)
        if min_match:
            datapoint.rrdmin = min_match.group(1)

        max_match = re.search(r'MAX_(\d+)', cfg, re.IGNORECASE)
        if max_match:
            datapoint.rrdmax = max_match.group(1)

    else:
        # Apply cfg items directly to datasource attributes.
        for k, v in cfg.items():
            if k not in ('aliases'):
                setattr(datapoint, k, v)

        if 'aliases' in cfg:
            add_aliases(dmd, datapoint, cfg['aliases'])


def add_aliases(dmd, datapoint, aliases):
    tf = getFacade('template', dmd)
    data = []
    for id_ in aliases.keys():
        id_ = str(id_)
        if aliases[id_]['formula'] is None:
            aliases[id_]['formula'] = ""
        data.append({'id': id_, 'formula': aliases[id_]['formula']})

    tf.setInfo(datapoint.uid, {'aliases': data})


def add_graph(dmd, device_class, template, id_, cfg):
    tf = getFacade('template', dmd)
    tf.addGraphDefinition(template.uid, str(id_))

    # http://jira.zenoss.com/jira/browse/ZEN-5019
    graph = tf.getGraphDefinition(template.uid + '/graphDefs/' + id_)

    # Apply cfg items directly to graph attributes.
    for k, v in cfg.items():
        if k not in ('graphpoints'):
            setattr(graph, k, v)

    if 'graphpoints' in cfg:
        for graphpoint_id, graphpoint_cfg in cfg['graphpoints'].items():
            add_graphpoint(
                dmd, device_class, template, graph, graphpoint_id, graphpoint_cfg)


def add_graphpoint(dmd, device_class, template, graph, id_, cfg):
    tf = getFacade('template', dmd)
    if cfg['type'] == 'Threshold':
        threshold = [t for t in tf.getThresholds(
            template.uid) if t.name == id_][0]
        tf.addThresholdToGraph(graph.uid, threshold.uid)

        graphpoints = []
        for gp in tf.getGraphPoints(graph.uid):
            if isinstance(gp, ThresholdGraphPointInfo) and gp.id == id_:
                graphpoint = gp
                break

    elif cfg['type'] == 'DataPoint':
        # this is all sorts of messed up getDataSources returns datapoints if the context is a device class
        # there isnt a getDataPoints call
        # the name of a datapoint appears to be a datasource.datapoint but the id path appears better
        # We are just splitting that and probably making some sort of bad
        # assumption here.
        datapoints = [dp for dp in tf.getDataSources(device_class.uid)
                      if dp._object.name() == cfg['dpName'] and
                      template.uid in dp.uid]
        for datapoint in datapoints:
            tf.addDataPointToGraph(datapoint.uid, graph.uid)
        # Normally we would try to find the created graphpoint by UID, but since we don't know that
        # we will find all graphpoints with the datapoint name.  If there are more than one,
        # we're in trouble.
        graphpoints = []
        for gp in tf.getGraphPoints(graph.uid):
            if isinstance(gp, DataPointGraphPointInfo) and gp.dpName == cfg['dpName']:
                graphpoints.append(gp)
        if len(graphpoints) != 1:
            # don't really know what to do here.. really, the only option is to delete the
            # pre-existing ones and hope there's only one in the json, but for now i'm leaving
            # that as an exercise to the user.
            print "Error: Expected to find one graphpoint, but found %d instead." % len(graphpoints)
            return
        graphpoint = graphpoints[0]
    else:
        print "GraphPoint of %s is not supported yet." % cfg['type']
        return

    # Apply cfg items directly to graph attributes.
    for k, v in cfg.items():
        if k not in ('type'):
            if k == 'description':
                graphpoint.setDescription(v)
            else:
                setattr(graphpoint, k, v)

    # Fix the graphpoint name/ID.  addDataPointToGraph sets it to a default value, but the
    # import file may have a different one specified.
    if graphpoint.id != id_:
        fix_id(graphpoint, id_)


def add_threshold(dmd, device_class, template, id_, cfg):
    tf = getFacade('template', dmd)
    # This is weird, the catalog is making us look up the datapoints at the
    # deviceclass level
    points = []
    allpoints = [(ds._object.name(), ds)
                 for ds in tf.getDataSources(device_class.uid)]

    # Handle a single datapoint
    if isinstance(cfg['dataPoints'], str):
        cfg['dataPoints'] = [cfg['dataPoints']]

    for dp in cfg['dataPoints']:
        for item in allpoints:
            if item[0] == dp:
                points.append(item[1].uid)
    tf.addThreshold(template.uid, cfg['type'], id_, points)
    threshold = [t for t in tf.getThresholds(
        template.uid + '/thresholds/' + id_)][0]

    # Apply cfg items directly to threshold attributes.
    for k, v in cfg.items():
        if k not in ('dataPoints', 'type'):
            setattr(threshold, k, v)


class ImportTemplate(ZenScriptBase):

    def buildOptions(self):
        ZenScriptBase.buildOptions(self)
        self.parser.add_option("-z", "--zenpack", dest="zenpack",
                               help="ZenPack to Add Templates To", metavar="ZenPack")

    def run(self):
        self.zenpack = None
        if self.options.zenpack:
            self.zenpack = self.dmd.ZenPackManager.packs._getOb(
                self.options.zenpack, None)
            if self.zenpack:
                if not self.zenpack.isDevelopment():
                    print "%s is not a valid Development Mode Zenpack. Exiting...." % self.options.zenpack
                    sys.exit(1)
            else:
                print "%s is not a valid Zenpack. Exiting...." % self.options.zenpack
                sys.exit(1)
        if self.args:
            print "Reading Templates from %s" % self.args[0]
            JSONFileToTemplates(self.dmd, self.args[0], self.zenpack)
        else:
            print "Reading Templates from StdIn"
            JSONStringToTemplates(self.dmd, sys.stdin.read(), self.zenpack)


if __name__ == "__main__":
    it = ImportTemplate(connect=True)
    it.run()
