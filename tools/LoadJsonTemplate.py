#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from transaction import commit
dmd = ZenScriptBase(connect=True).dmd

import sys
import json
import collections
import types
import logging

from Products.Zuul import IInfo
from Products.Zuul import getFacade

# http://jira.zenoss.com/jira/browse/ZEN-5017
from Products.Zuul import info as ZuulInfo
from Products.Zuul.facades import ObjectNotFoundException

log = logging.getLogger("zen.JsonTemplateLoader")

def ExportProp(obj, primaryKey='uid', excludes=[]):
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

def TemplatesToJSONFile(dmd, templates, jsonFile):
    tf=getFacade('template',dmd)
    data = {}
    for template in templates:
	rrdTemplate = IInfo(template)
	id_ = "%s|%s" % (rrdTemplate.uid.split('/rrdTemplates')[0], rrdTemplate.name)
	data[id_] = {}
	data[id_]['description'] = rrdTemplate.description
	data[id_]['targetPythonClass'] = rrdTemplate.targetPythonClass

	# Find the datasources
	data_ds = {}
	for ds in tf.getDataSources(rrdTemplate.uid):
	    ds = tf.getDataSourceDetails(ds.uid)
	    data_ds[ds.name] = ExportProps(ds, excludes=['id', 'getName', 'getDescription',
							    'name', 'newId','source','testable','availableParsers'])
            # Find the datapoints
	    data_dp = {}
	    for dp in tf.getDataSources(ds.uid):

	        data_dp[dp.newId] = ExportProps(dp, excludes=['aliases', 'isrow', 'leaf',
		    					     'availableRRDTypes', 'getDescription', 'id',
							     'getName', 'name', 'newId', 'type'])
	        # Find the aliases
		data_dp_alias = {}
		for alias in dp.aliases:
	  	    data_dp_alias[alias.name] = ExportProps(alias, excludes=['id', 'name', 'getName', 'getDescription',
									    'description'])

		    # Setinfo would prefer the Nones be emptry strings here.
	            if data_dp_alias[alias.name]['formula'] == None:
		        data_dp_alias[alias.name]['formula'] = ""

		data_dp[dp.newId]['aliases'] = data_dp_alias

	    data_ds[ds.name]['datapoints'] = data_dp
	data[id_]["datasources"] = data_ds

	# Find the thresholds
	data_thresh = {}
	for threshold in tf.getThresholds(rrdTemplate.uid):
	    data_thresh[threshold.name] = ExportProps(threshold, excludes=['getDescription', 
									  'eventClass', 'dsnames',
									  'getName', 'getDescription', 'id',
									  'name', 'newId'])
        data[id_]["thresholds"] = data_thresh

	# Find the graphs
	data_graph = {}
	for graph in tf.getGraphs(rrdTemplate.uid):
            data_graph[graph.name] = ExportProps(graph, excludes=['getDescription', 'getName', 'id', 'name', 'newId', 
								 'graphPoints', 'rrdVariables', 'fakeGraphCommands'])

            # Find the graph points
	    data_graph_point = {}
	    for graph_point in tf.getGraphPoints(graph.uid):
	        data_graph_point[graph_point.name] = ExportProps(graph_point, excludes=['getDescription', 'getName', 
                                                                                       'id', 'name', 'newId', 
										       'rrdVariables'])
	      
	    data_graph[graph.name]["graphpoints"] = data_graph_point

	data[id_]["graphs"] = data_graph

    with open(jsonFile, 'w') as outputfile:
        json.dump(data, outputfile, indent=4, sort_keys=True, separators=(',', ': '))

def JSONFileToTemplates(dmd,jsonFile):
    tf=getFacade('template',dmd)
    data = None
    with open(jsonFile, 'r') as jsonFileHandle:
        data = json.load(jsonFileHandle,object_pairs_hook=collections.OrderedDict)

    if data:
        for template_path, template_cfg in data.items():
            add_template(dmd,template_path,template_cfg)
        print "Templates loaded successfully."
        commit()
    else:
        print "No template found... exiting..."
        sys.exit(0)

def JSONStringToTemplates(dmd,jsonString):
    tf=getFacade('template',dmd)
    data = None
    data = json.loads(jsonString,object_pairs_hook=collections.OrderedDict)

    if data:
        for template_path, template_cfg in data.items():
            add_template(dmd,template_path,template_cfg)
        print "Templates loaded successfully."
        commit()
    else:
        print "No template found... exiting..."
        sys.exit(0)

def add_template(dmd,path, cfg):
    tf=getFacade('template',dmd)
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

    existing_template = [t for t in tf.getObjTemplates(device_class.uid) if device_class.uid+'/rrdTemplates/'+id_ == t.uid]
    
    if existing_template:
        tf.deleteTemplate(existing_template[0].uid)

    template = tf.addTemplate(id_,device_class.uid)
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
            add_threshold(dmd, device_class,template, threshold_id, threshold_cfg)

    if 'graphs' in cfg:
        for graph_id, graph_cfg in cfg['graphs'].items():
            add_graph(dmd, device_class,template, graph_id, graph_cfg)


