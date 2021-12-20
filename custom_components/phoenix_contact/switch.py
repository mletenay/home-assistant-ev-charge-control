"""Phoenix Contact's Electric Vehicle Charge Control switch."""
from __future__ import annotations

from .const import DOMAIN, KEY_COORDINATOR, KEY_EVSE, KEY_DEVICE_INFO
from .ev_charge_control import EvChargeControl

from homeassistant.helpers.entity import ToggleEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the vehicle charger switch entities from a config entry."""
    evse = hass.data[DOMAIN][config_entry.entry_id][KEY_EVSE]
    coordinator = hass.data[DOMAIN][config_entry.entry_id][KEY_COORDINATOR]
    device_info = hass.data[DOMAIN][config_entry.entry_id][KEY_DEVICE_INFO]

    async_add_entities([EvChargeControlEntity(coordinator, device_info, evse)])

    return True


class EvChargeControlEntity(CoordinatorEntity, ToggleEntity):
    """Representation of an Electric Vehicle Charge Control device."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device_info: DeviceInfo,
        evse: EvChargeControl,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._attr_name = "EV Charge Control"
        self._attr_icon = "mdi:car-electric"
        self._attr_unique_id = f"{DOMAIN}-{evse.status.serial}"
        self._attr_device_info = device_info
        self._evse = evse

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        return self.coordinator.data.charging_enabled

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
            "Vehicle status": self._evse.status.status_name(),
            "Charging duration": self._evse.status.duration,
            "Charging current": self._evse.status.current + " A",
        }
        return data
