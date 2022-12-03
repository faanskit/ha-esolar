"""Support for ESolar sensors."""
from __future__ import annotations

import datetime
from datetime import timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, UnitOfPower, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import ESolarCoordinator
from .const import (
    CONF_INVERTER_SENSORS,
    CONF_MONITORED_SITES,
    CONF_PV_GRID_DATA,
    DOMAIN,
    I_CTR,
    I_CURRENT_POWER,
    I_DB,
    I_G_CURR_L,
    I_G_FREQ_L,
    I_G_VOL_L,
    I_MOD_SN,
    I_MODEL,
    I_MONTH_E,
    I_PC,
    I_PV_CURR_PV,
    I_PV_VOL_PV,
    I_SN,
    I_STATUS,
    I_TODAY_E,
    I_TOTAL_E,
    I_TYPE,
    MANUFACTURER,
    P_ADR,
    P_CO2,
    P_CURRENCY,
    P_CURRENT_POWER,
    P_INCOME,
    P_TOTAL_E,
    P_NAME,
    P_PEAK_POWER,
    P_POWER,
    P_TODAY_E,
    P_TREES,
    P_TYPE,
    P_TYPE_AC_COUPLING,
    P_TYPE_BLEND,
    P_TYPE_GRID,
    P_TYPE_STORAGE,
    P_UID,
    PLANT_MODEL,
    B_DIRECTION,
    B_PVELEC,
    B_USELEC,
    B_BUYELEC,
    B_SELLELEC,
    B_BUY_RATE,
    B_SELL_RATE,
    B_GRID_POWER_W,
    B_GRID_POWER_VA,
    B_OUT_VOLT,
    B_OUT_CURR,
    B_OUT_POWER_WATT,
    B_OUT_POWER_VA,
    B_OUT_FREQ,
    B_BACKUP_POWER_W,
    B_ON_G_VOLT,
    B_ON_G_FREQ,
    B_ON_G_POWER_W,
)

ICON_POWER = "mdi:solar-power"
ICON_PANEL = "mdi:solar-panel"

SCAN_INTERVAL = timedelta(minutes=1)
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)
PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the eSolar sensor."""
    coordinator: ESolarCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[ESolarSensor] = []
    my_plants = entry.options.get(CONF_MONITORED_SITES)
    use_inverter_sensors = entry.options.get(CONF_INVERTER_SENSORS)
    use_pv_grid_attributes = entry.options.get(CONF_PV_GRID_DATA)

    for enabled_plant in my_plants:
        for plant in coordinator.data["plantList"]:
            if plant["plantname"] == enabled_plant:
                entities.append(
                    ESolarSensorPlant(
                        coordinator, plant["plantname"], plant["plantuid"]
                    )
                )
                if plant["type"] == 0:
                    entities.append(
                        ESolarSensorPlantTotalEnergy(
                            coordinator, plant["plantname"], plant["plantuid"]
                        )
                    )
                elif plant["type"] == 3:
                    entities.append(
                        ESolarSensorPlantBatterySellEnergy(
                            coordinator, plant["plantname"], plant["plantuid"]
                        )
                    )
                    entities.append(
                        ESolarSensorPlantBatteryBuyEnergy(
                            coordinator, plant["plantname"], plant["plantuid"]
                        )
                    )
                    entities.append(
                        ESolarSensorPlantBatteryChargeEnergy(
                            coordinator, plant["plantname"], plant["plantuid"]
                        )
                    )
                    entities.append(
                        ESolarSensorPlantBatteryDischargeEnergy(
                            coordinator, plant["plantname"], plant["plantuid"]
                        )
                    )
                    entities.append(
                        ESolarSensorPlantBatterySoC(
                            coordinator, plant["plantname"], plant["plantuid"]
                        )
                    )

                if use_inverter_sensors:
                    for inverter in plant["plantDetail"]["snList"]:
                        entities.append(
                            ESolarInverterEnergyTotal(
                                coordinator,
                                plant["plantname"],
                                plant["plantuid"],
                                inverter,
                            )
                        )
                        entities.append(
                            ESolarInverterPower(
                                coordinator,
                                plant["plantname"],
                                plant["plantuid"],
                                inverter,
                                use_pv_grid_attributes,
                            )
                        )
    async_add_entities(entities, True)


class ESolarSensor(CoordinatorEntity[ESolarCoordinator], SensorEntity):
    """Representation of a generic ESolar sensor."""

    def __init__(self, coordinator: ESolarCoordinator, plant_name, plant_uid) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._plant_name = plant_name
        self._plant_uid = plant_uid

        self._device_name: None | str = None
        self._device_model: None | str = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device_info of the device."""
        device_info = DeviceInfo(
            identifiers={(DOMAIN, self._plant_name)},
            manufacturer=MANUFACTURER,
            model=self._device_model,
            name=self._device_name,
        )

        return device_info


