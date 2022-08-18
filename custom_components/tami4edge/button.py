"""Button platform for Tami4edge."""

import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import EntityCategory
from . import Tami4edgeButton
_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None): 
    """Setup button platform."""
    sensors = []
    sensors.append(BoileWater(hass,"Boil Water","boil"))
    async_add_entities(sensors, True)


class BoileWater(ButtonEntity, Tami4edgeButton):
    """boil button."""
    def __init__(self, hass, name, id):
        super().__init__(hass, name, id)
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_name = name


    async def async_press(self) -> None:
        """Press the button."""
        x = await self.handler.client.boile_water()
