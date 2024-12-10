from __future__ import annotations
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.const import (
    UnitOfPower,
    PERCENTAGE,
)

from . import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = [
        VoltelloSensor(coordinator, "grid", "Grid Power", "kW"),
        VoltelloSensor(coordinator, "solar", "Solar Power", "kW"),
        VoltelloSensor(coordinator, "battery_power", "Battery Power", "kW"),
        VoltelloSensor(coordinator, "battery_charge", "Battery Charge", "%"),
        VoltelloSensor(coordinator, "home", "Home Power", "kW"),
        VoltelloSensor(coordinator, "ev", "EV Power", "kW"),
    ]

    async_add_entities(sensors)

class VoltelloSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, sensor_type, name, unit):
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_unique_id = f"voltello_{sensor_type}"

    @property
    def native_value(self):
        data = self.coordinator.data
        if not data:
            return None

        if self._sensor_type == "grid":
            return data.get("grid")
        elif self._sensor_type == "solar":
            return data.get("solar", {}).get("power")
        elif self._sensor_type == "battery_power":
            return data.get("battery", {}).get("power")
        elif self._sensor_type == "battery_charge":
            return data.get("battery", {}).get("stateOfCharge")
        elif self._sensor_type == "home":
            return data.get("home")
        elif self._sensor_type == "ev":
            return data.get("ev")