class ESolarSensorPlant(ESolarSensor):
    """Representation of a eSolar sensor for the plant."""

    def __init__(self, coordinator: ESolarCoordinator, plant_name, plant_uid) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator=coordinator, plant_name=plant_name, plant_uid=plant_uid
        )
        self._last_updated: datetime.datetime | None = None
        self._attr_available = False

        self._attr_unique_id = f"plantUid_{plant_uid}"

        self._device_name = plant_name
        self._device_model = PLANT_MODEL

        self._attr_icon = ICON_PANEL
        self._attr_name = f"ESolar Plant {self._plant_name} Status"

        self._attr_extra_state_attributes = {
            P_NAME: None,
            P_UID: None,
            P_ADR: None,
            P_TYPE: None,
            P_POWER: None,
            P_CURRENCY: None,
            P_TOTAL_E: None,
            P_CO2: None,
            P_TREES: None,
        }

    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                self._attr_extra_state_attributes[P_NAME] = plant["plantname"]
                self._attr_extra_state_attributes[P_UID] = plant["plantuid"]
                self._attr_extra_state_attributes[P_ADR] = (
                    plant["address"] + " " + plant["country"]
                )
                if plant["type"] == 0:
                    self._attr_extra_state_attributes[P_TYPE] = P_TYPE_GRID
                if plant["type"] == 1:
                    self._attr_extra_state_attributes[P_TYPE] = P_TYPE_STORAGE
                if plant["type"] == 2:
                    self._attr_extra_state_attributes[P_TYPE] = P_TYPE_BLEND
                if plant["type"] == 3:
                    self._attr_extra_state_attributes[P_TYPE] = P_TYPE_AC_COUPLING
                self._attr_extra_state_attributes[P_POWER] = float(plant["systempower"])
                self._attr_extra_state_attributes[P_CURRENCY] = plant["currency"]
                self._attr_extra_state_attributes[P_TOTAL_E] = plant["totalElectricity"]
                self._attr_extra_state_attributes[P_CO2] = plant["plantDetail"][
                    "totalReduceCo2"
                ]
                self._attr_extra_state_attributes[P_TREES] = plant["plantDetail"][
                    "totalPlantTreeNum"
                ]
                # Income only relevant for type 1 (R5)
                if (plant["plantDetail"]["type"]) == 1:
                    self._attr_extra_state_attributes[P_INCOME] = plant["plantDetail"][
                        "income"
                    ]
                else:
                    self._attr_extra_state_attributes[P_INCOME] = None

                if plant["runningState"] == 1:
                    self._attr_native_value = "Normal"
                elif plant["runningState"] == 2:
                    self._attr_native_value = "Alarm"
                elif plant["runningState"] == 3:
                    self._attr_native_value = "Offline"
                else:
                    self._attr_native_value = None
                self._attr_available = True

    @property
    def native_value(self) -> str | None:
        """Return sensor state."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                if plant["runningState"] == 1:
                    value = "Normal"
                elif plant["runningState"] == 2:
                    value = "Alarm"
                elif plant["runningState"] == 3:
                    value = "Offline"
                else:
                    value = None

                self._attr_extra_state_attributes[P_NAME] = plant["plantname"]
                self._attr_extra_state_attributes[P_UID] = plant["plantuid"]
                self._attr_extra_state_attributes[P_ADR] = (
                    plant["address"] + " " + plant["country"]
                )
                if plant["type"] == 0:
                    self._attr_extra_state_attributes[P_TYPE] = P_TYPE_GRID
                if plant["type"] == 1:
                    self._attr_extra_state_attributes[P_TYPE] = P_TYPE_STORAGE
                if plant["type"] == 2:
                    self._attr_extra_state_attributes[P_TYPE] = P_TYPE_BLEND
                if plant["type"] == 3:
                    self._attr_extra_state_attributes[P_TYPE] = P_TYPE_AC_COUPLING
                self._attr_extra_state_attributes[P_POWER] = float(plant["systempower"])
                self._attr_extra_state_attributes[P_CURRENCY] = plant["currency"]
                if (plant["plantDetail"]["type"]) == 1:
                    self._attr_extra_state_attributes[P_INCOME] = plant["plantDetail"][
                        "income"
                    ]
                else:
                    self._attr_extra_state_attributes[P_INCOME] = None
                self._attr_extra_state_attributes[P_CO2] = plant["plantDetail"][
                    "totalReduceCo2"
                ]
                self._attr_extra_state_attributes[P_TREES] = plant["plantDetail"][
                    "totalPlantTreeNum"
                ]
        return value


class ESolarSensorPlantTotalEnergy(ESolarSensor):
    """Representation of a eSolar sensor for the plant."""

    def __init__(self, coordinator: ESolarCoordinator, plant_name, plant_uid) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator=coordinator, plant_name=plant_name, plant_uid=plant_uid
        )
        self._last_updated: datetime.datetime | None = None
        self._attr_available = False

        self._attr_unique_id = f"plantUid_energy_{plant_uid}"

        self._device_name = plant_name
        self._device_model = PLANT_MODEL

        self._attr_icon = ICON_POWER
        self._attr_name = f"ESolar Plant {self._plant_name} Energy Total "
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING

        self._attr_extra_state_attributes = {
            P_NAME: None,
            P_UID: None,
            P_TODAY_E: None,
            P_CURRENT_POWER: None,
            P_PEAK_POWER: None,
        }

    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                self._attr_extra_state_attributes[P_NAME] = plant["plantname"]
                self._attr_extra_state_attributes[P_UID] = plant["plantuid"]
                self._attr_extra_state_attributes[P_TODAY_E] = float(
                    plant["todayElectricity"]
                )
                self._attr_extra_state_attributes[P_CURRENT_POWER] = float(
                    plant["nowPower"]
                )
                if plant["type"] == 0:
                    self._attr_extra_state_attributes[P_PEAK_POWER] = float(
                        plant["peakPower"]
                    )
                else:
                    self._attr_extra_state_attributes[P_PEAK_POWER] = None
                self._attr_native_value = float(plant["totalElectricity"])
                self._attr_available = True

    @property
    def native_value(self) -> str | None:
        """Return sensor state."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                value = float(plant["totalElectricity"])

                self._attr_extra_state_attributes[P_NAME] = plant["plantname"]
                self._attr_extra_state_attributes[P_UID] = plant["plantuid"]
                self._attr_extra_state_attributes[P_TODAY_E] = float(
                    plant["todayElectricity"]
                )
                self._attr_extra_state_attributes[P_CURRENT_POWER] = float(
                    plant["nowPower"]
                )
                if plant["type"] == 0:
                    self._attr_extra_state_attributes[P_PEAK_POWER] = float(
                        plant["peakPower"]
                    )
                else:
                    self._attr_extra_state_attributes[P_PEAK_POWER] = None
        return value


