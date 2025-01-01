"""Example integration using DataUpdateCoordinator."""
import requests
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession


import logging

import async_timeout

class WeatherUnionApiClient:
    """Coordinator"""
    def __init__(self, hass: HomeAssistant, api_key: str, latitude: str, longitude: str, location_name: str):
        # super().__init__(
        #     hass,
        #     _LOGGER,
        #     # Name of the data. For logging purposes.
        #     name="Weather Union Data",
        #     # Polling interval. Will only be polled if there are subscribers.
        #     update_interval=timedelta(minutes=5),
        # )
        self.hass = hass
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.location_name = location_name
        self.base_url = "https://www.weatherunion.com/gw/weather/external/v0/get_weather_data"

    def _get_weather_data(self):
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude
        }
        headers = {'x-zomato-api-key': self.api_key}
        try:
            # async with async_timeout.timeout(10):
            response = requests.get(self.base_url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except ApiAuthError as err:
            # Raising ConfigEntryAuthFailed will cancel future updates
            # and start a config flow with SOURCE_REAUTH (async_step_reauth)
            raise ConfigEntryAuthFailed from err
        except ApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    async def async_get_weather_data(self):
        return await self.hass.async_add_executor_job(self._get_weather_data)

    # async def _async_update_data(self):
    #     """Fetch data from API endpoint.

    #     This is the place to pre-process the data to lookup tables
    #     so entities can quickly look up their data.
    #     """
    #     try:
    #         # Note: asyncio.TimeoutError and aiohttp.ClientError are already
    #         # handled by the data update coordinator.
    #         async with async_timeout.timeout(10):
    #             # Grab active context variables to limit data required to be fetched from API
    #             # Note: using context is not required if there is no need or ability to limit
    #             # data retrieved from API.


    #             listening_idx = set(self.async_contexts())
    #             return await self.my_api.fetch_data(listening_idx)

