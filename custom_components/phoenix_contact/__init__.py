"""Support for Electric Vehicle Charge Control (EM-CP-PP-ETH device by Phoenix Contact)"""

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .ev_charge_control import EvChargeControl
from .switch import EvChargeControlEntity
from .select import EvChargeCurrentEntity


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
    }
)


# async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
#    """Expose Electric Vehicle charge control via statemachine and services."""
#    evse = EvChargeControl(config[CONF_IP_ADDRESS])
#    await evse.refresh()
#    async_add_entities([EvChargeControlEntity(evse)])
#    async_add_entities([EvChargeCurrentEntity(evse)])
#    return True
