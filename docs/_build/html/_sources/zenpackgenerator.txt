==============================================================================
ZenPack Generator
==============================================================================

Description
------------------------------------------------------------------------------

This gpl tool is meant to be an aide in the process of developing ZenPacks from scratch.
The goal of this project is to reduce the amount of time it takes to create a zenpack by taking a json formatted input file and generating a directory structure containing prepopulated files.

This generator will perform many tasks for you but not all of them.  At some point you will need
to leave the generator and tweak the ZenPack by hand.


The ZenPack Generator will perform these operations for you

* Layout the ZenPack directory Structure.

* Pre-populate many sections of boilerplate.

* Create the root __init__.py file.

* Create a Configure.zcml file for UI JavaScript registration.

* Create Components.

* Create Relationships between Components.

* Create most of the JavaScript for the UI.

The ZenPack Generator will NOT perform these operations.

* Create custom modelers.

* Create RRDTemplates.

* Update the objects.xml

ZenPack Generator Source Code: https://github.com/zenoss/ZenPackGenerator

Prerequisites
------------------------------------------------------------------------------

* Linux or Mac
* Python 2.7

This tool does NOT require a zenoss server.

Installation
------------------------------------------------------------------------------

Current Installation Steps. (Development mode)

* Clone the tool from the git repo.

  * git clone https://github.com/zenoss/ZenPackGenerator.git

* Install the ZenPack Generator Dependancies

  * cd ZenPackGenerator

  * python setup.py develop

* Testing successful installation

  * zpg -h

Quick Start
------------------------------------------------------------------------------
* Write a JSON file.  An example is listed below.

  .. include:: netbotzExample.txt
  See the :doc:`Json Format guide <jsonformat>` for more examples of the json input file.

* run the command `zpg -j netbotz.json -p /tmp/zpg`

    * /tmp/zpg is the destination prefix for the generated ZenPack.

You will find the ZenPack in `/tmp/zpg/ZenPacks.training.NetBotz`

At this point you can modify the templates found in `/tmp/zpg/ZenPacks.training.NetBotz/Templates`
and then rerun `zpg -j netbotz.json -p /tmp/zpg` to regenerate your zenpack with the modified templates.  Once you find the Generator to be too limiting move on to modifying the zenpack following the normal procedures.


