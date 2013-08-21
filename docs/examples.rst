==============================================================================
Examples of JSON input files
==============================================================================

Netbotz
--------------------

NetBotz II Example::

   {
       "id": "ZenPacks.training.NetBotz",
       "zProperties": [{
           "type": "boolean",
           "default": true,
           "Category": "NetBotz",
           "name": "zNetBotzExample"
       },{
       "name": "e1"
       }],
       "deviceClasses": [{
           "componentTypes": [{
               "name": "Enclosure", "properties": [
                   { "name": "enclosure_status" },
                   { "name": "error_status" },
                   { "name": "parent_id" },
                   { "name": "docked_id" }
               ]}, {
               "name": "TemperatureSensor",
               "properties": [
                   { "name": "enclosure" },
                   { "name": "port" }
               ]}
           ],
           "deviceType":
           {
               "name": "NetBotzDevice",
               "properties":
               [{
                   "Type": "int",
                   "name": "temp_sensor_count"
               }]
           },
       "path": "Device/Snmp",
       "zPythonClass": "NetBotzDevice"
       }]
   }


Genbotz Generalization of Netbotz
----------------------------------

GenBotz Example with Organizers (DeviceClasses)::


   {

      "id": "ZenPacks.training.GenBotz",
      "zProperties": [
        { "type": "boolean",
          "default": true,
          "Category": "GenBotz",
          "name": "zGenBotzExample" },
        { "name": "e1" }
      ],

      "deviceClasses": [{
          "componentTypes": [
            { "name": "Enclosure",
              "properties": [
              { "name": "enclosure_status" },
              { "name": "error_status" },
              { "name": "parent_id" },
              { "name": "docked_id" } ]},
            { "name": "TemperatureSensor",
              "properties": [{
                  "name": "enclosure",
                  "name": "port"
              }]
            }
          ],
          "deviceType":
          {
              "name": "GenBotzDevice",
              "properties":
              [{
                  "Type": "int",
                  "name": "temp_sensor_count"
              }]
          },
        "path": "Devices/GenBotz",
        "zPythonClass": "GenBotzDevice"
      }],

     "organizers": [{
         "name": "Devices/GenBotz",
         "Type": "DeviceClass",
         "properties": [
             {
                 "name": "zPingMonitorIgnore",
                 "Type": "boolean",
                 "value": "True"
             },{
                 "name": "zDeviceTemplates",
                 "Type": "lines",
                 "value": [ "Device", "GenBotzDevice" ]
             }
         ]
     }]
   }

NetScalar
--------------------

NetScaler Example::

   {
       "id": "ZenPacks.zenoss.NetScaler",
       "author": "Zenoss labs",
       "version": "0.0.1",
       "compat_zenoss_vers": ">=4.2",
       "deviceClasses": [{
           "componentTypes": [{
               "name": "VirtualServer",
               "properties": [{
                   "name": "id"
               }]
           }, {
               "name": "Service",
               "properties": [{
                   "name": "id"
               }]
           }, {
               "name": "Server",
               "properties": [{
                   "name": "id"
               }]
           }, {
               "name": "ServiceGroup",
               "properties": [{
                   "name": "id"
               }]
           }],
           "deviceType": {
               "name": "NetScalerDevice",
               "properties": [{
                   "Type": "String",
                   "name": "id"
               }]
           },
           "path": "Device/Snmp",
           "zPythonClass": "NetScalerDevice"
       }],
       "relationships": [{
           "componentA": "NetScalerDevice",
           "componentB": "VirtualServer",
           "Type": "1-M",
           "Contained": true
       }, {
           "componentA": "NetScalerDevice",
           "componentB": "Service",
           "Type": "1-M",
           "Contained": true
       }, {
           "componentA": "NetScalerDevice",
           "componentB": "Server",
           "Type": "1-M",
           "Contained": true
       }, {
           "componentA": "NetScalerDevice",
           "componentB": "ServiceGroup",
           "Type": "1-M",
           "Contained": true
       }, {
           "componentA": "VirtualServer",
           "componentB": "Service",
           "Type": "M-M",
           "Contained": false
       }, {
           "componentA": "Service",
           "componentB": "Server",
           "Type": "1-M",
           "Contained": false
       }, {
           "componentA": "Service",
           "componentB": "ServiceGroup",
           "Type": "M-M",
           "Contained": false
       }]
   }
