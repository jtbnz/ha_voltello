from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import ENERGY_KILO_WATT_HOUR
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .utils import get_service_points_list, get_live_data, get_displayed_data

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    api_token = config_entry.data["api_token"]
    customer_id = config_entry.data["customer_id"]
    utility_id = config_entry.data["utility_id"]

    coordinator = VoltelloDataUpdateCoordinator(hass, api_token, customer_id, utility_id)
    await coordinator.async_config_entry_first_refresh()

    sensors = []
    for sensor_type in ["solar", "grid", "battery", "home", "ev"]:
        sensors.append(VoltelloSensor(coordinator, sensor_type))

    async_add_entities(sensors, True)

class VoltelloDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api_token, customer_id, utility_id):
        self.api_token = api_token
        self.customer_id = customer_id
        self.utility_id = utility_id

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )

    async def _async_update_data(self):
        try:
            service_points_list = get_service_points_list(self.customer_id)
            service_point_id = service_points_list['data']['servicePoints'][0]['servicePointId']
            live_data = get_live_data(service_point_id)
            return get_displayed_data(live_data)
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")

class VoltelloSensor(SensorEntity):
    def __init__(self, coordinator, sensor_type):
        self.coordinator = coordinator
        self.sensor_type = sensor_type

    @property
    def name(self):
        return f"Voltello {self.sensor_type.capitalize()}"

    @property
    def state(self):
        return self.coordinator.data.get(self.sensor_type, {}).get("power")

    @property
    def unit_of_measurement(self):
        return ENERGY_KILO_WATT_HOUR

    @property
    def extra_state_attributes(self):
        if self.sensor_type == "battery":
            return {"state_of_charge": self.coordinator.data.get("battery", {}).get("stateOfCharge")}
        return {}

    @property
    def should_poll(self):
        return False

    @property
    def available(self):
        return self.coordinator.last_update_success

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))