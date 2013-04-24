import os
from zpg.options import ZpgOptionParser
from zpg.pluginmgr import PluginMgr
import pydata
import logging
logging.basicConfig()
log = logging.getLogger('ZenPack Generator')

def main():
    log.info("Starting...")

    parser = ZpgOptionParser()
    (opts, args) = parser.parse_args()

    pluginMgr = PluginMgr(opts.version)
    pluginMgr.getPlugins()
    config = pydata.config

    for plugin in [p for p in pluginMgr.plugins if p.type == 'filter']:
        p = plugin(config,opts)
        config = p.run()
    for plugin in [p for p in pluginMgr.plugins if p.type == 'layout']:
        p = plugin(config,opts)
        p.run()

    for plugin in pluginMgr.plugins:
        if plugin.type in ['layout', 'filter']:
            continue
        p = plugin(config,opts)
        p.run()

if __name__ == '__main__':
    main() 
