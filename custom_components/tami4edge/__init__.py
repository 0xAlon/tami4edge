"""
Component to integrate with Tami4edge.

For more details about this component, please refer to
https://github.com/0xAlon
"""

import logging
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity
from .API import Tami4EdgeApi 

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta

from .const import (
    DEFAULT_ICON,
    DOMAIN,
    DOMAIN_DATA,
    PLATFORMS,
    BUTTON_ICON,
    TOKEN_SCAN_INTERVAL
)


from homeassistant.const import (

    CONF_API_KEY,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_API_KEY): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Set up this component using YAML."""
    if config.get(DOMAIN) is None:
        # We get here if the integration is set up using config flow
        return True

    # Create DATA dict
    hass.data[DOMAIN_DATA] = {}

    # Get API key 
    api_key = config[DOMAIN].get(CONF_API_KEY)

    # Configure the client.
    websession = async_get_clientsession(hass)
    client = Tami4EdgeApi(websession, api_key)
    await client.refresh_token()


    handler = Tami4EdgeHandler(hass, client)
    hass.data[DOMAIN_DATA]["handler"] = handler
    

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name=DOMAIN,
        update_method=client.water_quality,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(hours=1),
    )
    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()
    hass.data[DOMAIN] = {
        "coordinator": coordinator,
    }

    # Load platforms
    for domain in PLATFORMS:
        hass.async_create_task(
            discovery.async_load_platform(hass, domain, DOMAIN, {}, config)
           
        )

    async_track_time_interval(hass, client.refresh_token, TOKEN_SCAN_INTERVAL) # Auto Update token  

    return True


class Tami4EdgeHandler:
    """This class handle communication with the API."""
    def __init__(self, hass, client):
        """Initialize the class."""
        self.hass = hass
        self.client = client
        
        
class Tami4edgeSensor(Entity):
    """Tami4edgeSensor Entity class."""

    def __init__(self, hass, name, id):
        self.hass = hass
        self.id = id
        self.handler = self.hass.data[DOMAIN_DATA]["handler"]
        self._name = name
        self._state = None

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
        return DEFAULT_ICON

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return f"{DOMAIN}_{self.id}"



class Tami4edgeButton(Entity):
    """Tami4edgeButton Entity class."""

    def __init__(self, hass, name, id):
        self.hass = hass
        self.id = id
        self.handler = self.hass.data[DOMAIN_DATA]["handler"]
        self._name = name
        self._state = None

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
        return BUTTON_ICON

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return f"{DOMAIN}_{self.id}"