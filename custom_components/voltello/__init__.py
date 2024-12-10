import logging
from datetime import timedelta
import aiohttp
import async_timeout
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

DOMAIN = "voltello"
SCAN_INTERVAL = timedelta(minutes=5)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api_token = entry.data["api_token"]
    customer_id = entry.data["customer_id"]
    utility_id = entry.data["utility_id"]

    base_url = 'https://acapi.vecddevau1.village.energy/xv1'
    service_points_endpoint = '/get/customer/energy/electricity/servicepoints/'
    security_context = 'Voltello/CUSTOMERS/Individual/'

    headers = {
        "apiKey": api_token,
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    async def async_update_data():
        async with aiohttp.ClientSession() as session:
            # Get service point ID
            service_points_url = f"{base_url}{service_points_endpoint}{security_context}{customer_id}?customerId={customer_id}&utilityIdentifier={utility_id}"
            async with session.get(service_points_url, headers=headers) as response:
                service_points_list = await response.json()
                service_point_id = service_points_list['data']['servicePoints'][0]['servicePointId']

            # Get real-time usage data
            usage_url = f"{base_url}{service_points_endpoint}{service_point_id}/usage/realtime/{security_context}{customer_id}"
            async with session.get(usage_url, headers=headers) as response:
                live_data = await response.json()

                flow_data = live_data['data']['flowData']
                is_displayed = flow_data['isDisplayed']
                power_data = flow_data['power']

                displayed_data = {}

                if is_displayed.get('grid'):
                    displayed_data['grid'] = power_data['grid']['power']
                if is_displayed.get('solar'):
                    displayed_data['solar'] = {
                        'power': power_data['solar']['power'],
                        'name': power_data['solar']['endPoints'][0]['nickName']
                    }
                if is_displayed.get('battery'):
                    displayed_data['battery'] = {
                        'power': power_data['battery']['power'],
                        'stateOfCharge': power_data['battery']['endPoints'][0]['stateOfCharge']
                    }
                if is_displayed.get('home'):
                    displayed_data['home'] = power_data['home']['power']
                if is_displayed.get('ev'):
                    displayed_data['ev'] = power_data['ev']['power']

                return displayed_data

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="voltello_sensor",
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)