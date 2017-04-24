"""
Toon van Eneco Support.
This provides a component for the rebranded Quby thermostat as provided by
Eneco.
"""
import logging
import voluptuous as vol

# Import the device class from the component that you want to support
from homeassistant.const import (CONF_USERNAME, CONF_PASSWORD)
from homeassistant.helpers.discovery import load_platform
import homeassistant.helpers.config_validation as cv

# Home Assistant depends on 3rd party packages for API specific code.
REQUIREMENTS = ['toonlib==0.1.2']

_LOGGER = logging.getLogger(__name__)

DOMAIN = "toon"
TOON_HANDLE = "toon_handle"

# Validation of the user's configuration
CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Setup toon."""
    hass.data[TOON_HANDLE] = toonDataStore(config['toon']['username'], config['toon']['password'])

    # Load Climate (for Thermostat)
    load_platform(hass, 'climate', DOMAIN)

    # Load Sensor (for Gas and Power)
    load_platform(hass, 'sensor', DOMAIN)

    # Initialization successfull
    return True

class toonDataStore:
    """An object to store the toon data."""

    def __init__(self, username, password):
        """Initialize toon."""
        from toonlib import Toon

        # Creating the class
        toon = Toon(username, password)

        self.toon = toon
        self.data = {}

    def update(self):
        """Update toon data."""
        self.data["power"] = self.toon.power.value 
        self.data["today"] = round((float(self.toon.power.daily_usage) + float(self.toon.power.daily_usage_low)) / 1000, 2)
        self.data["temp"] = self.toon.temperature
        
        if self.toon.thermostat_state is not None:
            self.data["state"] = self.toon.thermostat_state.name
        else:
            self.data["state"] = "Manual"

        self.data["setpoint"] = float(self.toon.thermostat_info.current_set_point) / 100
        self.data["gas"] = round(float(self.toon.gas.daily_usage) / 1000, 2)

    def set_state(self, state):
        self.toon.thermostat_state = state
        self.update()

    def set_temp(self, temp):
        self.toon.thermostat = temp
        self.update()
        
    def get_data(self, data_id):
        """Get the cached data."""
        data = {'error': 'no data'}

        if data_id in self.data:
            data = self.data[data_id]

        return data


