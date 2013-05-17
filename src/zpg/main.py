import os
import sys
import json
from zpg.options import ZpgOptionParser
from zpg.pluginmgr import PluginMgr
import pydata
import logging
from lib.ZenPack import ZenPack

logging.basicConfig()
log = logging.getLogger('ZenPack Generator')

def main():
    log.info('ZenPack Generator Starting')
    parser = ZpgOptionParser()
    (opts, args) = parser.parse_args()

    if not opts.json:
        print "Required json input file missing.  exiting..."
        sys.exit(1)

    f = open(opts.json, 'r')
    jsi = json.load(f)
    jsi['opts'] = opts
    jsi['destdir'] = opts.dest
    zp_json=ZenPack(**jsi)
    zp_json.write()

    # import pdb;pdb.set_trace()
    zp = ZenPack('ZenPacks.training.NetBotz2', destdir=opts.dest, opts=opts)
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
    # import pdb;pdb.set_trace()