def add_datasource(dmd, template, id_, cfg):
    tf=getFacade('template',dmd)
    if 'type' not in cfg:
        die('No type for %s/%s.', template.id, id_)
    datasource_types = [ds_type['type'] for ds_type in tf.getDataSourceTypes()]
    if cfg['type'] not in datasource_types:
        die('%s datasource type is not one of %s.',
            cfg['type'], ', '.join(datasource_types))

    datasource = tf.addDataSource(template.uid,str(id_),cfg['type'])
    
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
            #need to reference the object because 4.2.3
            #didnt register the commanddatasource properly.
            #http://jira.zenoss.com/jira/browse/ZEN-5303 
            setattr(datasource._object, k, v)

    if 'datapoints' in cfg:
        for datapoint_id, datapoint_cfg in cfg['datapoints'].items():
            add_datapoint(dmd, datasource, datapoint_id, datapoint_cfg)


def add_datapoint(dmd, datasource, id_, cfg):
    tf=getFacade('template',dmd)
    datapoint = tf.addDataPoint(datasource.uid,str(id_))
    
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
    tf=getFacade('template',dmd)
    data = []
    for id_ in aliases.keys():
        id_ = str(id_)
        if aliases[id_]['formula'] == None:
            aliases[id_]['formula'] = ""
        data.append({'id':id_,'formula':aliases[id_]['formula']})
    
    tf.setInfo(datapoint.uid, {'aliases':data})
    
def add_graph(dmd, device_class,template, id_, cfg):
    tf=getFacade('template',dmd)
    tf.addGraphDefinition(template.uid,str(id_))
    
    # http://jira.zenoss.com/jira/browse/ZEN-5019
    graph = tf.getGraphDefinition(template.uid+'/graphDefs/'+id_)

    # Apply cfg items directly to graph attributes.
    for k, v in cfg.items():
        if k not in ('graphpoints'):
            setattr(graph, k, v)

    if 'graphpoints' in cfg:
        for graphpoint_id, graphpoint_cfg in cfg['graphpoints'].items():
            add_graphpoint(dmd, device_class,template,graph, graphpoint_id, graphpoint_cfg)

def add_graphpoint(dmd, device_class,template, graph, id_, cfg):
    tf=getFacade('template',dmd)
    if cfg['type'] == 'Threshold':
        threshold = [t for t in tf.getThresholds(template.uid) if t.name == id_][0]
        tf.addThresholdToGraph(graph.uid,threshold.uid)
    elif cfg['type'] == 'DataPoint':
        # this is all sorts of messed up getDataSources returns datapoints if the context is a device class
        # there isnt a getDataPoints call
        # the name of a datapoint appears to be a datasource.datapoint but the id path appears better
        # We are just splitting that and probably making some sort of bad assumption here.
        datapoints = [dp for dp in tf.getDataSources(device_class.uid) 
                                             if dp._object.name() == cfg['dpName'] and 
                                                template.uid in dp.uid]
        for datapoint in datapoints:
            tf.addDataPointToGraph(datapoint.uid,graph.uid)
    else:
        print "GraphPoint of %s is not supported yet." % cfg['type']
        return
    
    try:
        graphpoint = [gp for gp in tf.getGraphPoints(graph.uid) if gp.dpName == cfg['dpName']][0]
    except Exception:
        graphpoint = [gp for gp in tf.getGraphPoints(graph.uid) if gp.id == id_][0]
   
    # Apply cfg items directly to graph attributes.
    for k, v in cfg.items():
        if k not in ('type'):
            setattr(graph, k, v)

def add_threshold(dmd, device_class,template, id_, cfg):
    tf=getFacade('template',dmd)
    # This is weird, the catalog is making us look up the datapoints at the deviceclass level
    points = []
    allpoints = [(ds._object.name(),ds) for ds in tf.getDataSources(device_class.uid)]

    # Handle a single datapoint
    if isinstance(cfg['dataPoints'], str):
        cfg['dataPoints'] = [cfg['dataPoints']]
    
    for dp in cfg['dataPoints']:
        for item in allpoints:
            if item[0] == dp:
                points.append(item[1].uid)
    tf.addThreshold(template.uid,cfg['type'],id_,points)
    threshold = [t for t in tf.getThresholds(template.uid+'/thresholds/'+id_)][0]

    # Apply cfg items directly to threshold attributes.
    for k, v in cfg.items():
        if k not in ('dataPoints','type'):
            setattr(threshold, k, v)

def main():
    # sys.argv[0] is zendmd. Pop it so the script can use normal conventions.
    sys.argv.pop(0)
    if len(sys.argv) == 1:
        JSONFileToTemplates(dmd,sys.argv[0])
    else:
        JSONStringToTemplates(dmd,sys.stdin.read())


if __name__ == "__main__":
   main()
