"""Phoenix Contact's Electric Vehicle Charge Current Select."""
from homeassistant.components.select import SelectEntity

from homeassistant.const import CONF_IP_ADDRESS
from .const import DOMAIN
from .ev_charge_control import EvChargeControl


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Expose Electric Vehicle charge control via statemachine and services."""
    evse = EvChargeControl(config[CONF_IP_ADDRESS])
    await evse.refresh()
    async_add_entities([EvChargeCurrentEntity(evse)])
    return True


class EvChargeCurrentEntity(SelectEntity):
    """Representation of an Electric Vehicle Charge Control device."""

    def __init__(self, evse):
        """Initialize the sensor."""
        self._evse = evse
        self._attr_name = "EV Charge Current"
        self._attr_icon = "mdi:car-electric"
        self._attr_options = evse.status.current_options
        self._attr_current_option = evse.status.current
        self._attr_unique_id = f"{DOMAIN}-{evse.status.serial}"

    async def async_select_option(self, option: str) -> None:
        await self._evse.set_charging_current(option)

    async def async_update(self):
        """Reload state of the charger"""
        await self._evse.refresh()
        self._attr_current_option = self._evse.status.current
