"""
Toon van Eneco Utility Gages.
This provides a component for the rebranded Quby thermostat as provided by
Eneco.
"""
import logging

from homeassistant.helpers.entity import Entity
import custom_components.toon as toon_main


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup sensors."""
    add_devices([
        toonSensor(hass, 'Gas', 'M3'),
        toonSensor(hass, 'Power', 'Watt'),
        toonSensor(hass, 'Today', 'kWh'),
    ])

class toonSensor(Entity):
    """Representation of a sensor."""

    def __init__(self, hass, name, unit_of_measurement):
        """Initialize the sensor."""
        self._name = name
        self._state = None
        self._unit_of_measurement = unit_of_measurement
        self.thermos = hass.data[toon_main.TOON_HANDLE]

    @property
    def should_poll(self):
        """Polling required"""
        return True

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.thermos.get_data(self.name.lower())

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return self._unit_of_measurement

    def update(self):
        """Get the latest data from the sensor."""
        self.thermos.update()
