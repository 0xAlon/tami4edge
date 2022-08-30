"""Sensor platform for Tami4edge."""

import logging
import datetime
from re import T

from .API import Tami4EdgeApi

from .coordinator import WaterQualityCoordinator, WaterConsumptionCoordinator

from homeassistant.core import callback

from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorEntity,
    SensorEntityDescription,
)

from homeassistant.const import TIME_DAYS, VOLUME_LITERS

from .const import DOMAIN_DATA, WATER_ICON, CALENDAR_ICON

_LOGGER = logging.getLogger(__name__)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

ENTITY_DESCRIPTIONS = [
    SensorEntityDescription(
        key="uv",
        name="UV Upcoming Replacement",
        icon=CALENDAR_ICON,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_of_measurement=TIME_DAYS,
    ),
    SensorEntityDescription(
        key="filter",
        name="Filter Upcoming Replacement",
        icon=CALENDAR_ICON,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_of_measurement=TIME_DAYS,
    ),

    SensorEntityDescription(
        key="daily",
        name="Daily Water Consumption",
        icon=WATER_ICON,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_of_measurement=VOLUME_LITERS,
    ),

    SensorEntityDescription(
        key="weekly",
        name="Weekly Water Consumption",
        icon=WATER_ICON,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_of_measurement=VOLUME_LITERS,
    ),
    SensorEntityDescription(
        key="avg",
        name="Average Water Consumption",
        icon=WATER_ICON,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_of_measurement=VOLUME_LITERS,
    ),
]


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup sensor platform."""

    api = hass.data[DOMAIN_DATA]["handler"]

    try:
        waterQualityCoordinator = WaterQualityCoordinator(hass, api)
        waterConsumptionCoordinator = WaterConsumptionCoordinator(hass, api)

        entities = []
        for entity_description in ENTITY_DESCRIPTIONS:
            if entity_description.unit_of_measurement == TIME_DAYS:
                entities.append(
                    WaterQualityEntity(
                        coordinator=waterQualityCoordinator,
                        api=api,
                        entity_description=entity_description,
                    )
                )
            elif entity_description.unit_of_measurement == VOLUME_LITERS:
                entities.append(
                    WaterConsumptionEntity(
                        coordinator=waterConsumptionCoordinator,
                        api=api,
                        entity_description=entity_description,
                    )
                )
        hass.data[DOMAIN_DATA]["waterConsumptionCoordinator"] = waterConsumptionCoordinator
        async_add_entities(entities)
        await waterQualityCoordinator.async_config_entry_first_refresh()
        await waterConsumptionCoordinator.async_config_entry_first_refresh()
    except Exception as exception:
        _LOGGER.exception("Fail to setup tami4edge platform")
        raise exception


class WaterQualityEntity(CoordinatorEntity, SensorEntity):
    """Representation of the entity."""

    def __init__(
            self,
            coordinator: DataUpdateCoordinator,
            api: Tami4EdgeApi,
            entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the entity."""
        CoordinatorEntity.__init__(self, coordinator)
        self.entity_description = entity_description
        self._state = None
        self.api = api
        self._attr_unique_id = f"tami4edge_{self.entity_description.key}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        try:
            timestamp = datetime.datetime.fromtimestamp(
                int(str(self.coordinator.data[self.entity_description.key])[0:10]))
            today = datetime.datetime.now()
            delta = timestamp - today
            self._attr_native_value = delta.days
        except KeyError:
            return
        self.async_write_ha_state()


class WaterConsumptionEntity(CoordinatorEntity, SensorEntity):
    """Representation of the entity."""

    def __init__(
            self,
            coordinator: DataUpdateCoordinator,
            api: Tami4EdgeApi,
            entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the entity."""
        CoordinatorEntity.__init__(self, coordinator)
        self.entity_description = entity_description
        self._state = None
        self.api = api
        self._attr_unique_id = f"tami4edge_{self.entity_description.key}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        try:
            self._attr_native_value = self.coordinator.data[self.entity_description.key]
        except KeyError:
            return
        self.async_write_ha_state()
