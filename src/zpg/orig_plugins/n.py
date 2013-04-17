#!/usr/bin/env python
from Cheetah.Template import Template
import pydata
import pprint

if __name__ == "__main__":
   
    config = pydata.config 
    t = Template(file="n.tmpl", searchList=[config])
    print t.respond() 
