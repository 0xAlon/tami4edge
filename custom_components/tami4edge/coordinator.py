"""Coordinator for Tami4Edge."""

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

import logging
from .const import (WATER_QUALITY_INTERVAL, WATER_CONSUMPTION_INTERVAL)

_LOGGER = logging.getLogger(__name__)


class WaterQualityCoordinator(DataUpdateCoordinator):
    """Water quality coordinator."""

    def __init__(self, hass: HomeAssistant, api) -> None:
        """Initialize the water quality coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="water quality coordinator",
            update_interval=WATER_QUALITY_INTERVAL,
        )
        self.api = api

    async def _async_update_data(self) -> dict:
        """Fetch data from the API endpoint."""

        try:
            water_quality = await self.api.client.water_quality()
            return {
                "filter": water_quality['filterInfo']['upcomingReplacement'],
                "uv": water_quality['uvInfo']['upcomingReplacement'],
            }
        except Exception as exceptioe:
            raise UpdateFailed(f"Error communicating with API: {exceptioe}") from exceptioe


class WaterConsumptionCoordinator(DataUpdateCoordinator):
    """Water consumption coordinator."""

    def __init__(self, hass: HomeAssistant, api) -> None:
        """Initialize the water consumption coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="water consumption coordinator",
            update_interval=WATER_CONSUMPTION_INTERVAL,
        )
        self.api = api

    async def _async_update_data(self) -> dict:
        """Fetch data from the API endpoint."""
        try:
            water_consumption = await self.api.client.water_consumption()
            return {
                "daily": round(list(water_consumption['deviceStatistics'].items())[-1][1] / 1000, 3),
                "avg": round((sum(water_consumption['deviceStatistics'].values()) / 1000) / 7, 3),
                "weekly": round(sum(water_consumption['deviceStatistics'].values()) / 1000, 3),
            }
        except Exception as exceptioe:
            raise UpdateFailed(f"Error communicating with API: {exceptioe}") from exceptioe
