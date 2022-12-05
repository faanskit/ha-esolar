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
    P_UNKNOWN,
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
    P_TYPE_ONGRID,
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
    I_NORMAL,
    I_ALARM,
    I_OFFLINE,
    I_STOCK,
    I_HISTORY,
    B_DIR_CH,
    B_DIR_DIS,
    B_DIR_STB,
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
                    peak_power = 0
                    for inverter in plant["peakList"]:
                        peak_power += inverter["peakPower"]
                    self._attr_extra_state_attributes[P_PEAK_POWER] = float(peak_power)
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
                    peak_power = 0
                    for inverter in plant["peakList"]:
                        peak_power += inverter["peakPower"]
                    self._attr_extra_state_attributes[P_PEAK_POWER] = float(peak_power)
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
                charge = float(0)
                if "beanList" in plant:
                    for bean in plant["beanList"]:
                        charge += float(bean["chargeElec"])
                self._attr_available = True

    @property
    def native_value(self) -> str | None:
        """Return sensor state."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                charge = float(0)
                if "beanList" in plant:
                    for bean in plant["beanList"]:
                        charge += float(bean["chargeElec"])
                value = charge

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
                discharge = float(0)
                if "beanList" in plant:
                    for bean in plant["beanList"]:
                        discharge += float(bean["dischargeElec"])
                self._attr_native_value = discharge
                self._attr_available = True

    @property
    def native_value(self) -> str | None:
        """Return sensor state."""
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                discharge = float(0)
                if "beanList" in plant:
                    for bean in plant["beanList"]:
                        discharge += float(bean["dischargeElec"])
                value = discharge

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
        installed_power = 0
        available_power = 0
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                self._attr_extra_state_attributes[P_NAME] = plant["plantname"]
                self._attr_extra_state_attributes[P_UID] = plant["plantuid"]
                for inverter in plant["plantDetail"]["snList"]:
                    for kit in plant["kitList"]:
                        if inverter == kit["devicesn"]:
                            if kit["onLineStr"] == "1":
                                installed_power += kit["storeDevicePower"]["batCapcity"]
                                available_power += (
                                    kit["storeDevicePower"]["batCapcity"]
                                    * kit["storeDevicePower"]["batEnergyPercent"]
                                )

                if installed_power > 0:
                    self._attr_native_value = float(available_power / installed_power)
                    self._attr_available = True
                else:
                    self._attr_available = False

    @property
    def native_value(self) -> str | None:
        """Return sensor state."""
        installed_power = 0
        available_power = 0
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                for inverter in plant["plantDetail"]["snList"]:
                    for kit in plant["kitList"]:
                        if inverter == kit["devicesn"]:
                            if kit["onLineStr"] == "1":
                                installed_power += kit["storeDevicePower"]["batCapcity"]
                                available_power += (
                                    kit["storeDevicePower"]["batCapcity"]
                                    * kit["storeDevicePower"]["batEnergyPercent"]
                                )
                if installed_power > 0:
                    value = float(available_power / installed_power)
                else:
                    value = None

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
        self.inverter_sn = inverter_sn

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
                for kit in plant["kitList"]:
                    if kit["devicesn"] == self.inverter_sn:
                        self._attr_extra_state_attributes[I_MODEL] = kit["devicetype"]

                        if kit["type"] == 0:
                            self._attr_extra_state_attributes[I_TYPE] = P_TYPE_ONGRID
                        elif kit["type"] == 1:
                            self._attr_extra_state_attributes[I_TYPE] = P_TYPE_STORAGE
                        elif kit["type"] == 2:
                            self._attr_extra_state_attributes[
                                I_TYPE
                            ] = P_TYPE_AC_COUPLING
                        else:
                            self._attr_extra_state_attributes[I_TYPE] = P_UNKNOWN

                        self._attr_extra_state_attributes[I_SN] = kit["devicesn"]
                        self._attr_extra_state_attributes[I_PC] = kit["devicepc"]
                        self._attr_extra_state_attributes[I_DB] = kit["displayfw"]
                        # self._attr_extra_state_attributes[I_CTR] = kit["slavemcufw"]
                        self._attr_extra_state_attributes[I_CTR] = kit["mastermcufw"]
                        self._attr_extra_state_attributes[I_MOD_SN] = kit["kitSn"]
                        self._attr_extra_state_attributes[I_TODAY_E] = float(
                            kit["todaySellEnergy"]
                        )
                        self._attr_extra_state_attributes[I_MONTH_E] = float(
                            kit["monthSellEnergy"]
                        )
                        self._attr_extra_state_attributes[I_TOTAL_E] = float(
                            kit["totalSellEnergy"]
                        )
                        if kit["onLineStr"] == "1":
                            self._attr_extra_state_attributes[I_STATUS] = I_NORMAL
                        elif kit["onLineStr"] == "2":
                            self._attr_extra_state_attributes[I_STATUS] = I_ALARM
                        elif kit["onLineStr"] == "3":
                            self._attr_extra_state_attributes[I_STATUS] = I_OFFLINE
                        elif kit["onLineStr"] == "4":
                            self._attr_extra_state_attributes[I_STATUS] = I_STOCK
                        elif kit["onLineStr"] == "5":
                            self._attr_extra_state_attributes[I_STATUS] = I_HISTORY
                        else:
                            self._attr_extra_state_attributes[I_STATUS] = P_UNKNOWN

                        self._attr_extra_state_attributes[I_CURRENT_POWER] = kit[
                            "powernow"
                        ]

                        if kit["type"] == 2:
                            if kit["storeDevicePower"]["batteryDirection"] == 0:
                                self._attr_extra_state_attributes[
                                    B_DIRECTION
                                ] = B_DIR_STB
                            elif kit["storeDevicePower"]["batteryDirection"] == 1:
                                self._attr_extra_state_attributes[
                                    B_DIRECTION
                                ] = B_DIR_DIS
                            elif kit["storeDevicePower"]["batteryDirection"] == -1:
                                self._attr_extra_state_attributes[
                                    B_DIRECTION
                                ] = B_DIR_CH
                            else:
                                self._attr_extra_state_attributes[
                                    B_DIRECTION
                                ] = P_UNKNOWN

                        self._attr_native_value = float(kit["totalSellEnergy"])

                if "beanList" in plant:
                    for bean in plant["beanList"]:
                        if bean["devicesn"] == self.inverter_sn:
                            self._attr_extra_state_attributes[B_PVELEC] = bean["pvElec"]
                            self._attr_extra_state_attributes[B_USELEC] = bean[
                                "useElec"
                            ]
                            self._attr_extra_state_attributes[B_BUYELEC] = bean[
                                "buyElec"
                            ]
                            self._attr_extra_state_attributes[B_SELLELEC] = bean[
                                "sellElec"
                            ]
                            self._attr_extra_state_attributes[B_BUY_RATE] = bean[
                                "buyRate"
                            ]
                            self._attr_extra_state_attributes[B_SELL_RATE] = bean[
                                "sellRate"
                            ]

    @property
    def native_value(self) -> float | None:
        """Return sensor state."""
        value = None
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                for kit in plant["kitList"]:
                    if kit["devicesn"] == self.inverter_sn:
                        value = float(kit["totalSellEnergy"])
                        if kit["type"] == 0:
                            self._attr_extra_state_attributes[I_TYPE] = P_TYPE_ONGRID
                        elif kit["type"] == 1:
                            self._attr_extra_state_attributes[I_TYPE] = P_TYPE_STORAGE
                        elif kit["type"] == 2:
                            self._attr_extra_state_attributes[
                                I_TYPE
                            ] = P_TYPE_AC_COUPLING
                        else:
                            self._attr_extra_state_attributes[I_TYPE] = P_UNKNOWN
                        self._attr_extra_state_attributes[I_TODAY_E] = float(
                            kit["todaySellEnergy"]
                        )
                        self._attr_extra_state_attributes[I_MONTH_E] = float(
                            kit["monthSellEnergy"]
                        )
                        self._attr_extra_state_attributes[I_TOTAL_E] = float(
                            kit["totalSellEnergy"]
                        )
                        if kit["onLineStr"] == "1":
                            self._attr_extra_state_attributes[I_STATUS] = I_NORMAL
                        elif kit["onLineStr"] == "2":
                            self._attr_extra_state_attributes[I_STATUS] = I_ALARM
                        elif kit["onLineStr"] == "3":
                            self._attr_extra_state_attributes[I_STATUS] = I_OFFLINE
                        elif kit["onLineStr"] == "4":
                            self._attr_extra_state_attributes[I_STATUS] = I_STOCK
                        elif kit["onLineStr"] == "4":
                            self._attr_extra_state_attributes[I_STATUS] = I_HISTORY
                        else:
                            self._attr_extra_state_attributes[I_STATUS] = P_UNKNOWN

                        self._attr_extra_state_attributes[I_CURRENT_POWER] = kit[
                            "powernow"
                        ]

                        if kit["type"] == 2:
                            if kit["storeDevicePower"]["batteryDirection"] == 0:
                                self._attr_extra_state_attributes[
                                    B_DIRECTION
                                ] = B_DIR_STB
                            elif kit["storeDevicePower"]["batteryDirection"] == 1:
                                self._attr_extra_state_attributes[
                                    B_DIRECTION
                                ] = B_DIR_DIS
                            elif kit[0]["storeDevicePower"]["batteryDirection"] == -1:
                                self._attr_extra_state_attributes[
                                    B_DIRECTION
                                ] = B_DIR_CH
                            else:
                                self._attr_extra_state_attributes[
                                    B_DIRECTION
                                ] = P_UNKNOWN
                if "beanList" in plant:
                    for bean in plant["beanList"]:
                        if bean["devicesn"] == self.inverter_sn:
                            self._attr_extra_state_attributes[B_PVELEC] = bean["pvElec"]
                            self._attr_extra_state_attributes[B_USELEC] = bean[
                                "useElec"
                            ]
                            self._attr_extra_state_attributes[B_BUYELEC] = bean[
                                "buyElec"
                            ]
                            self._attr_extra_state_attributes[B_SELLELEC] = bean[
                                "sellElec"
                            ]
                            self._attr_extra_state_attributes[B_BUY_RATE] = bean[
                                "buyRate"
                            ]
                            self._attr_extra_state_attributes[B_SELL_RATE] = bean[
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
        self.inverter_sn = inverter_sn

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
                for kit in plant["kitList"]:
                    if kit["devicesn"] == self.inverter_sn:
                        self._attr_extra_state_attributes[I_MODEL] = kit["devicetype"]
                        self._attr_extra_state_attributes[I_SN] = kit["devicesn"]
                        self._attr_native_value = float(kit["powernow"])

    @property
    def native_value(self) -> float | None:
        """Return sensor state."""
        value = None
        for plant in self._coordinator.data["plantList"]:
            if plant["plantname"] == self._plant_name:
                for kit in plant["kitList"]:
                    if kit["devicesn"] == self.inverter_sn:
                        value = float(kit["powernow"])
                        if self.use_pv_grid_attributes:
                            if kit["onLineStr"] == "1":
                                self._attr_extra_state_attributes[I_PV_VOL_PV] = [
                                    kit["findRawdataPageList"]["pV1Volt"],
                                    kit["findRawdataPageList"]["pV2Volt"],
                                    kit["findRawdataPageList"]["pV3Volt"],
                                ]
                                self._attr_extra_state_attributes[I_PV_CURR_PV] = [
                                    kit["findRawdataPageList"]["pV1Curr"],
                                    kit["findRawdataPageList"]["pV2Curr"],
                                    kit["findRawdataPageList"]["pV3Curr"],
                                ]
                                self._attr_extra_state_attributes[I_G_VOL_L] = [
                                    kit["findRawdataPageList"]["rGridVolt"],
                                    kit["findRawdataPageList"]["sGridVolt"],
                                    kit["findRawdataPageList"]["tGridVolt"],
                                ]
                                self._attr_extra_state_attributes[I_G_CURR_L] = [
                                    kit["findRawdataPageList"]["rGridCurr"],
                                    kit["findRawdataPageList"]["sGridCurr"],
                                    kit["findRawdataPageList"]["tGridCurr"],
                                ]
                                self._attr_extra_state_attributes[I_G_FREQ_L] = [
                                    kit["findRawdataPageList"]["rGridFreq"],
                                    kit["findRawdataPageList"]["sGridFreq"],
                                    kit["findRawdataPageList"]["tGridFreq"],
                                ]
                                self._attr_extra_state_attributes[I_G_FREQ_L] = [
                                    kit["findRawdataPageList"]["rGridFreq"],
                                    kit["findRawdataPageList"]["sGridFreq"],
                                    kit["findRawdataPageList"]["tGridFreq"],
                                ]
                                if (kit["findRawdataPageList"]["deviceType"]) == 2:

                                    self._attr_extra_state_attributes[
                                        B_GRID_POWER_W
                                    ] = [
                                        kit["findRawdataPageList"]["rGridPowerWatt"],
                                        kit["findRawdataPageList"]["sGridPowerWatt"],
                                        kit["findRawdataPageList"]["tGridPowerWatt"],
                                    ]
                                    self._attr_extra_state_attributes[
                                        B_GRID_POWER_VA
                                    ] = [
                                        kit["findRawdataPageList"]["rGridPowerVA"],
                                        kit["findRawdataPageList"]["sGridPowerVA"],
                                        kit["findRawdataPageList"]["tGridPowerVA"],
                                    ]
                                    self._attr_extra_state_attributes[B_OUT_VOLT] = [
                                        kit["findRawdataPageList"]["rOutVolt"],
                                        kit["findRawdataPageList"]["sOutVolt"],
                                        kit["findRawdataPageList"]["tOutVolt"],
                                    ]
                                    self._attr_extra_state_attributes[B_OUT_CURR] = [
                                        kit["findRawdataPageList"]["rOutCurr"],
                                        kit["findRawdataPageList"]["sOutCurr"],
                                        kit["findRawdataPageList"]["tOutCurr"],
                                    ]
                                    self._attr_extra_state_attributes[
                                        B_OUT_POWER_WATT
                                    ] = [
                                        kit["findRawdataPageList"]["rOutPowerWatt"],
                                        kit["findRawdataPageList"]["sOutPowerWatt"],
                                        kit["findRawdataPageList"]["tOutPowerWatt"],
                                    ]
                                    self._attr_extra_state_attributes[
                                        B_OUT_POWER_VA
                                    ] = [
                                        kit["findRawdataPageList"]["rOutPowerVA"],
                                        kit["findRawdataPageList"]["sOutPowerVA"],
                                        kit["findRawdataPageList"]["tOutPowerVA"],
                                    ]
                                    self._attr_extra_state_attributes[B_OUT_FREQ] = [
                                        kit["findRawdataPageList"]["rOutFreq"],
                                        kit["findRawdataPageList"]["sOutFreq"],
                                        kit["findRawdataPageList"]["tOutFreq"],
                                    ]
                                    self._attr_extra_state_attributes[B_ON_G_VOLT] = [
                                        kit["findRawdataPageList"]["rOnGridOutVolt"],
                                        kit["findRawdataPageList"]["sOnGridOutVolt"],
                                        kit["findRawdataPageList"]["tOnGridOutVolt"],
                                    ]
                                    self._attr_extra_state_attributes[B_ON_G_FREQ] = [
                                        kit["findRawdataPageList"]["rOnGridOutFreq"]
                                    ]
                                    self._attr_extra_state_attributes[
                                        B_ON_G_POWER_W
                                    ] = [
                                        kit["findRawdataPageList"][
                                            "rOnGridOutPowerWatt"
                                        ],
                                        kit["findRawdataPageList"][
                                            "sOnGridOutPowerWatt"
                                        ],
                                        kit["findRawdataPageList"][
                                            "tOnGridOutPowerWatt"
                                        ],
                                    ]
                                    self._attr_extra_state_attributes[B_ON_G_FREQ] = [
                                        kit["findRawdataPageList"]["rOnGridOutFreq"]
                                    ]
                                    self._attr_extra_state_attributes[
                                        B_BACKUP_POWER_W
                                    ] = [kit["findRawdataPageList"]["rBackupPowerWatt"]]
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
