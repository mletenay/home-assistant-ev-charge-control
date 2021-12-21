"""Phoenix Contact's Electric Vehicle Charge Current Select."""
from __future__ import annotations

from .const import DOMAIN, KEY_COORDINATOR, KEY_EVSE, KEY_DEVICE_INFO
from .ev_charge_control import EvChargeControl

from homeassistant.components.sensor import SensorEntity
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

    async_add_entities(
        [
            EvChargeStatusEntity(coordinator, device_info, evse),
            EvChargeDurationEntity(coordinator, device_info, evse),
        ]
    )


class EvChargeStatusEntity(CoordinatorEntity, SensorEntity):
    """Representation of an Electric Vehicle Charge Control device."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device_info: DeviceInfo,
        evse: EvChargeControl,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._attr_name = "EV Charge Status"
        self._attr_icon = "mdi:car-electric"
        self._attr_unique_id = f"{DOMAIN}-status-{evse.status.serial}"
        self._attr_device_info = device_info
        self._evse = evse

    @property
    def native_value(self):
        """Return the value reported by the sensor."""
        return self.coordinator.data.status_name()


class EvChargeDurationEntity(CoordinatorEntity, SensorEntity):
    """Representation of an Electric Vehicle Charge Control device."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device_info: DeviceInfo,
        evse: EvChargeControl,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._attr_name = "EV Charge Duration"
        self._attr_icon = "mdi:car-electric"
        self._attr_unique_id = f"{DOMAIN}-duration-{evse.status.serial}"
        self._attr_device_info = device_info
        self._evse = evse

    @property
    def native_value(self):
        """Return the value reported by the sensor."""
        return self.coordinator.data.duration
