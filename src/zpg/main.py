import os
from zpg.options import ZpgOptionParser
from zpg.pluginmgr import PluginMgr
import pydata
import logging
import time
import sys
logging.basicConfig()
log = logging.getLogger('ZenPack Generator')

def main():
    log.info("Starting...")

    parser = ZpgOptionParser()
    (opts, args) = parser.parse_args()

    pluginMgr = PluginMgr(opts.version)
    pluginMgr.getPlugins()
    config = pydata.config

    if opts.rmind:
        print "ZenPack Generator Mind Reader Input"
        print
        print "Searching for CEO...."
        print
        time.sleep(2)
        print "Found Bill Karpovich"
        print
        time.sleep(2)
        print "Connecting...."
        print
        time.sleep(2)
        print "Connecting...."
        print
        time.sleep(2)
        print "Stimulating Brain Cells."
        print
        time.sleep(5)
        print "Connected"
        print
        time.sleep(2)
        print "Scanning.....(This May take some time)"
        print
        print
        print
        time.sleep(2)
        print "Traumatic Childhood Memory... Block Err .. (skipping)"
        print
        print
        print
        time.sleep(15)
        print "Scanning.....(100,000 Zenpacks found so far...)"
        print
        time.sleep(5)
        print "Scanning.....(100,000,000 Zenpacks found so far...)"
        print
        time.sleep(5)
        print "Scanning.....(100,000,000,000,000 Zenpacks found so far...)"
        print
        time.sleep(3)
        print "Error.... Too Many ZenPacks found... please limit search."
        print
        sys.exit(1)

   
    
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
