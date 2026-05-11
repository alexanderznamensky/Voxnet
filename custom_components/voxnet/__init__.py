"""Voxnet integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import VoxnetClient
from .const import CONF_LOGIN, CONF_PASSWORD, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN, PLATFORMS
from .coordinator import VoxnetBalanceCoordinator



async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate old config entries."""
    if entry.version == 1:
        data = dict(entry.data)
        options = dict(entry.options)

        # In versions <= 1.1.0 scan_interval was stored in seconds.
        # From config flow version 2 it is stored in minutes.
        for target in (data, options):
            if CONF_SCAN_INTERVAL in target:
                old_value = int(target[CONF_SCAN_INTERVAL])
                if old_value >= 60:
                    target[CONF_SCAN_INTERVAL] = max(1, old_value // 60)

        hass.config_entries.async_update_entry(
            entry,
            data=data,
            options=options,
            version=2,
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Voxnet Balance from a config entry."""
    login = entry.data[CONF_LOGIN]
    password = entry.data[CONF_PASSWORD]
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))

    client = VoxnetClient(login, password)
    coordinator = VoxnetBalanceCoordinator(hass, client, entry, int(scan_interval))

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    entry.async_on_unload(entry.add_update_listener(async_update_options))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload entry when options are changed."""
    await hass.config_entries.async_reload(entry.entry_id)
