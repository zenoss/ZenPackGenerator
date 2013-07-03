import os
import sys
import json
from zpg.options import ZpgOptionParser
import logging
from lib.ZenPack import ZenPack

logging.basicConfig(level=logging.INFO)
root=logging.getLogger()
root.setLevel(level=logging.INFO)

def main():
    log = logging.getLogger('Main')
    log.info('ZenPack Generator Starting')
    parser = ZpgOptionParser()
    (opts, args) = parser.parse_args()

    if not opts.json:
        log.info("Required json input file missing.  exiting...")
        sys.exit(1)

    if opts.debug:
        log.setLevel(level=logging.DEBUG)
        log.debug('Turned on Debug Output')


    f = open(opts.json, 'r')
    jsi = json.load(f)
    jsi['opts'] = opts
    zp_json=ZenPack(**jsi)
    zp_json.write()
    log.info('ZenPack Generator Finished')
    log.info('')
    log.info('')
    log.info('\t   Possible Next Steps.')
    log.info('')
    log.info('\t\t1. Modify the Templates in %s/%s/Templates and rerun the zpg with the same input json.' % (opts.prefix, zp_json.id))
    log.info('\t\t2. Create a modeller plugin.')
    log.info('\t\t3. Install the ZenPack')
    log.info('\t\t4. Create a json rrdtemplate and load it with tools/LoadJsonTemplate.py')
    log.info('\t\t5. Update other settings via the webui.')
    log.info('\t\t6. Export the objects.xml from the running system back into this zenpack.')
    log.info('')

    #zp = ZenPack('ZenPacks.training.NetBotz2', opts=opts)
    #zp.addZProperty('zNetBotzExampleProperty', 'boolean', True, 'NetBotz')
    #zp.addZProperty('e1')
    #dc = zp.addDeviceClass('Device/Snmp', zPythonClass='NetBotzDevice')
    #e = dc.addComponentType('Enclosure')
    #e.addProperty('enclosure_status')
    #e.addProperty('error_status')
    #e.addProperty('parent_id')
    #e.addProperty('docked_id')
    #ts = e.addComponentType('TemperatureSensor')
    #ts.addProperty('port')
    #dc.deviceType.addProperty('temp_sensor_count', Type='int')
    #zp.write()
    # import pdb;pdb.set_trace()