class ESolarSensorPlantBatteryBuyEnergy(ESolarSensor):
    """Representation of a eSolar sensor for the plant."""

    def __init__(self, coordinator: ESolarCoordinator, plant_name, plant_uid) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator=coordinator, plant_name=plant_name, plant_uid=plant_uid
        )
        self._last_updated: datetime.datetime | None = None
        self._attr_available = False

        self._attr_unique_id = f"plantUid_energy_buy_{plant_uid}"

        self._device_name = plant_name
        self._device_model = PLANT_MODEL

        self._attr_icon = ICON_POWER
        self._attr_name = f"ESolar Plant {self._plant_name} Buy Energy Total"
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING

        self._attr_extra_state_attributes = {
            P_NAME: None,
            P_UID: None,
        }

    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                self._attr_extra_state_attributes[P_NAME] = plant["plantname"]
                self._attr_extra_state_attributes[P_UID] = plant["plantuid"]
                self._attr_native_value = float(plant["plantDetail"]["totalBuyElec"])
                self._attr_available = True

    @property
    def native_value(self) -> str | None:
        """Return sensor state."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                value = float(plant["plantDetail"]["totalBuyElec"])

        return value


class ESolarSensorPlantBatterySellEnergy(ESolarSensor):
    """Representation of a eSolar sensor for the plant."""

    def __init__(self, coordinator: ESolarCoordinator, plant_name, plant_uid) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator=coordinator, plant_name=plant_name, plant_uid=plant_uid
        )
        self._last_updated: datetime.datetime | None = None
        self._attr_available = False

        self._attr_unique_id = f"plantUid_energy_sell_{plant_uid}"

        self._device_name = plant_name
        self._device_model = PLANT_MODEL

        self._attr_icon = ICON_POWER
        self._attr_name = f"ESolar Plant {self._plant_name} Sell Energy Total"
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING

        self._attr_extra_state_attributes = {
            P_NAME: None,
            P_UID: None,
        }

    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                self._attr_extra_state_attributes[P_NAME] = plant["plantname"]
                self._attr_extra_state_attributes[P_UID] = plant["plantuid"]
                self._attr_native_value = float(plant["plantDetail"]["totalSellElec"])
                self._attr_available = True

    @property
    def native_value(self) -> str | None:
        """Return sensor state."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                value = float(plant["plantDetail"]["totalSellElec"])

        return value


