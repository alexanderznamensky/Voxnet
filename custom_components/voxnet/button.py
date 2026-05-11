"""Button platform for Voxnet."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VoxnetBalanceCoordinator


BUTTON_DESCRIPTION = ButtonEntityDescription(
    key="refresh",
    translation_key="refresh",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Voxnet Balance button."""
    coordinator: VoxnetBalanceCoordinator = entry.runtime_data
    async_add_entities([VoxnetRefreshButton(coordinator, entry)])


class VoxnetRefreshButton(CoordinatorEntity[VoxnetBalanceCoordinator], ButtonEntity):
    """Button to manually refresh Voxnet balance."""

    entity_description = BUTTON_DESCRIPTION
    _attr_has_entity_name = True

    def __init__(self, coordinator: VoxnetBalanceCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_refresh"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.async_request_refresh()

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title,
            "manufacturer": "Voxnet",
        }
