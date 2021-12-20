"""Phoenix Contact's Electric Vehicle Charge Current Select."""

from .const import DOMAIN, KEY_EVSE, KEY_DEVICE_INFO
from .ev_charge_control import EvChargeControl

from homeassistant.const import ELECTRIC_CURRENT_AMPERE
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import DeviceInfo


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the vehicle charger select entities from a config entry."""
    evse = hass.data[DOMAIN][config_entry.entry_id][KEY_EVSE]
    device_info = hass.data[DOMAIN][config_entry.entry_id][KEY_DEVICE_INFO]

    async_add_entities([EvChargeCurrentEntity(device_info, evse)])

    return True


class EvChargeCurrentEntity(SelectEntity):
    """Representation of an Electric Vehicle Charge Control device."""

    def __init__(
        self,
        device_info: DeviceInfo,
        evse: EvChargeControl,
    ) -> None:
        """Initialize the entity."""
        self._attr_name = "EV Charge Current"
        self._attr_icon = "mdi:car-electric"
        self._attr_unique_id = f"{DOMAIN}-{evse.status.serial}"
        self._attr_device_info = device_info
        self._attr_unit_of_measurement = ELECTRIC_CURRENT_AMPERE
        self._attr_options = evse.status.current_options
        self._attr_current_option = evse.status.current
        self._evse = evse

    async def async_select_option(self, option: str) -> None:
        await self._evse.set_charging_current(option)

    async def async_update(self):
        """Reload state of the charger"""
        await self._evse.refresh()
        self._attr_current_option = self._evse.status.current
