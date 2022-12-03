"""ESolar Cloud Platform data fetchers"""
import requests
import datetime
from datetime import timedelta
import calendar


BASE_URL = "https://fopapp.saj-electric.com/sajAppApi/api"
BASE_URL_WEB = "https://fop.saj-electric.com/saj"
WEB_TIMEOUT = 10

BASIC_TEST = False
# Use "H1", "R5" or "Robbie"
TEST_SYSTEM = "Robbie"
if BASIC_TEST:
    from .esolar_static_test import (
        get_esolar_data_static_r5,
        get_esolar_data_static_h1,
        get_esolar_data_static_robbie,
        web_get_plant_static_r5,
        web_get_plant_static_h1,
        web_get_plant_static_robbie,
    )


def add_months(sourcedate, months):
    """SAJ eSolar Helper Function - Adds a months to input"""
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def add_years(source_date, years):
    """SAJ eSolar Helper Function - Adds a years to input"""
    try:
        return source_date.replace(year=source_date.year + years)
    except ValueError:
        return source_date + (
            datetime.date(source_date.year + years, 1, 1)
            - datetime.date(source_date.year, 1, 1)
        )


def get_esolar_data(username, password, plant_list=None, use_pv_grid_attributes=True):
    """SAJ eSolar Data Update"""
    if BASIC_TEST:
        if TEST_SYSTEM == "H1":
            return get_esolar_data_static_h1(
                username, password, plant_list, use_pv_grid_attributes
            )
        elif TEST_SYSTEM == "Robbie":
            return get_esolar_data_static_robbie(
                username, password, plant_list, use_pv_grid_attributes
            )
        return get_esolar_data_static_r5(
            username, password, plant_list, use_pv_grid_attributes
        )

    try:
        plant_info = None
        session = esolar_web_autenticate(username, password)
        plant_info = web_get_plant(session, plant_list)
        web_get_plant_details(session, plant_info)
        web_get_plant_detailed_chart(session, plant_info)
        web_get_device_page_list(session, plant_info, use_pv_grid_attributes)

    except requests.exceptions.HTTPError as errh:
        raise requests.exceptions.HTTPError(errh)
    except requests.exceptions.ConnectionError as errc:
        raise requests.exceptions.ConnectionError(errc)
    except requests.exceptions.Timeout as errt:
        raise requests.exceptions.Timeout(errt)
    except requests.exceptions.RequestException as errr:
        raise requests.exceptions.RequestException(errr)
    except ValueError as errv:
        raise ValueError(errv) from errv

    return plant_info


def esolar_web_autenticate(username, password):
    """
    Function to authenticate on SAJ's WEB Portal
    """
    if BASIC_TEST:
        return True

    try:
        session = requests.Session()
        response = session.post(
            BASE_URL_WEB + "/login",
            data={
                "lang": "en",
                "username": username,
                "password": password,
                "rememberMe": "true",
            },
            timeout=WEB_TIMEOUT,
        )

        response.raise_for_status()

        if response.status_code != 200:
            raise ValueError(f"Login failed, returned {response.status_code}")

        return session

    except requests.exceptions.HTTPError as errh:
        raise requests.exceptions.HTTPError(errh)
    except requests.exceptions.ConnectionError as errc:
        raise requests.exceptions.ConnectionError(errc)
    except requests.exceptions.Timeout as errt:
        raise requests.exceptions.Timeout(errt)
    except requests.exceptions.RequestException as errr:
        raise requests.exceptions.RequestException(errr)


