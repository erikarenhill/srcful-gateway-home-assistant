import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    name = coordinator.data["name"]
    unique_id = entry.entry_id

    async_add_entities([
        GatewayNameSensor(coordinator, name, unique_id),
        GatewayUptimeSensor(coordinator, name, unique_id),
        InverterConnectionSensor(coordinator, name, unique_id),
        InverterHostSensor(coordinator, name, unique_id),
        InverterPortSensor(coordinator, name, unique_id),
        InverterStatusSensor(coordinator, name, unique_id),
        InverterTypeSensor(coordinator, name, unique_id),
        GatewayFirmwareVersionSensor(coordinator, name, unique_id),
        CryptoDeviceNameSensor(coordinator, name, unique_id),
        CryptoSerialSensor(coordinator, name, unique_id)
    ], update_before_add=True)

class InverterSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, unique_id, sensor_name, key, unit_of_measurement=None):
        super().__init__(coordinator)
        self._attr_name = f"{name} {sensor_name}"
        self._attr_unique_id = f"{unique_id}_{sensor_name.lower()}"
        self._key = key
        self._unit_of_measurement = unit_of_measurement
        self.coordinator = coordinator

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def state(self):
        return self.coordinator.data.get(self._key)

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
            name=self.coordinator.data["name"],
            manufacturer="Gateway Manufacturer",
            model="Gateway Model",
            sw_version=self.coordinator.data["version"].get("version"),
        )

class GatewayNameSensor(InverterSensor):
    def __init__(self, coordinator, name, unique_id):
        super().__init__(coordinator, name, unique_id, "Name", "name")

    @property
    def state(self):
        return self.coordinator.data["name"]

class GatewayUptimeSensor(InverterSensor):
    def __init__(self, coordinator, name, unique_id):
        super().__init__(coordinator, name, unique_id, "Uptime", "uptime", "s")

    @property
    def state(self):
        milliseconds = self.coordinator.data["uptime"].get("msek", 0)
        seconds = milliseconds // 1000
        return seconds

class InverterConnectionSensor(InverterSensor):
    def __init__(self, coordinator, name, unique_id):
        super().__init__(coordinator, name, unique_id, "Connection", "inverter")

    @property
    def state(self):
        return self.coordinator.data["inverter"].get("connection", "unknown")

class InverterHostSensor(InverterSensor):
    def __init__(self, coordinator, name, unique_id):
        super().__init__(coordinator, name, unique_id, "Host", "inverter")

    @property
    def state(self):
        return self.coordinator.data["inverter"].get("host", "unknown")

class InverterPortSensor(InverterSensor):
    def __init__(self, coordinator, name, unique_id):
        super().__init__(coordinator, name, unique_id, "Port", "inverter")

    @property
    def state(self):
        return self.coordinator.data["inverter"].get("port", 0)

class InverterStatusSensor(InverterSensor):
    def __init__(self, coordinator, name, unique_id):
        super().__init__(coordinator, name, unique_id, "Status", "inverter")

    @property
    def state(self):
        return self.coordinator.data["inverter"].get("status", "unknown")

class InverterTypeSensor(InverterSensor):
    def __init__(self, coordinator, name, unique_id):
        super().__init__(coordinator, name, unique_id, "Type", "inverter")

    @property
    def state(self):
        return self.coordinator.data["inverter"].get("type", "unknown")

class GatewayFirmwareVersionSensor(InverterSensor):
    def __init__(self, coordinator, name, unique_id):
        super().__init__(coordinator, name, unique_id, "Version", "version")

    @property
    def state(self):
        return self.coordinator.data["version"].get("version", "unknown")

class CryptoDeviceNameSensor(InverterSensor):
    def __init__(self, coordinator, name, unique_id):
        super().__init__(coordinator, name, unique_id, "Device name", "crypto")

    @property
    def state(self):
        return self.coordinator.data["crypto"].get("deviceName", "unknown")

class CryptoSerialSensor(InverterSensor):
    def __init__(self, coordinator, name, unique_id):
        super().__init__(coordinator, name, unique_id, "Serial number", "crypto")

    @property
    def state(self):
        return self.coordinator.data["crypto"].get("serialNumber", "unknown")