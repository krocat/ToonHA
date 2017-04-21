"""
Toon van Eneco Thermostat Support.
This provides a component for the rebranded Quby thermostat as provided by
Eneco.
"""
import logging

from homeassistant.components.climate import (
    ClimateDevice, ATTR_TEMPERATURE)
from homeassistant.const import TEMP_CELSIUS
import custom_components.toon as toon_main

STATE_COMFORT = "Comfort"
STATE_HOME = "Home"
STATE_AWAY = "Away"
STATE_SLEEP = "Sleep"
STATE_MANUAL = "Manual"

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup thermostat."""
    # Add toon
    add_devices((ThermostatDevice(hass), ), True)

class ThermostatDevice(ClimateDevice):
    """Interface class for the toon module and HA."""

    def __init__(self, hass):
        """Initialize the device."""
        self._name = "Toon van Eneco"
        self.hass = hass
        self.thermos = hass.data[toon_main.TOON_HANDLE]

        # set up internal state vars
        self._state = None
        self._temperature = None
        self._setpoint = None
        self._operation_list = [STATE_COMFORT, STATE_HOME, STATE_AWAY,
                                STATE_SLEEP, STATE_MANUAL]

    @property
    def name(self):
        """Name of this Thermostat."""
        return self._name

    @property
    def should_poll(self):
        """Polling is required."""
        return True

    @property
    def temperature_unit(self):
        """The unit of measurement used by the platform."""
        return TEMP_CELSIUS

    @property
    def current_operation(self):
        """Return current operation i.e. comfort, home, away."""
        state = self.thermos.get_data("state")

        if state == "0":
            return STATE_COMFORT
        elif state == "1":
            return  STATE_HOME
        elif state == "2":
            return  STATE_SLEEP
        elif state == "3":
            return  STATE_AWAY
        else:
            return  STATE_MANUAL
    
    @property
    def operation_list(self):
        """List of available operation modes."""
        return self._operation_list

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self.thermos.get_data("temp")

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self.thermos.get_data("setpoint")

    def set_temperature(self, **kwargs):
        """Change the setpoint of the thermostat."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        self.thermos.toon.login()
        self.thermos.toon.refresh_toon_state()
        result = self.thermos.toon.set_thermostat(float(temp))
        self.thermos.toon.logout()
        self.thermos.set_data("setpoint", float(temp))
        self.thermos.set_data("state", "99")


    def set_operation_mode(self, operation_mode):
        """Set new operation mode."""
        
        if operation_mode == STATE_COMFORT:
            program = "0"
        elif operation_mode == STATE_HOME:
            program = "1"
        elif operation_mode == STATE_SLEEP:
            program = "2"
        elif operation_mode == STATE_AWAY:
            program = "3"
        else:
            program = None
        
        if program is None:
            return False

        self.thermos.toon.login()
        self.thermos.toon.refresh_toon_state()
        result = self.thermos.toon.set_program_state(int(program))
        self.thermos.toon.logout()
        self.thermos.set_data("state", program)

    def update(self):
        """Update local state."""
        self.thermos.update()

