DOMAIN = "voltello"
CONF_API_TOKEN = "api_token"
CONF_CUSTOMER_ID = "customer_id"
CONF_UTILITY_ID = "utility_id"

DEFAULT_SCAN_INTERVAL = 300  # 5 minutes

SENSOR_TYPES = {
    "solar_power": {
        "key": "solar",
        "name": "Solar Power",
        "unit": "kW",
        "icon": "mdi:solar-power"
    },
    "grid_power": {
        "key": "grid",
        "name": "Grid Power",
        "unit": "kW",
        "icon": "mdi:transmission-tower"
    },
    "battery_power": {
        "key": "battery",
        "name": "Battery Power",
        "unit": "kW",
        "icon": "mdi:battery"
    },
    "battery_soc": {
        "key": "battery_soc",
        "name": "Battery State of Charge",
        "unit": "%",
        "icon": "mdi:battery-charging"
    },
    "home_power": {
        "key": "home",
        "name": "Home Power",
        "unit": "kW",
        "icon": "mdi:home"
    },
    "ev_power": {
        "key": "ev",
        "name": "EV Power",
        "unit": "kW",
        "icon": "mdi:car-electric"
    }
}