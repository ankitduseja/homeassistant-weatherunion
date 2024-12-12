from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
import logging

from .api import WeatherUnionApiClient

_LOGGER = logging.getLogger(__name__)

class WeatherUnionDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api_client: WeatherUnionApiClient):
        self.api_client = api_client
        update_interval = timedelta(minutes=5)
        
        super().__init__(
            hass,
            _LOGGER,
            name="Weather Union Data Update Coordinator",
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        try:
            return await self.api_client.async_get_weather_data()
        except Exception as e:
            raise UpdateFailed(f"Error fetching data: {e}")
