from homeassistant.helpers.entity import Entity
from .const import DOMAIN
from slugify import slugify

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    sensors = [
        WeatherUnionSensor(coordinator, "temperature", "Temperature", "°C"),
        WeatherUnionSensor(coordinator, "humidity", "Humidity", "%"),
        WeatherUnionSensor(coordinator, "wind_speed", "Wind Speed", "m/s"),
        WeatherUnionSensor(coordinator, "wind_direction", "Wind Direction", "°"),
        WeatherUnionSensor(coordinator, "rain_intensity", "Rain Intensity", "mm/h"),
        WeatherUnionSensor(coordinator, "rain_accumulation", "Rain Accumulation", "mm")
    ]
    async_add_entities(sensors, True)

class WeatherUnionSensor(Entity):
    
    def __init__(self, coordinator, sensor_type, name, unit_of_measurement):
        slug=slugify(coordinator.api_client.location_name).replace("-", "_")
        self.coordinator = coordinator
        self._sensor_type = sensor_type
        self._name = f"Weather Union {coordinator.api_client.location_name} {name}"
        self._unit_of_measurement = unit_of_measurement
        self._state = None
        self._unique_id = f"weatherunion_{slug}_{sensor_type}"

    # @callback
    # def _handle_coordinator_update(self) -> None:
    #     """Handle updated data from the coordinator."""
    #     self._attr_is_on = self.api_client.data["state"]
    #     self.async_write_ha_state()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self.coordinator.data["locality_weather_data"].get(self._sensor_type)

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def unique_id(self):
        return self._unique_id
    
    @property
    def should_poll(self):
        return False

    @property
    def available(self):
        return self.coordinator.last_update_success

    # async def async_update(self):
    #     data = await self.api_client.async_get_weather_data()
    #     self._state = data["locality_weather_data"].get(self._sensor_type)

    async def async_added_to_hass(self):
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))
    
    async def async_update(self):
        await self.coordinator.async_request_refresh()
