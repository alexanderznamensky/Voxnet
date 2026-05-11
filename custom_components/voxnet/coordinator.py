"""DataUpdateCoordinator for Voxnet."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import VoxnetApiError, VoxnetClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class VoxnetBalanceCoordinator(DataUpdateCoordinator[float]):
    """Coordinator for Voxnet balance polling."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: VoxnetClient,
        entry: ConfigEntry,
        scan_interval: int,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=scan_interval),
            config_entry=entry,
        )
        self.client = client

    async def _async_update_data(self) -> float:
        """Fetch data from Voxnet."""
        try:
            return await self.hass.async_add_executor_job(self.client.get_balance)
        except VoxnetApiError as err:
            raise UpdateFailed(str(err)) from err
