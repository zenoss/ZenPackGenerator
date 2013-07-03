#!/usr/bin/env python

from lxml import etree
import lxml.etree
import sys


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level + 1)
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

# tomany
for obj in root.xpath('//*[@id="instances"]'):
    import pdb
    pdb.set_trace()
    obj.getparent().remove(obj)

indent(tree.getroot())
print etree.tostring(tree, pretty_print=True)
