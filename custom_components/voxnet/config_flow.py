"""Config flow for Voxnet."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .api import VoxnetApiError, VoxnetClient
from .const import CONF_ACCOUNT_NAME, CONF_LOGIN, CONF_PASSWORD, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN, MIN_SCAN_INTERVAL


class VoxnetBalanceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Voxnet."""

    VERSION = 2

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            login = user_input[CONF_LOGIN].strip()
            password = user_input[CONF_PASSWORD]
            account_name = user_input.get(CONF_ACCOUNT_NAME, "").strip() or login
            scan_interval = int(user_input[CONF_SCAN_INTERVAL])

            await self.async_set_unique_id(login.lower())
            self._abort_if_unique_id_configured()

            client = VoxnetClient(login, password)
            try:
                await self.hass.async_add_executor_job(client.get_balance)
            except VoxnetApiError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"Voxnet {account_name}",
                    data={
                        CONF_LOGIN: login,
                        CONF_PASSWORD: password,
                        CONF_ACCOUNT_NAME: account_name,
                        CONF_SCAN_INTERVAL: scan_interval,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_LOGIN): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Optional(CONF_ACCOUNT_NAME): str,
                    vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
                        vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL)
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Create the options flow."""
        return VoxnetBalanceOptionsFlow()


class VoxnetBalanceOptionsFlow(config_entries.OptionsFlow):
    """Handle Voxnet Balance options."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SCAN_INTERVAL, default=current_interval): vol.All(
                        vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL)
                    ),
                }
            ),
        )
