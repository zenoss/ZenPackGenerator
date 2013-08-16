==============================================================================
Specific Examples of ZPG Use Cases
==============================================================================
 This document will provide specific use cases and fragments that will
hopefully guide the users onto a higher plane of ZPG conciousness.

Devices without a Root
==============================================================================

OracleDB::

In this example OracleDB is a device that inherits its /Device base from the
parent server, be it Linux, AIX, Solaris, or some "other" operating system.
This means that it needs to be able to patch itself underneath the device tree
of that server target type and not have a stand-alone device root.

Thus inside of ZenPacks.zenoss.OracleDB/ZenPacks/zenoss/OracleDB/__init__.py
we should see:

__init__.py::

    # Define new device relations.  
    NEW_DEVICE_RELATIONS = (
        ('instance', 'OracleInstance'),
        ('storage', 'OracleStorage'),
        ('rac', 'OracleRAC'),
        ('schema', 'OracleSchema'),
    )

In order to achieve this you must remove the entire "deviceType" structure out of
the ZPG json file;

OracleDB.json Example::

  {
    "id": "ZenPacks.zenoss.OracleDB",
    "author": "Zenoss",
    "version": "0.0.1",
    "compat_zenoss_vers": ">=4.2",

    "deviceClasses": [{
        "path": "",

        "componentTypes": [
                        {
                "name": "Instance",
                "meta_type": "OracleInstance",
                "properties": [
                    {"name": "sid"},
                    {"name": "name_label"},
                    {"name": "connectionString", "Type": "string"},
                    {"name": "hostname"},
                    {"name": "oracleVersion"},
                    {"name": "databaseName"},
                    {"name": "databaseDBID"},
                    {"name": "databasePlatformName"},
                    {"name": "RACnetworkPeers"},
                    {"name": "instanceRole"},
                    {"name": "publicIP"},
                    {"name": "interconnectIP"}
                ]
            },...
      }]....
  }
