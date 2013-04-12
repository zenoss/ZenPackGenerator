from zope.interface import implements

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t


class Enclosure(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'NetBotzEnclosure'

    # Fields inherited from DeviceComponent and ManagedEntity
    #   id, title, snmpindex

    enclosure_status = None
    error_status = None
    parent_id = None
    docked_id = None

    _properties = ManagedEntity._properties + (
        {'id': 'enclosure_status', 'type': 'string'},
        {'id': 'error_status', 'type': 'string'},
        {'id': 'parent_id', 'type': 'string'},
        {'id': 'docked_id', 'type': 'string'},
        )

    _relations = ManagedEntity._relations + (
        ('sensor_device', ToOne(ToManyCont,
            'ZenPacks.training.NetBotz.NetBotzDevice',
            'enclosures',
            )),

        ('temperature_sensors', ToManyCont(ToOne,
            'ZenPacks.training.NetBotz.TemperatureSensor',
            'enclosure',
            )),
        )

    factory_type_information = ({
        'actions': ({
            'id': 'perfConf',
            'name': 'Template',
            'action': 'objTemplates',
            'permissions': (ZEN_CHANGE_DEVICE,),
            },),
        },)

    def device(self):
        return self.sensor_device()

    def getRRDTemplateName(self):
        return 'Enclosure'


class IEnclosureInfo(IComponentInfo):
    enclosure_status = schema.TextLine(title=_t(u'Enclosure Status'))
    error_status = schema.TextLine(title=_t(u'Error Status'))
    parent_id = schema.TextLine(title=_t(u'Parent Enclosure ID'))
    docked_id = schema.TextLine(title=_t(u'Docked Enclosure ID'))
    temperature_sensor_count = schema.Int(title=_t(u'Number of Temperature Sensors'))


class EnclosureInfo(ComponentInfo):
    implements(IEnclosureInfo)

    enclosure_status = ProxyProperty('enclosure_status')
    error_status = ProxyProperty('error_status')
    parent_id = ProxyProperty('parent_id')
    docked_id = ProxyProperty('docked_id')

    @property
    def temperature_sensor_count(self):
        # Using countObjects is fast.
        return self._object.temperature_sensors.countObjects()

        # Using len on the results of calling the relationship is slow.
        # return len(self._object.temperature_sensors())

