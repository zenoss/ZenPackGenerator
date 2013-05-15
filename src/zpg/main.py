import os
from zpg.options import ZpgOptionParser
from zpg.pluginmgr import PluginMgr
import pydata
import logging
from lib.ZenPack import ZenPack

logging.basicConfig()
log = logging.getLogger('ZenPack Generator')

#def main():
#    log.info("Starting...")

#    parser = ZpgOptionParser()
#    (opts, args) = parser.parse_args()




    #pluginMgr = PluginMgr(opts.version)
    #pluginMgr.getPlugins()
    #config = pydata.config

    #for plugin in [p for p in pluginMgr.plugins if p.type == 'filter']:
    #    p = plugin(config,opts)
    #    config = p.run()
    #for plugin in [p for p in pluginMgr.plugins if p.type == 'layout']:
    #    p = plugin(config,opts)
    #    p.run()
#
#    for plugin in pluginMgr.plugins:
#        if plugin.type in ['layout', 'filter']:
#            continue
#        p = plugin(config,opts)
#        p.run()

#if __name__ == '__main__':
    #main() 

def main():
    log.info('ZenPack Generator Starting')
    parser = ZpgOptionParser()
    (opts, args) = parser.parse_args()
    import pdb;pdb.set_trace()
    zp = ZenPack('ZenPacks.training.NetBotz', destdir=opts.dest, opts=opts)
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
    import pdb;pdb.set_trace()
