==============================================================================
JSON Format
==============================================================================

This is one of the simplest json input files that will actually generate a zenpack.

.. include:: netbotzExample.txt

.. note:: This generator makes many assumptions for you as it builds a zenpack.  Many of these assumptions can be overridden via the json input file.  Others will need to be modified as part of the template files.

ZenPack
------------------------------------------------------------------------------

Json Options for a ZenPack::

    {
      "id": "ZenPacks.training.NetBotz",
      "author": "Your Name",
      "version": "0.0.1",
      "license": "gpl",
      "install_requires": "",
      "compat_zenoss_vers": ">=4.2",
      "prev_zenpack_name": "",
      "organizers": [],
      "zProperties": [],
      "deviceClasses": [],
      "relationships": []
    }

* id: A string defining the unique name of your Zenpack. [required]
* author: The Name of the ZenPack Author. [optional]
* version: The ZenPack version. [optional]
* license: The License type. [optional]
* install_requires: Installation Requirements for python [optional]
    * eg "install_requires": ['ZenPacks.zenoss.ExampleRequirement]
* compat_zenoss_vers: A String representing the zenoss versions this zenpack is compatible with. [optional]
    * eg "compat_zenoss_vers": ">=4.2"
* prev_zenpack_name: A String representing previous zenpack names. [optional]
* zproperties: An Array of :ref:`zproperty` elements. [optional]
* deviceClasses: An Array of :ref:`deviceClass` elements. [optional]
* relationships: An Array of :ref:`relationship` elements. [optional]
* organizers: An Array of :ref:`organizer` elements. [optional]

.. _zproperties:

zProperties []
----------------

Json Options for a zProperty::

    "zProperties": [{
        "name": "zExampleProperty",
        "type": "string",
        "default": "Default Value",
        "Category": None
    }]

* name: The Name of the zproperty as a string. [required]
* type: The Type of zproperty. [optional]
        Valid values: [string, int]
* default: The default value for the zProperty. [optional]
* Category: An optional category for the zProperty. [optional]

.. _deviceClasses:

deviceClasses []
---------------------------

Json Options for a deviceClass::

    "deviceClasses": [{
        "path": 'Device/Snmp',
        "prefix": '/zport/dmd',
        "zPythonClass": 'Products.ZenModel.Device.Device',
        "componentTypes": [],
        "deviceType": null
    }]


* path: A Path within the device class hierarchy. [required]
* prefix: A prefix that combined with the path will give the final path to the device class. [optional]
    * You will almost never need to change this.

* zPythonClass: the Python class to assign to this deviceClass. [optional]
    * The component can be in :ref:`shorthand` notation.
* componentTypes: An Array of :ref:`componentType` objects. [optional]
* deviceType: A single :ref:`deviceType` object. [optional]

.. _organizers:

organizers []
-------------

Json Options for a Organizer::

    "organizers": [{
        "name": "Devices/Server/Dell/Blade",
        "type": "DeviceClass",
        "properties": [{
            "name": "zPingMonitorIgnore", 
            "type": "boolean", 
            "value": "True"
        }, {
            "name": "zDeviceTemplates", 
            "type": "lines", 
            "value": [ "example.Template" ] 
        }]
    }]

* name: A slash separated path for the organizer
* type: The Organizer Type.  Currently "DeviceClass" is the only supported type.
* properties: An Array of :ref:`property` objects. [optional]
    * Only the name, Type, and value fields are valid here.

.. _relationships:

relationships []
----------------

Json Options for a Relationship::

    "relationships": [{
        "componentA": 'Fan',
        "componentB": 'Blades',
        "type": '1-M',
        "contained": True
    }, {
        "componentA": "VirtualServer",
        "componentB": "Service",
        "type": "M-M",
        "contained": false
    }, {
        "componentA": "HardDrive",
        "componentB": "TemperatureSensor",
        "type": "1-1",
        "contained": True
    }]

* componentA: a Parent component [required]
    * The component can be in :ref:`shorthand` notation.
* componentB: a Child component [required]
    * The component can be in :ref:`shorthand` notation.
* type: The type of Relationship [optional]
    * Defaults to 1-M
    * Valid types: 1-1, 1-M, M-M
* contained: Is componentB contained within componentA [optional]
    * Defaults to True
    * Valid Options [True/False]

.. _componentTypes:

componentTypes []
-----------------

Json Options for a ComponentType::

    "componentTypes": [{
        "name": "ComponentName",
        "names": "ComponentNames",
        "klasses": ['DeviceComponent'],
        "imports": ["import os", "import sys"],
        "meta_type": "componentname",
        "namespace": "Zenpacks.example.Demo",
        "panelSort": 'PropertyA',
        "panelSortDirection": "asc",
        "device": False,
        "properties": [],
        "componentTypes": [],
        "impacts": [],
        "impactedBy": []
    }]

* name: The Name of the Component, Used to define the Module and Class of a Component. [required]
* names: The Plural Form of the Component Name. [optional]
* klasses: A single Class or an array of Classes. [optional]
    * Valid entries:
        * 'ManagedEntity'
        * 'Products.ZenModel.ManagedEntity'
        * ['ManangedEntity', 'HWComponent']
        * ['Products.ZenModel.ManagedEntity', 'Products.ZenModel.HWComponent.HWComponent']
    * The component can be in :ref:`shorthand` notation.
* imports: a single import or an array of imports. [optional]
    * Valid entries:
        * 'import os'
        * ['import os', 'import sys']
* meta_type: The components meta_type [optional],
* namespace: The fully resolvable prefix for a Component. [optional]
    * Defaults to the ZenPack id
* panelSort: The default column property to sort by in the UI. [optional]
* panelSortDirection: The direction to sort by.
    * Valid entries:
        * 'asc'
        * 'dsc'
* device: Is this a device Component [optional]
    * Valid entries:
        * True
        * False
    * Defaults to False
* properties: An Array of :ref:`property` objects. [optional]
* componentTypes: An Array of :ref:`componentType` objects. [optional]
    * This sets up a One to Many Contained relationship of Nested objects.
* impacts: An Array of components that this component impacts.
    * The component can be in :ref:`shorthand` notation.
* impactedBy: An Array of components that this component is impactedBy.
    * The component can be in :ref:`shorthand` notation.
    
.. _deviceType:

deviceType []
-------------

Json Options for a DeviceType::

    "deviceType": [{
        "name": "DeviceName",
        "names": "DeviceNames",
        "klasses": ['DeviceComponent'],
        "imports": ["import os", "import sys"],
        "meta_type": "devicename",
        "namespace": "Zenpacks.example.Demo",
        "panelSort": 'PropertyA',
        "panelSortDirection": "asc",
        "properties": [],
        "componentTypes": [],
        "impacts": [],
        "impactedBy": []
    }]

* name: The Name of the Device Component, Used to define the Module and Class of a Component. [required]
* names: The Plural Form of the Device Component Name. [optional]
* klasses: A single Class or an array of Classes. [optional]
    * Valid entries:
        * 'ManagedEntity'
        * 'Products.ZenModel.ManagedEntity'
        * ['ManangedEntity', 'HWComponent']
        * ['Products.ZenModel.ManagedEntity', 'Products.ZenModel.HWComponent.HWComponent']
    * The component can be in :ref:`shorthand` notation.
* imports: a single import or an array of imports. [optional]
    * Valid entries:
        * 'import os'
        * ['import os', 'import sys']
* meta_type: The components meta_type [optional],
* namespace: The fully resolvable prefix for a Component. [optional]
    * Defaults to the ZenPack id
* panelSort: The default column property to sort by in the UI. [optional]
* panelSortDirection: The direction to sort by.
    * Valid entries:
        * ['asc', 'dsc']
* properties: An Array of :ref:`property` objects. [optional]
* componentTypes: An Array of :ref:`componentType` objects. [optional]
    * This sets up a One to Many contained relationship of Nested objects.
* impacts: An Array of components that this component impacts.
    * The component can be in :ref:`shorthand` notation.
* impactedBy: An Array of components that this component is impactedBy.
    * The component can be in :ref:`shorthand` notation.

.. _properties:

properties []
-------------

Json Options for a Property::

    "properties": [{
        "name": "PropertyName",
        "names": "PropertyNames",
        "mode": 'w',
        "value": 10,
        "detailDisplay": True,
        "gridDisplay": True,
        "sortable": True,
        "width": 10,
        "panelRenderer": 'PanelRenderer'
    }]

* name: The Name of the property [required]
* names: The Plural Name of the property [optional]
* mode: The Mode of the property [optional]
    * valid Inputs:
        * r
        * w
    * Defaults to w
* value: The default Value for a property.
    * Defaults to None
* detailDisplay: Display the property in the details section.
    * Valid Inputs:
        * True
        * False
    * Defaults to True
* gridDisplay: Display the property in the Grid Component Panel section.
    * Valid Inputs:
        * True
        * False
    * Defaults to True
* sortable: Is this property sortable in the Component Grid Panel [optional]
    * Valid Inputs:
        * True
        * False
    * Defaults to True
* width: The width of a component grid panel column in pixels. [optional]
    * Defaults to 10
* panelRenderer: A renderer to use when displaying the property. [optional]
    * Defaults to None

.. _shorthand:

ShortHand
---------

    Shorthand notation means that the Class is not fully resolved.
    This means the shorthand form will search for a component class with the same name inside the zenpack.  If found, the Component will be expanded to The fully resolvable path to the Component.  Eg `Component` will become `ZenPack.example.Demo.Component`.  If the Component does not exist inside the zenpack, then the Component will Expand to `Products.ZenModel.Component.Component`
