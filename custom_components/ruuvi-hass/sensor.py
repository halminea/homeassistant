"""Platform for RuuviTag sensor integration."""

import datetime
import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_FORCE_UPDATE, CONF_MONITORED_CONDITIONS, CONF_NAME, CONF_MAC
)

from ruuvitag_sensor.ruuvi import RuuviTagSensor


REQUIREMENTS = ['ruuvitag_sensor']

_LOGGER = logging.getLogger(__name__)

CONF_ADAPTER = 'adapter'
CONF_TIMEOUT = 'timeout'
CONF_POLL_INTERVAL = 'poll_interval'

DEFAULT_ADAPTER = 'hci0'
DEFAULT_FORCE_UPDATE = False
DEFAULT_NAME = 'RuuviTag'
DEFAULT_TIMEOUT = 3
MAX_POLL_INTERVAL = 10  # in seconds

# Sensor types are defined like: Name, units
SENSOR_TYPES = {
    'temperature': ['Temperature', TEMP_CELSIUS],
    'humidity': ['Humidity', '%'],
    'pressure': ['Pressure', 'hPa'],
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MAC): cv.string,
    vol.Optional(CONF_MONITORED_CONDITIONS, default=list(SENSOR_TYPES)):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
    vol.Optional(CONF_POLL_INTERVAL, default=MAX_POLL_INTERVAL): cv.positive_int,
    vol.Optional(CONF_ADAPTER, default=DEFAULT_ADAPTER): cv.string,
})

#def setup_platform(hass, config, add_entities, discovery_info=None):
#    """Set up the sensor platform."""
#    add_entities([RuuviTagSensor()])

def setup_platform(hass, config, add_devices, discovery_info=None):
    mac_addresses = config.get(CONF_MAC)
    if not isinstance(mac_addresses, list):
        mac_addresses = [mac_addresses]

    probe = RuuviProbe(RuuviTagSensor, mac_addresses, config.get(CONF_TIMEOUT), config.get(CONF_POLL_INTERVAL))

    devs = []
    for mac_address in mac_addresses:
        for condition in config.get(CONF_MONITORED_CONDITIONS):
            prefix = config.get(CONF_NAME, mac_address)
            name = "{} {}".format(prefix, condition)
            _LOGGER.info("setup_platform for RuuviTag %s" % name)
            devs.append(RuuviSensor(
                probe, config.get(CONF_MAC), condition, name
            ))
    add_devices(devs)


class RuuviProbe(object):
    def __init__(self, RuuviTagSensor, mac_addresses, timeout, max_poll_interval):
        self.RuuviTagSensor = RuuviTagSensor
        self.mac_addresses = mac_addresses
        self.timeout = timeout
        self.max_poll_interval = max_poll_interval
        self.last_poll = datetime.datetime.now()

        default_condition = {'humidity': None, 'identifier': None, 'pressure': None, 'temperature': None}
        self.conditions = {mac: default_condition for mac in mac_addresses}

    def poll(self):
        if (datetime.datetime.now() - self.last_poll).total_seconds() < self.max_poll_interval:
            return
        try:
            self.conditions = self.RuuviTagSensor.get_data_for_sensors(self.mac_addresses, self.timeout)
        except:
            _LOGGER.exception("Error on polling sensors")
        self.last_poll = datetime.datetime.now()


class RuuviSensor(Entity):
    """Representation of the RuuviTag Sensor."""
    def __init__(self, poller, mac_address, sensor_type, name):
        self.poller = poller
        self._name = name
        self.mac_address = mac_address
        self.sensor_type = sensor_type

        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the unit of measurement."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return SENSOR_TYPES[self.sensor_type][1]

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self.poller.poll()
        self._state = self.poller.conditions.get(self.mac_address, {}).get(self.sensor_type)