def web_get_plant(session, requested_plant_list=None):
    """
    Function to retrieve platUid from WEB Portal, requires web_authenticate
    """
    if session is None:
        raise ValueError("Missing session identifier trying to obain plants")

    if BASIC_TEST:
        if TEST_SYSTEM == "H1":
            return web_get_plant_static_h1()
        if TEST_SYSTEM == "Robbie":
            return web_get_plant_static_robbie()
        return web_get_plant_static_r5()

    try:
        output_plant_list = []
        response = session.post(
            BASE_URL_WEB + "/monitor/site/getUserPlantList",
            data={
                "pageNo": "",
                "pageSize": "",
                "orderByIndex": "",
                "officeId": "",
                "clientDate": datetime.date.today().strftime("%Y-%m-%d"),
                "runningState": "",
                "selectInputType": "",
                "plantName": "",
                "deviceSn": "",
                "type": "",
                "countryCode": "",
                "isRename": "",
                "isTimeError": "",
                "systemPowerLeast": "",
                "systemPowerMost": "",
            },
            timeout=WEB_TIMEOUT,
        )

        response.raise_for_status()
        plant_list = response.json()
        if requested_plant_list is not None:
            for plant in plant_list["plantList"]:
                if plant["plantname"] in requested_plant_list:
                    output_plant_list.append(plant)
            return {"status": plant_list["status"], "plantList": output_plant_list}

        return plant_list

    except requests.exceptions.HTTPError as errh:
        raise requests.exceptions.HTTPError(errh)
    except requests.exceptions.ConnectionError as errc:
        raise requests.exceptions.ConnectionError(errc)
    except requests.exceptions.Timeout as errt:
        raise requests.exceptions.Timeout(errt)
    except requests.exceptions.RequestException as errr:
        raise requests.exceptions.RequestException(errr)


def web_get_plant_details(session, plant_info):
    """
    Function to retrieve platUid from WEB Portal, requires web_authenticate
    """
    if session is None:
        raise ValueError("Missing session identifier trying to obain plants")

    try:
        device_list = []
        for plant in plant_info["plantList"]:
            response = session.post(
                BASE_URL_WEB + "/monitor/site/getPlantDetailInfo",
                data={
                    "plantuid": plant["plantuid"],
                    "clientDate": datetime.date.today().strftime("%Y-%m-%d"),
                },
                timeout=WEB_TIMEOUT,
            )

            response.raise_for_status()
            plant_detail = response.json()
            plant.update(plant_detail)
            for device in plant_detail["plantDetail"]["snList"]:
                device_list.append(device)

    except requests.exceptions.HTTPError as errh:
        raise requests.exceptions.HTTPError(errh)
    except requests.exceptions.ConnectionError as errc:
        raise requests.exceptions.ConnectionError(errc)
    except requests.exceptions.Timeout as errt:
        raise requests.exceptions.Timeout(errt)
    except requests.exceptions.RequestException as errr:
        raise requests.exceptions.RequestException(errr)


def web_get_plant_detailed_chart(session, plant_info):
    """
    Function to retrieve kitList from WEB Portal, requires web_authenticate
    """
    if session is None:
        raise ValueError("Missing session identifier trying to obain plants")

    try:
        today = datetime.date.today()
        previous_chart_day = today - timedelta(days=1)
        next_chart_day = today + timedelta(days=1)
        chart_day = today.strftime("%Y-%m-%d")
        previous_chart_month = add_months(today, -1).strftime("%Y-%m")
        next_chart_month = add_months(today, 1).strftime("%Y-%m")
        chart_month = today.strftime("%Y-%m")
        previous_chart_year = add_years(today, -1).strftime("%Y")
        next_chart_year = add_years(today, 1).strftime("%Y")
        chart_year = today.strftime("%Y")
        epochmilliseconds = round(
            int(
                (
                    datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)
                ).total_seconds()
                * 1000
            )
        )
        client_date = datetime.date.today().strftime("%Y-%m-%d")

        for plant in plant_info["plantList"]:
            #
            # NOTE : This URL now takes a sinle inverter, but it should somehow take a list
            #
            # deviceSnArr={plant['plantDetail']['snList'][0]  <<== Is correct if there is only one inverter in the system
            #
            url = f"{BASE_URL_WEB}/monitor/site/getPlantDetailChart2?plantuid={plant['plantuid']}&chartDateType=1&energyType=0&clientDate={client_date}&deviceSnArr={plant['plantDetail']['snList'][0]}&chartCountType=2&previousChartDay={previous_chart_day}&nextChartDay={next_chart_day}&chartDay={chart_day}&previousChartMonth={previous_chart_month}&nextChartMonth={next_chart_month}&chartMonth={chart_month}&previousChartYear={previous_chart_year}&nextChartYear={next_chart_year}&chartYear={chart_year}&elecDevicesn=&_={epochmilliseconds}"
            response = session.post(url, timeout=WEB_TIMEOUT)
            response.raise_for_status()
            plant_chart = response.json()
            if (plant_chart["type"]) == 0:
                plant.update({"peakPower": plant_chart["peakPower"]})
            elif (plant_chart["type"]) == 1:
                plant.update({"viewBean": plant_chart["viewBean"]})

    except requests.exceptions.HTTPError as errh:
        raise requests.exceptions.HTTPError(errh)
    except requests.exceptions.ConnectionError as errc:
        raise requests.exceptions.ConnectionError(errc)
    except requests.exceptions.Timeout as errt:
        raise requests.exceptions.Timeout(errt)
    except requests.exceptions.RequestException as errr:
        raise requests.exceptions.RequestException(errr)


