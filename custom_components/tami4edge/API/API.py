"""Tami4edge API client"""
import asyncio
import logging
from json import JSONDecodeError
import aiohttp

_LOGGER = logging.getLogger(__name__)


class Tami4EdgeApiError(Exception):
    pass


class Tami4EdgeApi:

    def __init__(self, websession, token=None):

        self.base_url = 'https://swelcustomers.strauss-water.com'

        self.header = {'Host': 'swelcustomers.strauss-water.com',
                       'Accept': 'application/json, text/plain, */*',
                       'Connection': 'keep-alive',
                       'Accept-Language': 'en-us',
                       'User-Agent': 'tami4edge/81 CFNetwork/1333.0.4 Darwin/21.5.0',
                       'Content-Type': 'application/json'
                       }

        self.token = token
        self._session = websession
        self.id = None

    async def _send_post_request(self, data=None, api=None) -> dict:
        try:
            resp = await self._session.post(
                url=self.base_url + api,
                data=data,
                headers=self.header,
            )
            json_resp = await resp.json(content_type=None)
        except asyncio.TimeoutError:
            raise Tami4EdgeApiError(
                "Failed to communicate with API due to time out"
            )
        except aiohttp.ClientError as ex:
            raise Tami4EdgeApiError(
                f"Failed to communicate with API due to ClientError ({str(ex)})"
            )
        except JSONDecodeError as ex:
            raise Tami4EdgeApiError(
                f"Recieved invalid response from API: {str(ex)}"
            )

        return json_resp

    async def _send_get_request(self, api=None) -> dict:
        try:
            resp = await self._session.get(
                url=self.base_url + api,
                headers=self.header,
            )
            json_resp = await resp.json(content_type=None)
        except asyncio.TimeoutError:
            raise Tami4EdgeApiError(
                "Failed to communicate with API due to time out"
            )
            pass
        except aiohttp.ClientError as ex:
            raise Tami4EdgeApiError(
                f"Failed to communicate with API due to ClientError ({str(ex)})"
            )
        except JSONDecodeError as ex:
            raise Tami4EdgeApiError(
                f"Recieved invalid response from API: {str(ex)}"
            )

        return json_resp

    async def refresh_token(self, now=None):
        data = '{\"token\":\"' + self.token + '\"}'
        response = await self._send_post_request(data=data, api='/public/token/refresh')
        self.header['Authorization'] = 'Bearer' + response['access_token']

    async def boile_water(self):
        response = await self._send_post_request(api=f'/api/v1/device/{self.id}/startBoiling')
        return response

    async def water_consumption(self):
        response = await self._send_get_request(api='/api/v2/customer/myConsumption')
        return response

    async def water_quality(self):
        response = await self._send_get_request(api='/api/v2/customer/waterQuality')
        return response

    async def get_device(self):
        response = await self._send_get_request(api='/api/v1/device')
        self.id = response[0]['id']
        return response