class ESolarSensorPlantBatteryChargeEnergy(ESolarSensor):
    """Representation of a eSolar sensor for the plant."""

    def __init__(self, coordinator: ESolarCoordinator, plant_name, plant_uid) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator=coordinator, plant_name=plant_name, plant_uid=plant_uid
        )
        self._last_updated: datetime.datetime | None = None
        self._attr_available = False

        self._attr_unique_id = f"plantUid_energy_charge_{plant_uid}"

        self._device_name = plant_name
        self._device_model = PLANT_MODEL

        self._attr_icon = ICON_POWER
        self._attr_name = f"ESolar Plant {self._plant_name} Charge Energy"
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING

        self._attr_extra_state_attributes = {
            P_NAME: None,
            P_UID: None,
        }

    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                self._attr_extra_state_attributes[P_NAME] = plant["plantname"]
                self._attr_extra_state_attributes[P_UID] = plant["plantuid"]
                self._attr_native_value = float(plant["viewBean"]["chargeElec"])
                self._attr_available = True

    @property
    def native_value(self) -> str | None:
        """Return sensor state."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                value = float(plant["viewBean"]["chargeElec"])

        return value


class ESolarSensorPlantBatteryDischargeEnergy(ESolarSensor):
    """Representation of a eSolar sensor for the plant."""

    def __init__(self, coordinator: ESolarCoordinator, plant_name, plant_uid) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator=coordinator, plant_name=plant_name, plant_uid=plant_uid
        )
        self._last_updated: datetime.datetime | None = None
        self._attr_available = False

        self._attr_unique_id = f"plantUid_energy_discharge_{plant_uid}"

        self._device_name = plant_name
        self._device_model = PLANT_MODEL

        self._attr_icon = ICON_POWER
        self._attr_name = f"ESolar Plant {self._plant_name} Discharge Energy"
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING

        self._attr_extra_state_attributes = {
            P_NAME: None,
            P_UID: None,
        }

    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                self._attr_extra_state_attributes[P_NAME] = plant["plantname"]
                self._attr_extra_state_attributes[P_UID] = plant["plantuid"]
                self._attr_native_value = float(plant["viewBean"]["dischargeElec"])
                self._attr_available = True

    @property
    def native_value(self) -> str | None:
        """Return sensor state."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                value = float(plant["viewBean"]["dischargeElec"])

        return value


