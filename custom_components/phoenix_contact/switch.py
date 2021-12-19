"""Phoenix Contact's Electric Vehicle Charge Control switch."""
from homeassistant.helpers.entity import ToggleEntity

from homeassistant.const import CONF_IP_ADDRESS
from .const import DOMAIN
from .ev_charge_control import EvChargeControl


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Expose Electric Vehicle charge control via statemachine and services."""
    evse = EvChargeControl(config[CONF_IP_ADDRESS])
    await evse.refresh()
    async_add_entities([EvChargeControlEntity(evse)])
    return True


class EvChargeControlEntity(ToggleEntity):
    """Representation of an Electric Vehicle Charge Control device."""

    def __init__(self, evse):
        """Initialize the sensor."""
        self._evse = evse
        self._attr_name = "EV Charge Control"
        self._attr_icon = "mdi:car-electric"
        self._attr_is_on = evse.status.charging_enabled
        self._attr_unique_id = f"{DOMAIN}-{evse.status.serial}"

    async def async_turn_on(self, **kwargs):
        """Enable vehicle charging"""
        self._attr_is_on = await self._evse.set_charging_enabled(True)

    async def async_turn_off(self, **kwargs):
        """Disable vehicle charging"""
        self._attr_is_on = await self._evse.set_charging_enabled(False)

    @property
    def extra_state_attributes(self):
        """Return the charger state attributes."""
        data = {
            "Vehicle status": self._evse.get_vehicle_status(),
            "Charging duration": self._evse.status.duration,
            "Charging current": self._evse.status.current + " A",
        }
        return data

    async def async_update(self):
        """Reload state of the charger"""
        await self._evse.refresh()