def web_get_device_page_list(session, plant_info, use_pv_grid_attributes):
    """
    Function to retrieve platUid from WEB Portal, requires web_authenticate
    """
    if session is None:
        raise ValueError("Missing session identifier trying to obain plants")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    try:
        chart_month = datetime.date.today().strftime("%Y-%m")
        url = f"{BASE_URL_WEB}/cloudMonitor/device/findDevicePageList"
        payload = f"officeId=&pageNo=&pageSize=&orderName=1&orderType=2&plantuid=&deviceStatus=&localDate={datetime.date.today().strftime('%Y-%m-%d')}&localMonth={chart_month}"

        response = session.post(
            url=f"{BASE_URL_WEB}/cloudMonitor/device/findDevicePageList",
            data=payload,
            timeout=WEB_TIMEOUT,
        )
        response.raise_for_status()
        device_list = response.json()["list"]
        if use_pv_grid_attributes:
            for device in device_list:
                url = f"{BASE_URL_WEB}/cloudMonitor/deviceInfo/findRawdataPageList"
                payload = f"deviceSn={device['devicesn']}&deviceType=0&timeStr={datetime.date.today().strftime('%Y-%m-%d')}"
                response = session.post(
                    url, headers=headers, data=payload, timeout=WEB_TIMEOUT
                )
                response.raise_for_status()
                kit = response.json()
                if len(kit["list"]) > 0:
                    device.update({"findRawdataPageList": kit["list"][0]})
                else:
                    device.update({"findRawdataPageList": None})

        for plant in plant_info["plantList"]:
            kit = []
            for device in device_list:
                if device["devicesn"] in plant["plantDetail"]["snList"]:
                    kit.append(device)

                    # Fetch battery for H1 system (UNTESTED CODE)
                    # print(f'Plant UID: {plant["plantuid"]}')
                    # print(f'Device SN:  {device["devicesn"]}')
                    # print(f'Plant type: {plant["type"]}\n')
                    if plant["type"] == 3:
                        # print("Fetching storage information...")
                        epochmilliseconds = round(
                            int(
                                (
                                    datetime.datetime.utcnow()
                                    - datetime.datetime(1970, 1, 1)
                                ).total_seconds()
                                * 1000
                            )
                        )
                        url = f"{BASE_URL_WEB}/monitor/site/getStoreOrAcDevicePowerInfo"
                        payload = f"plantuid={plant['plantuid']}&devicesn={device['devicesn']}&_={epochmilliseconds}"
                        # print(f"Fetching URL    : {url}")
                        # print(f"Fetching Payload: {payload}")
                        response = session.post(
                            url, headers=headers, data=payload, timeout=WEB_TIMEOUT
                        )
                        response.raise_for_status()
                        store_device_power = response.json()
                        # print("Response:")
                        # print("---------")
                        # print(store_device_power)
                        device.update(store_device_power)

            plant.update({"kitList": kit})

    except requests.exceptions.HTTPError as errh:
        raise requests.exceptions.HTTPError(errh)
    except requests.exceptions.ConnectionError as errc:
        raise requests.exceptions.ConnectionError(errc)
    except requests.exceptions.Timeout as errt:
        raise requests.exceptions.Timeout(errt)
    except requests.exceptions.RequestException as errr:
        raise requests.exceptions.RequestException(errr)
