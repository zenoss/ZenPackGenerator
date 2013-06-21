#!/usr/bin/env python

from lxml import etree
import sys

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


if len(sys.argv) > 1:
    src = sys.argv[1]
else:
    src = sys.stdin

tree = etree.parse(src)
root = tree.getroot()

#for obj in root.xpath('//*[@class="DeviceClass"]'):
#    obj.getparent().remove(obj)

for obj in root.xpath('//*[starts-with(@id,"rrdTemplate")]'):
    obj.getparent().remove(obj)

for obj in root.xpath('//*[starts-with(@id,"/zport/dmd/zenMenus")]'):
    obj.getparent().remove(obj)

for obj in root.xpath('//*[starts-with(@class,"RRDTemplate")]'):
    obj.getparent().remove(obj)

for obj in root.xpath('//*[starts-with(@class,"OSProcess")]'):
    obj.getparent().remove(obj)

for obj in root.xpath('//*[starts-with(@class,"Event")]'):
    obj.getparent().remove(obj)

for obj in root.xpath('//*[starts-with(@class,"Manufa")]'):
    obj.getparent().remove(obj)

for obj in root.xpath('//*[starts-with(@class,"IpServ")]'):
    obj.getparent().remove(obj)

for obj in root.xpath('//*[starts-with(@class,"WinServ")]'):
    obj.getparent().remove(obj)

for obj in root.xpath('//*[starts-with(@class,"Report")]'):
    obj.getparent().remove(obj)

for obj in root.xpath('//*[@class="HardwareClass"]'):
    obj.getparent().remove(obj)

for obj in root.xpath('//*[@class="SoftwareClass"]'):
    obj.getparent().remove(obj)

for obj in root.xpath('//*[starts-with(@class, "Mib")]'):
    #print tree.getpath(obj), "Mib"
    obj.getparent().remove(obj)

for obj in root.xpath('//comment()'):
    obj.getparent().remove(obj)

for obj in root.xpath('//*'):
    obj.text = obj.text.strip('\n')
    obj.text = obj.text.strip()
    #for attrib in ['type', 'mode','module', 'class', 'visible', 'select_variable']:
    #    if attrib in obj.attrib:
    #        del(obj.attrib[attrib])

#for obj in root.xpath('//*[@class="HardwareClass"]'):
#    print tree.getpath(obj), "HardwareClass",etree.tostring(obj)
#    obj.getparent().remove(obj)
#
##for obj in root.xpath('//*[@class="SoftwareClass"]'):
#    print tree.getpath(obj), "SoftwareClass",etree.tostring(obj)
#    obj.getparent().remove(obj)
#
#for obj in root.xpath('//*[@class="Manufacturer"]'):
##    print tree.getpath(obj), "Manufacturer"
#    obj.getparent().remove(obj)
#
#for obj in root.xpath('//*[starts-with(@class, "EventClass")]'):
#    print tree.getpath(obj), "EventClass"
#    obj.getparent().remove(obj)
#

indent(tree.getroot())
print etree.tostring(tree, pretty_print=True)