class ESolarSensorPlantBatterySoC(ESolarSensor):
    """Representation of a eSolar sensor for the plant."""

    def __init__(self, coordinator: ESolarCoordinator, plant_name, plant_uid) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator=coordinator, plant_name=plant_name, plant_uid=plant_uid
        )
        self._last_updated: datetime.datetime | None = None
        self._attr_available = False

        self._attr_unique_id = f"plantUid_energy_battery_soc_{plant_uid}"

        self._device_name = plant_name
        self._device_model = PLANT_MODEL

        # self._attr_icon = ICON_POWER
        self._attr_name = f"ESolar Plant {self._plant_name} State Of Charge"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_state_class = SensorStateClass.MEASUREMENT

        self._attr_extra_state_attributes = {
            P_NAME: None,
            P_UID: None,
        }

    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                self._attr_extra_state_attributes[P_NAME] = plant["plantname"]
                self._attr_extra_state_attributes[P_UID] = plant["plantuid"]
                self._attr_native_value = float(
                    plant["kitList"][0]["storeDevicePower"]["batEnergyPercent"]
                )
                self._attr_available = True

    @property
    def native_value(self) -> str | None:
        """Return sensor state."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                value = float(
                    plant["kitList"][0]["storeDevicePower"]["batEnergyPercent"]
                )

        return value


class ESolarInverterEnergyTotal(ESolarSensor):
    """Representation of a eSolar sensor for the plant."""

    def __init__(
        self, coordinator: ESolarCoordinator, plant_name, plant_uid, inverter_sn
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator=coordinator, plant_name=plant_name, plant_uid=plant_uid
        )
        self._last_updated: datetime.datetime | None = None
        self._attr_available = False

        self._attr_unique_id = f"inverter_{inverter_sn}"

        self._device_name = plant_name
        self._device_model = PLANT_MODEL

        self._attr_icon = ICON_POWER
        self._attr_name = f"ESolar {inverter_sn} Energy Total"
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING

        self._attr_extra_state_attributes = {
            P_NAME: None,
            P_UID: None,
            I_MODEL: None,
            I_TYPE: None,
            I_SN: None,
            I_PC: None,
            I_DB: None,
            I_CTR: None,
            I_MOD_SN: None,
            I_TODAY_E: None,
            I_MONTH_E: None,
            I_TOTAL_E: None,
            I_STATUS: None,
            I_CURRENT_POWER: None,
        }

    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                self._attr_extra_state_attributes[P_NAME] = plant["plantname"]
                self._attr_extra_state_attributes[P_UID] = plant["plantuid"]
                self._attr_extra_state_attributes[I_MODEL] = plant["kitList"][0][
                    "devicetype"
                ]
                if plant["kitList"][0]["type"] == 0:
                    self._attr_extra_state_attributes[I_TYPE] = "On-grid"
                else:
                    self._attr_extra_state_attributes[I_TYPE] = "Unknown"

                self._attr_extra_state_attributes[I_SN] = plant["kitList"][0][
                    "devicesn"
                ]
                self._attr_extra_state_attributes[I_PC] = plant["kitList"][0][
                    "devicepc"
                ]
                self._attr_extra_state_attributes[I_DB] = plant["kitList"][0][
                    "displayfw"
                ]
                self._attr_extra_state_attributes[I_CTR] = plant["kitList"][0][
                    "slavemcufw"
                ]
                self._attr_extra_state_attributes[I_MOD_SN] = plant["kitList"][0][
                    "kitSn"
                ]
                self._attr_extra_state_attributes[I_TODAY_E] = float(
                    plant["kitList"][0]["todaySellEnergy"]
                )
                self._attr_extra_state_attributes[I_MONTH_E] = float(
                    plant["kitList"][0]["monthSellEnergy"]
                )
                self._attr_extra_state_attributes[I_TOTAL_E] = float(
                    plant["kitList"][0]["totalSellEnergy"]
                )
                if plant["kitList"][0]["onLineStr"] == "1":
                    self._attr_extra_state_attributes[I_STATUS] = "Normal"
                elif plant["kitList"][0]["onLineStr"] == "2":
                    self._attr_extra_state_attributes[I_STATUS] = "Alarm"
                elif plant["kitList"][0]["onLineStr"] == "3":
                    self._attr_extra_state_attributes[I_STATUS] = "Off-line"
                elif plant["kitList"][0]["onLineStr"] == "4":
                    self._attr_extra_state_attributes[I_STATUS] = "Stock"
                elif plant["kitList"][0]["onLineStr"] == "4":
                    self._attr_extra_state_attributes[I_STATUS] = "History"
                else:
                    self._attr_extra_state_attributes[I_STATUS] = "Unknown"

                self._attr_extra_state_attributes[I_CURRENT_POWER] = plant["kitList"][
                    0
                ]["powernow"]

                if plant["kitList"][0]["type"] == 2:
                    if plant["kitList"][0]["storeDevicePower"]["batteryDirection"] == 0:
                        self._attr_extra_state_attributes[B_DIRECTION] = "Standby"
                    elif (
                        plant["kitList"][0]["storeDevicePower"]["batteryDirection"] == 1
                    ):
                        self._attr_extra_state_attributes[B_DIRECTION] = "Discharging"
                    elif (
                        plant["kitList"][0]["storeDevicePower"]["batteryDirection"]
                        == -1
                    ):
                        self._attr_extra_state_attributes[B_DIRECTION] = "Charging"
                    else:
                        self._attr_extra_state_attributes[B_DIRECTION] = "Unknown"

                    self._attr_extra_state_attributes[B_PVELEC] = plant["viewBean"][
                        "pvElec"
                    ]
                    self._attr_extra_state_attributes[B_USELEC] = plant["viewBean"][
                        "useElec"
                    ]
                    self._attr_extra_state_attributes[B_BUYELEC] = plant["viewBean"][
                        "buyElec"
                    ]
                    self._attr_extra_state_attributes[B_SELLELEC] = plant["viewBean"][
                        "sellElec"
                    ]
                    self._attr_extra_state_attributes[B_BUY_RATE] = plant["viewBean"][
                        "buyRate"
                    ]
                    self._attr_extra_state_attributes[B_SELL_RATE] = plant["viewBean"][
                        "sellRate"
                    ]
                self._attr_native_value = float(plant["kitList"][0]["totalSellEnergy"])

    @property
    def native_value(self) -> float | None:
        """Return sensor state."""
        value = None
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                value = float(plant["kitList"][0]["totalSellEnergy"])
                if plant["kitList"][0]["type"] == 0:
                    self._attr_extra_state_attributes[I_TYPE] = "On-grid"
                else:
                    self._attr_extra_state_attributes[I_TYPE] = "Unknown"
                self._attr_extra_state_attributes[I_TODAY_E] = float(
                    plant["kitList"][0]["todaySellEnergy"]
                )
                self._attr_extra_state_attributes[I_MONTH_E] = float(
                    plant["kitList"][0]["monthSellEnergy"]
                )
                self._attr_extra_state_attributes[I_TOTAL_E] = float(
                    plant["kitList"][0]["totalSellEnergy"]
                )
                if plant["kitList"][0]["onLineStr"] == "1":
                    self._attr_extra_state_attributes[I_STATUS] = "Normal"
                elif plant["kitList"][0]["onLineStr"] == "2":
                    self._attr_extra_state_attributes[I_STATUS] = "Alarm"
                elif plant["kitList"][0]["onLineStr"] == "3":
                    self._attr_extra_state_attributes[I_STATUS] = "Off-line"
                elif plant["kitList"][0]["onLineStr"] == "4":
                    self._attr_extra_state_attributes[I_STATUS] = "Stock"
                elif plant["kitList"][0]["onLineStr"] == "4":
                    self._attr_extra_state_attributes[I_STATUS] = "History"
                else:
                    self._attr_extra_state_attributes[I_STATUS] = "Unknown"

                self._attr_extra_state_attributes[I_CURRENT_POWER] = plant["kitList"][
                    0
                ]["powernow"]

                if plant["kitList"][0]["type"] == 2:
                    if plant["kitList"][0]["storeDevicePower"]["batteryDirection"] == 0:
                        self._attr_extra_state_attributes[B_DIRECTION] = "Standby"
                    elif (
                        plant["kitList"][0]["storeDevicePower"]["batteryDirection"] == 1
                    ):
                        self._attr_extra_state_attributes[B_DIRECTION] = "Discharging"
                    elif (
                        plant["kitList"][0]["storeDevicePower"]["batteryDirection"]
                        == -1
                    ):
                        self._attr_extra_state_attributes[B_DIRECTION] = "Charging"
                    else:
                        self._attr_extra_state_attributes[B_DIRECTION] = "Unknown"

                    self._attr_extra_state_attributes[B_PVELEC] = plant["viewBean"][
                        "pvElec"
                    ]
                    self._attr_extra_state_attributes[B_USELEC] = plant["viewBean"][
                        "useElec"
                    ]
                    self._attr_extra_state_attributes[B_BUYELEC] = plant["viewBean"][
                        "buyElec"
                    ]
                    self._attr_extra_state_attributes[B_SELLELEC] = plant["viewBean"][
                        "sellElec"
                    ]
                    self._attr_extra_state_attributes[B_BUY_RATE] = plant["viewBean"][
                        "buyRate"
                    ]
                    self._attr_extra_state_attributes[B_SELL_RATE] = plant["viewBean"][
                        "sellRate"
                    ]

        return value


class ESolarInverterPower(ESolarSensor):
    """Representation of a eSolar sensor for the plant."""

    def __init__(
        self,
        coordinator: ESolarCoordinator,
        plant_name,
        plant_uid,
        inverter_sn,
        use_pv_grid_attributes,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator=coordinator, plant_name=plant_name, plant_uid=plant_uid
        )
        self.use_pv_grid_attributes = use_pv_grid_attributes
        self._last_updated: datetime.datetime | None = None
        self._attr_available = False
        self._attr_unique_id = f"PV_{inverter_sn}"

        self._device_name = plant_name
        self._device_model = PLANT_MODEL

        self._attr_icon = ICON_POWER
        self._attr_name = f"ESolar {inverter_sn} Power"
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT

        if self.use_pv_grid_attributes:
            self._attr_extra_state_attributes = {
                P_NAME: None,
                P_UID: None,
                I_MODEL: None,
                I_SN: None,
                I_PV_VOL_PV: None,
                I_PV_CURR_PV: None,
                I_G_VOL_L: None,
                I_G_CURR_L: None,
                I_G_FREQ_L: None,
            }
        else:
            self._attr_extra_state_attributes = {
                P_NAME: None,
                P_UID: None,
                I_MODEL: None,
                I_SN: None,
            }
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                self._attr_extra_state_attributes[P_NAME] = plant["plantname"]
                self._attr_extra_state_attributes[P_UID] = plant["plantuid"]
                self._attr_extra_state_attributes[I_MODEL] = plant["kitList"][0][
                    "devicetype"
                ]
                self._attr_extra_state_attributes[I_SN] = plant["kitList"][0][
                    "devicesn"
                ]
                self._attr_native_value = float(plant["kitList"][0]["powernow"])

    @property
    def native_value(self) -> float | None:
        """Return sensor state."""
        value = None
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                value = float(plant["kitList"][0]["powernow"])
                if self.use_pv_grid_attributes:
                    if plant["kitList"][0]["onLineStr"] == "1":
                        self._attr_extra_state_attributes[I_PV_VOL_PV] = [
                            plant["kitList"][0]["findRawdataPageList"]["pV1Volt"],
                            plant["kitList"][0]["findRawdataPageList"]["pV2Volt"],
                            plant["kitList"][0]["findRawdataPageList"]["pV3Volt"],
                        ]
                        self._attr_extra_state_attributes[I_PV_CURR_PV] = [
                            plant["kitList"][0]["findRawdataPageList"]["pV1Curr"],
                            plant["kitList"][0]["findRawdataPageList"]["pV2Curr"],
                            plant["kitList"][0]["findRawdataPageList"]["pV3Curr"],
                        ]
                        self._attr_extra_state_attributes[I_G_VOL_L] = [
                            plant["kitList"][0]["findRawdataPageList"]["rGridVolt"],
                            plant["kitList"][0]["findRawdataPageList"]["sGridVolt"],
                            plant["kitList"][0]["findRawdataPageList"]["tGridVolt"],
                        ]
                        self._attr_extra_state_attributes[I_G_CURR_L] = [
                            plant["kitList"][0]["findRawdataPageList"]["rGridCurr"],
                            plant["kitList"][0]["findRawdataPageList"]["sGridCurr"],
                            plant["kitList"][0]["findRawdataPageList"]["tGridCurr"],
                        ]
                        self._attr_extra_state_attributes[I_G_FREQ_L] = [
                            plant["kitList"][0]["findRawdataPageList"]["rGridFreq"],
                            plant["kitList"][0]["findRawdataPageList"]["sGridFreq"],
                            plant["kitList"][0]["findRawdataPageList"]["tGridFreq"],
                        ]
                        self._attr_extra_state_attributes[I_G_FREQ_L] = [
                            plant["kitList"][0]["findRawdataPageList"]["rGridFreq"],
                            plant["kitList"][0]["findRawdataPageList"]["sGridFreq"],
                            plant["kitList"][0]["findRawdataPageList"]["tGridFreq"],
                        ]
                        if (
                            plant["kitList"][0]["findRawdataPageList"]["deviceType"]
                        ) == 2:

                            self._attr_extra_state_attributes[B_GRID_POWER_W] = [
                                plant["kitList"][0]["findRawdataPageList"][
                                    "rGridPowerWatt"
                                ],
                                plant["kitList"][0]["findRawdataPageList"][
                                    "sGridPowerWatt"
                                ],
                                plant["kitList"][0]["findRawdataPageList"][
                                    "tGridPowerWatt"
                                ],
                            ]
                            self._attr_extra_state_attributes[B_GRID_POWER_VA] = [
                                plant["kitList"][0]["findRawdataPageList"][
                                    "rGridPowerVA"
                                ],
                                plant["kitList"][0]["findRawdataPageList"][
                                    "sGridPowerVA"
                                ],
                                plant["kitList"][0]["findRawdataPageList"][
                                    "tGridPowerVA"
                                ],
                            ]
                            self._attr_extra_state_attributes[B_OUT_VOLT] = [
                                plant["kitList"][0]["findRawdataPageList"]["rOutVolt"],
                                plant["kitList"][0]["findRawdataPageList"]["sOutVolt"],
                                plant["kitList"][0]["findRawdataPageList"]["tOutVolt"],
                            ]
                            self._attr_extra_state_attributes[B_OUT_CURR] = [
                                plant["kitList"][0]["findRawdataPageList"]["rOutCurr"],
                                plant["kitList"][0]["findRawdataPageList"]["sOutCurr"],
                                plant["kitList"][0]["findRawdataPageList"]["tOutCurr"],
                            ]
                            self._attr_extra_state_attributes[B_OUT_POWER_WATT] = [
                                plant["kitList"][0]["findRawdataPageList"][
                                    "rOutPowerWatt"
                                ],
                                plant["kitList"][0]["findRawdataPageList"][
                                    "sOutPowerWatt"
                                ],
                                plant["kitList"][0]["findRawdataPageList"][
                                    "tOutPowerWatt"
                                ],
                            ]
                            self._attr_extra_state_attributes[B_OUT_POWER_VA] = [
                                plant["kitList"][0]["findRawdataPageList"][
                                    "rOutPowerVA"
                                ],
                                plant["kitList"][0]["findRawdataPageList"][
                                    "sOutPowerVA"
                                ],
                                plant["kitList"][0]["findRawdataPageList"][
                                    "tOutPowerVA"
                                ],
                            ]
                            self._attr_extra_state_attributes[B_OUT_FREQ] = [
                                plant["kitList"][0]["findRawdataPageList"]["rOutFreq"],
                                plant["kitList"][0]["findRawdataPageList"]["sOutFreq"],
                                plant["kitList"][0]["findRawdataPageList"]["tOutFreq"],
                            ]
                            self._attr_extra_state_attributes[B_ON_G_VOLT] = [
                                plant["kitList"][0]["findRawdataPageList"][
                                    "rOnGridOutVolt"
                                ],
                                plant["kitList"][0]["findRawdataPageList"][
                                    "sOnGridOutVolt"
                                ],
                                plant["kitList"][0]["findRawdataPageList"][
                                    "tOnGridOutVolt"
                                ],
                            ]
                            self._attr_extra_state_attributes[B_ON_G_FREQ] = [
                                plant["kitList"][0]["findRawdataPageList"][
                                    "rOnGridOutFreq"
                                ]
                            ]
                            self._attr_extra_state_attributes[B_ON_G_POWER_W] = [
                                plant["kitList"][0]["findRawdataPageList"][
                                    "rOnGridOutPowerWatt"
                                ],
                                plant["kitList"][0]["findRawdataPageList"][
                                    "sOnGridOutPowerWatt"
                                ],
                                plant["kitList"][0]["findRawdataPageList"][
                                    "tOnGridOutPowerWatt"
                                ],
                            ]
                            self._attr_extra_state_attributes[B_ON_G_FREQ] = [
                                plant["kitList"][0]["findRawdataPageList"][
                                    "rOnGridOutFreq"
                                ]
                            ]
                            self._attr_extra_state_attributes[B_BACKUP_POWER_W] = [
                                plant["kitList"][0]["findRawdataPageList"][
                                    "rBackupPowerWatt"
                                ]
                            ]
                    else:
                        self._attr_extra_state_attributes[I_PV_VOL_PV] = [
                            None,
                            None,
                            None,
                        ]
                        self._attr_extra_state_attributes[I_PV_CURR_PV] = [
                            None,
                            None,
                            None,
                        ]
                        self._attr_extra_state_attributes[I_G_VOL_L] = [
                            None,
                            None,
                            None,
                        ]
                        self._attr_extra_state_attributes[I_G_CURR_L] = [
                            None,
                            None,
                            None,
                        ]
                        self._attr_extra_state_attributes[I_G_FREQ_L] = [
                            None,
                            None,
                            None,
                        ]

        return value
