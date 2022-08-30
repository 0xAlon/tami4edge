"""Button platform for Tami4edge."""

import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN_DATA, KETTLE_ICON, SYNC_ICON

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup button platform."""

    sensors = []

    waterConsumptionCoordinator = hass.data[DOMAIN_DATA]['waterConsumptionCoordinator']

    sensors.append(BoileWater(hass, "Boil Water"))
    sensors.append(SyncSensors(hass, waterConsumptionCoordinator, "Sync"))

    async_add_entities(sensors, True)


class BoileWater(ButtonEntity):
    """boil button."""

    def __init__(self, hass, name):
        self.hass = hass
        self.handler = self.hass.data[DOMAIN_DATA]["handler"]
        self._name = name
        self._state = None
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_unique_id = "tami4edge_boil_water"

    async def async_press(self) -> None:
        """Press the button."""
        x = await self.handler.client.boile_water()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        return KETTLE_ICON


class SyncSensors(ButtonEntity):
    """Manually update sensors."""

    def __init__(self, hass, waterConsumptionCoordinator, name):
        self.hass = hass
        self.handler = self.hass.data[DOMAIN_DATA]["handler"]
        self._name = name
        self._state = None
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_unique_id = "tami4edge_sync_data"
        self.waterConsumptionCoordinator = waterConsumptionCoordinator

    async def async_press(self) -> None:
        """Press the button."""
        await self.waterConsumptionCoordinator.async_request_refresh()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        return SYNC_ICON
