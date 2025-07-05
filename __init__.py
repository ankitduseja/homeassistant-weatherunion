
"""The WeatherUnion component."""

from __future__ import annotations

from dataclasses import dataclass
import logging



from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import WeatherUnionDataUpdateCoordinator
from .api import WeatherUnionApiClient
from .sensor import async_setup_entry as sensor_async_setup_entry

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # _LOGGER.debug("Using latitude: %s", entry.latitude)
    # _LOGGER.debug("Using longitude: %s", entry.longitude)

    api_key = entry.data["api_key"]
    location_name = entry.data["location_name"]
    latitude = entry.data["latitude"]
    longitude = entry.data["longitude"]
    
    api_client = WeatherUnionApiClient(hass, api_key, latitude, longitude, location_name)
    coordinator = WeatherUnionDataUpdateCoordinator(hass, api_client)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True

