"""Phoenix Contact's Electric Vehicle Charge Current Select."""
from __future__ import annotations

from .const import DOMAIN, KEY_COORDINATOR, KEY_EVSE, KEY_DEVICE_INFO
from .ev_charge_control import EvChargeControl

from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the vehicle charger select entities from a config entry."""
    evse = hass.data[DOMAIN][config_entry.entry_id][KEY_EVSE]
    coordinator = hass.data[DOMAIN][config_entry.entry_id][KEY_COORDINATOR]
    device_info = hass.data[DOMAIN][config_entry.entry_id][KEY_DEVICE_INFO]

    async_add_entities([EvChargeCurrentEntity(coordinator, device_info, evse)])


class EvChargeCurrentEntity(CoordinatorEntity, SelectEntity):
    """Representation of an Electric Vehicle Charger charging current entity."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device_info: DeviceInfo,
        evse: EvChargeControl,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._attr_name = "EV Charging Current"
        self._attr_icon = "mdi:car-electric"
        self._attr_unique_id = f"{DOMAIN}-{evse.status.serial}"
        self._attr_device_info = device_info
        self._evse = evse

    @property
    def options(self) -> list[str]:
        """Return a set of selectable options."""
        return list(map(lambda x: x + " A", self.coordinator.data.current_options))

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        return self.coordinator.data.current + " A"

    async def async_select_option(self, option: str) -> None:
        await self._evse.set_charging_current(option)
        self.async_write_ha_state()
