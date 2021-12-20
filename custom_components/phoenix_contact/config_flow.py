"""Config flow to configure Goodwe inverters using their local API."""
from __future__ import annotations

import logging
import voluptuous as vol

from .ev_charge_control import EvChargeControl

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DEFAULT_NAME,
    DOMAIN,
)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
    }
)

_LOGGER = logging.getLogger(__name__)


class GoodweFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Goodwe config flow."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            host = user_input[CONF_HOST]

            try:
                evse = EvChargeControl(host)
                await evse.refresh()
            except Exception:
                errors["base"] = "connection_error"
            else:
                await self.async_set_unique_id(evse.status.serial)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=DEFAULT_NAME,
                    data={
                        CONF_HOST: host,
                    },
                )

        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )
