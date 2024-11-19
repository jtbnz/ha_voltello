from datetime import timedelta
import logging
from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.const import CONF_NAME

from .const import DOMAIN, SENSOR_TYPES
from .utils import get_service_points_list, get_live_data, get_displayed_data

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = VoltelloCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(VoltelloSensor(coordinator, sensor_type))
    
    async_add_entities(entities)

class VoltelloCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry):
        super().__init__(
            hass,
            _LOGGER,
            name="Voltello",
            update_interval=timedelta(seconds=300),
        )
        self.entry = entry

    async def _async_update_data(self):
        service_points = await self.hass.async_add_executor_job(
            get_service_points_list, self.entry.data["customer_id"]
        )
        service_point_id = service_points['data']['servicePoints'][0]['servicePointId']
        
        live_data = await self.hass.async_add_executor_job(
            get_live_data, service_point_id
        )
        
        return get_displayed_data(live_data)

class VoltelloSensor(CoordinatorEntity, Entity):
    def __init__(self, coordinator, sensor_type):
        super().__init__(coordinator)
        self.sensor_type = sensor_type
        self.sensor_data = SENSOR_TYPES[sensor_type]

    @property
    def name(self):
        return f"Voltello {self.sensor_data['name']}"

    @property
    def unique_id(self):
        return f"voltello_{self.sensor_type}"

    @property
    def state(self):
        data = self.coordinator.data
        if self.sensor_data['key'] in data:
            if isinstance(data[self.sensor_data['key']], dict):
                if self.sensor_type == "battery_soc":
                    return data["battery"]["stateOfCharge"]
                return data[self.sensor_data['key']]["power"]
            return data[self.sensor_data['key']]
        return None

    @property
    def unit_of_measurement(self):
        return self.sensor_data["unit"]

    @property
    def icon(self):
        return self.sensor_data["icon"]