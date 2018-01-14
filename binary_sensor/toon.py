"""
Toon van Eneco burner binary sensor.

This provides a sensor for water heater ("burner") activity. The burner can
either be an actual gas burner or an electric heater.
"""
import logging

from homeassistant.components.binary_sensor import BinarySensorDevice
import custom_components.toon as toon_main

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Setup burner."""
    _toon_main = hass.data[toon_main.TOON_HANDLE]

    device = []

    if _toon_main.toon.thermostat_info.burner_info:
        device.append(BurnerSensor(hass))

    add_devices_callback(device, True)


class BurnerSensor(BinarySensorDevice):
    """Representation of a sensor."""
    def __init__(self, hass):
        """Initialize the sensor."""
        self._name = "burner_status"
        self._state = False
        self._icon = "mdi:fire"
        self.toon = hass.data[toon_main.TOON_HANDLE]

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self):
        """Return the status of the sensor."""
        return self.toon.get_data("burner_on")

    @property
    def icon(self):
        """Return the mdi icon of the sensor."""
        return self._icon

    def update(self):
        """Update sensor state."""
        self.toon.update()
