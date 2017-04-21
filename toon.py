"""
Toon van Eneco Support.
This provides a component for the rebranded Quby thermostat as provided by
Eneco.
"""
import logging
import voluptuous as vol
from datetime import timedelta

# Import the device class from the component that you want to support
from homeassistant.const import (CONF_USERNAME, CONF_PASSWORD)
from homeassistant.helpers.discovery import load_platform
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

# Home Assistant depends on 3rd party packages for API specific code.
REQUIREMENTS = ['https://github.com/krocat/toon/archive/'
                'v1.0.4.zip#'
                'toon==1.0.4']

_LOGGER = logging.getLogger(__name__)

DOMAIN = "toon"
TOON_HANDLE = "toon_handle"

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=2)

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
        from toon.Toon import Toon

        # Creating the class
        toon = Toon(username, password)
        toon.set_maxretries(5)

        self.toon = toon
        self.data = {}


    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Update toon data."""
        result = self.toon.login()
        thermostat = self.toon.retrieve_toon_state()
        self.toon.logout()

        if 'powerUsage' in thermostat:
            self.data["power"] = thermostat["powerUsage"]["value"]
            if 'dayLowUsage' in thermostat["powerUsage"]:
                self.data["today"] = round((float(thermostat["powerUsage"]["dayUsage"]) / 1000) + (float(thermostat["powerUsage"]["dayLowUsage"]) / 1000), 2)
            else:
                self.data["today"] = round(float(thermostat["powerUsage"]["dayUsage"]) / 1000, 2)

        if 'thermostatInfo' in thermostat:
            self.data["temp"] = float(thermostat["thermostatInfo"]["currentTemp"]) / 100
            self.data["state"] = str(thermostat["thermostatInfo"]["activeState"])
            self.data["setpoint"] = float(thermostat["thermostatInfo"]["currentSetpoint"]) / 100
        if 'gasUsage' in thermostat:
            self.data["gas"] = round(float(thermostat["gasUsage"]["dayUsage"]) / 1000, 2)

    def get_data(self, data_id):
        """Get the cached data."""
        data = {'error': 'no data'}

        if data_id in self.data:
            data = self.data[data_id]

        return data

    def set_data(self, data_id, value):
        """Set the cached data after update."""
        
        if data_id in self.data:
            self.data[data_id] = value

