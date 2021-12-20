"""Support for Electric Vehicle Charge Control (EM-CP-PP-ETH device by Phoenix Contact)"""

import voluptuous as vol


from .const import DOMAIN, KEY_DEVICE_INFO, KEY_EVSE, PLATFORMS
from .ev_charge_control import EvChargeControl
from .switch import EvChargeControlEntity
from .select import EvChargeCurrentEntity

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers import config_validation as cv

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Phoenix Contact components from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    host = entry.data[CONF_HOST]

    # Connect to vehicle charger
    try:
        evse = EvChargeControl(host)
        await evse.refresh()
    except Exception as err:
        raise ConfigEntryNotReady from err

    device_info = DeviceInfo(
        configuration_url=evse.url_root,
        identifiers={(DOMAIN, evse.status.serial)},
        name=entry.title,
        manufacturer="Phoenix Contact",
    )

    hass.data[DOMAIN][entry.entry_id] = {
        KEY_EVSE: evse,
        KEY_DEVICE_INFO: device_info,
    }

    entry.async_on_unload(entry.add_update_listener(update_listener))

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


async def update_listener(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)
