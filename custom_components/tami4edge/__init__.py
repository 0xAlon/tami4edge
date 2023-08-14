"""
Component to integrate with Tami4edge.

For more details about this component, please refer to
https://github.com/0xAlon
"""

import logging

from homeassistant.core import ServiceResponse, SupportsResponse
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers import discovery
from .API import Tami4EdgeApi
from .const import (
    DOMAIN,
    DOMAIN_DATA,
    PLATFORMS,
    TOKEN_SCAN_INTERVAL
)

from homeassistant.const import CONF_API_KEY

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

    await client.get_device()

    # Load platforms
    for domain in PLATFORMS:
        hass.async_create_task(
            discovery.async_load_platform(hass, domain, DOMAIN, {}, config)

        )

    # Service Functions
    async def handle_prepare_drink(call):
        drink = call.data.get('drink_id')
        x = await handler.client.prepare_drink(drink_id=drink)

    async def handle_fetch_drinks(call) -> ServiceResponse:
        return await handler.client.drinks()

    async def handle_boile_water(self):
        return await handler.client.boile_water()
    
    # Init Services
    hass.services.async_register(DOMAIN, "boile_water", handle_boile_water)
    hass.services.async_register(DOMAIN, "prepare_drink", handle_prepare_drink)
    hass.services.async_register(DOMAIN, "fetch_drinks", handle_fetch_drinks, supports_response=SupportsResponse.ONLY)

    async_track_time_interval(hass, client.refresh_token, TOKEN_SCAN_INTERVAL)  # Auto Update token

    return True


class Tami4EdgeHandler:
    """This class handle communication with the API."""

    def __init__(self, hass, client):
        """Initialize the class."""
        self.hass = hass
        self.client = client
