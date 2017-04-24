"""
Support for Eneco Slimmer stekkers (Smart Plugs).

"""
import logging

from homeassistant.components.switch import SwitchDevice
from homeassistant.const import (
    STATE_OFF, STATE_ON, STATE_STANDBY, STATE_UNKNOWN)
from homeassistant.loader import get_component
import custom_components.toon as toon_main

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Setup discovered Smart Plugs."""
    toon_main = hass.data[toon_main.TOON_HANDLE]
    for plug in toon_main.toon.plugs:
        add_devices_callback([EnecoSmartPlug(plug)])


class EnecoSmartPlug(SwitchDevice):
    """Representation of a Smart Plug."""

    def __init__(self, plug):
        """Initialize the Smart Plug."""
        self.smartplug = plug
        self._unique_id = self.smartplug.device_uuid
        self._name = self.smartplug.name
        self._current_power_w = self.smartplug.current_usage
        self.today_energy_kwh = self.smartplug.daily_usage
        self._is_on = self.smartplug.current_state
        self._available = self.smartplug.is_connected

    @property
    def should_poll(self):
        """No polling needed with subscriptions."""
        return True

    @property
    def unique_id(self):
        """Return the ID of this switch."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the switch if any."""
        return self._name

    @property
    def current_power_w(self):
        """Current power usage in W."""
        return self._current_power_w

    @property
    def today_energy_kwh(self):
        """Today total energy usage in kWh."""
        return self.today_energy_kwh

    @property
    def is_on(self):
        """Return true if switch is on. Standby is on."""
        return self._is_on

    @property
    def available(self):
        """True if switch is available."""
        return self._available


    def turn_on(self, **kwargs):
        """Turn the switch on."""
        

    def turn_off(self):
        """Turn the switch off."""
        

    def update(self):
        """Update state."""