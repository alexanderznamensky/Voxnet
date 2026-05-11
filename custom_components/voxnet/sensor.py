"""Sensor platform for Voxnet."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VoxnetBalanceCoordinator


SENSOR_DESCRIPTION = SensorEntityDescription(
    key="balance",
    translation_key="balance",
    native_unit_of_measurement="RUB",
    device_class=SensorDeviceClass.MONETARY,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Voxnet Balance sensor."""
    coordinator: VoxnetBalanceCoordinator = entry.runtime_data
    async_add_entities([VoxnetBalanceSensor(coordinator, entry)])


class VoxnetBalanceSensor(CoordinatorEntity[VoxnetBalanceCoordinator], SensorEntity):
    """Voxnet balance sensor."""

    entity_description = SENSOR_DESCRIPTION
    _attr_has_entity_name = True

    def __init__(self, coordinator: VoxnetBalanceCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_balance"

    @property
    def native_value(self) -> float | None:
        """Return the balance."""
        return self.coordinator.data

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title,
            "manufacturer": "Voxnet",
        }
