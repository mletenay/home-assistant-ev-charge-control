"""Phoenix Contact's Electric Vehicle Charge Control switch."""
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.helpers import config_validation as cv, entity_platform
from homeassistant.helpers.entity import ToggleEntity

from .ev_charge_control import EvChargeControl

DOMAIN = "phoenix_contact"

SERVICE_SET_CHARGING_CURRENT = "set_charging_current"
SERVICE_ENABLE_CHARGING = "enable_charging"
SERVICE_DISABLE_CHARGING = "disable_charging"
ATTR_CURRENT = "current"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({vol.Required(CONF_IP_ADDRESS): cv.string,})


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Expose Electric Vehicle charge control via statemachine and services."""
    evse = EvChargeControl(config[CONF_IP_ADDRESS])
    await evse.refresh()
    async_add_entities([EvChargeControlEntity(evse)])

    platform = entity_platform.current_platform.get()
    platform.async_register_entity_service(
        SERVICE_SET_CHARGING_CURRENT,
        {vol.Required(ATTR_CURRENT): cv.string},
        "async_set_charging_current",
    )
    platform.async_register_entity_service(
        SERVICE_ENABLE_CHARGING, {}, "async_enable_charging",
    )
    platform.async_register_entity_service(
        SERVICE_DISABLE_CHARGING, {}, "async_disable_charging",
    )

    return True


class EvChargeControlEntity(ToggleEntity):
    """Representation of an Electric Vehicle Charge Control device."""

    def __init__(self, evse):
        """Initialize the sensor."""
        self._evse = evse
        self._is_on = evse.status.charging_enabled
        self._uid = DOMAIN + "-" + evse.status.serial

    async def async_set_charging_current(self, current: str):
        """Set the charging current."""
        await self._evse.set_charging_current(current)

    async def async_enable_charging(self):
        """Enable charging."""
        await self._evse.set_charging_enabled(True)

    async def async_disable_charging(self):
        """Disable charging"""
        await self._evse.set_charging_enabled(False)

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._uid

    @property
    def name(self):
        """Return the name of the sensor."""
        return "EV Charge Control"

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return "mdi:car-electric"

    @property
    def is_on(self):
        """Return True if entity is on."""
        return self._is_on

    @property
    def current(self):
        """Return the current speed."""
        return self._evse.status.current

    @property
    def current_list(self):
        """Get the list of available currents."""
        return self._evse.status.current_options

    async def async_turn_on(self, **kwargs):
        """Enable vehicle charging"""
        self._is_on = await self._evse.set_charging_enabled(True)

    async def async_turn_off(self, **kwargs):
        """Disable vehicle charging"""
        self._is_on = await self._evse.set_charging_enabled(False)

    @property
    def device_state_attributes(self):
        """Return the charger state attributes."""
        data = {
            "Vehicle status": self._evse.get_vehicle_status(),
            "Charging duration": self._evse.status.duration,
            "Charging current": self._evse.status.current + " A",
        }
        return data

    @property
    def capability_attributes(self):
        """Return capability attributes."""
        return {"Current options": self.current_list}

    async def async_update(self):
        """Reload state of the charger"""
        await self._evse.refresh()
