"""Sensor platform for Tami4edge."""

from cgitb import handler
import logging
import datetime
from . import Tami4edgeSensor

from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorEntity,
)
from homeassistant.const import (
    DEVICE_CLASS_DATE,
    TIME_DAYS,
    VOLUME_LITERS,
)

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None): 
    """Setup sensor platform."""
    sensors = []

    filter_coordinator = hass.data[DOMAIN]["coordinator"]


    sensors.append(WaterConsumption(hass,"Average Daily Usage","avg"))
    sensors.append(WaterConsumption(hass,"Daily usage","day"))
    sensors.append(WaterConsumption(hass,"Weekly Usage","week"))

    async_add_entities([FilterReplacment(filter_coordinator, "WATER_FILTER", "Water Filter")], True)
    async_add_entities([FilterReplacment(filter_coordinator, "UV", "UV Filter")], True)

    async_add_entities(sensors, True)




class FilterReplacment(CoordinatorEntity,SensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, id, name):
        super().__init__(coordinator)
        self._state = -1
        self._id = id
        self._name = name

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return "mdi:nintendo-switch"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        value = self.coordinator.data.values()


        if self._id == "WATER_FILTER":
            try:
                value = list(value)[0]['upcomingReplacement']
            except KeyError:
                pass
        elif self._id == "UV":
            try:
                value = list(value)[1]['upcomingReplacement']
            except KeyError:
                pass
        
            
        timestamp = datetime.datetime.fromtimestamp(int(str(value)[0:10]))
        today = datetime.datetime.now()
        delta = timestamp - today
        self._state = delta.days

        return self._state

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return DEVICE_CLASS_DATE

    @property
    def state_class(self):
        """Return the state class of the sensor."""
        return STATE_CLASS_MEASUREMENT

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TIME_DAYS

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return 'mdi:water-opacity'

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return f"{DOMAIN}_{self._id}"


class WaterConsumption(Tami4edgeSensor, SensorEntity):
    """WaterConsumption Sensor class."""

    def __init__(self, hass, name , id):
        super().__init__(hass, name, id)
        self.id = id

    async def async_update(self):
        """Update the sensor."""
        data = await self.handler.client.water_consumption()

        if self.id == "day":
            self._state = round(list(data['deviceStatistics'].items())[-1][1] / 1000,3)
        elif self.id == "avg":
            self._state = round((sum(data['deviceStatistics'].values()) / 1000) / 7,3)
        elif self.id == "week":
            self._state = round(sum(data['deviceStatistics'].values()) / 1000,3)

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return DEVICE_CLASS_DATE

    @property
    def state_class(self):
        """Return the state class of the sensor."""
        return STATE_CLASS_MEASUREMENT

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return VOLUME_LITERS