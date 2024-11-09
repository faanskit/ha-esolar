"""ESolar Basic Test Data."""


def web_get_plant_static_h1_r5():
    """SAJ eSolar Data Update - STATIC PLANT H1 + R5."""
    plant_info = {
        "pageNo": 1,
        "pageSize": 10,
        "plantList": [
            {
                "plantuid": "99999999-9999-9999-9999-999999999999",
                "plantname": "R5 Solar Inverter System",
                "systempower": 5.6,
                "currency": "\u20ac",
                "type": 0,
                "installername": "",
                "countryCode": "DK",
                "country": "Denmark",
                "province": "",
                "city": "",
                "county": "",
                "foreignRemark": "",
                "address": "",
                "latitude": 54.7897259,
                "longitude": 15.0732433,
                "createDateStr": "2022-03-12 09:47:27",
                "isOnline": "Y",
                "runningState": 1,
                "nowPower": 477.0,
                "todayElectricity": 2.48,
                "totalElectricity": 5771.17,
                "enableEdit": "Y",
                "enableDelete": "Y",
                "enableVisitor": "Y",
                "isFavorite": "0",
                "isRename": 0,
                "isMulBind": 0,
                "isTimeError": 0,
            },
            {
                "plantuid": "88888888-8888-8888-8888-888888888888",
                "plantname": "H1 Battery Inverter System",
                "systempower": 3.0,
                "currency": "$",
                "type": 3,
                "installername": "",
                "countryCode": "DK",
                "country": "Denmark",
                "city": "",
                "county": "",
                "foreignRemark": "",
                "address": "***HIDDEN***",
                "createDateStr": "2022-02-24 11:07:18",
                "isOnline": "Y",
                "runningState": 1,
                "nowPower": 647.0,
                "todayElectricity": 2.35,
                "totalElectricity": 5432.08,
                "enableEdit": "N",
                "enableDelete": "N",
                "enableVisitor": "N",
                "isFavorite": "0",
                "isRename": 0,
                "isMulBind": 0,
                "isTimeError": 0,
            },
        ],
        "pageHtml": '<ul>\n<li class="disabled"><a href="javascript:;">« Previous</a></li>\n<li class="active"><a href="javascript:;">1</a></li>\n<li class="disabled"><a href="javascript:;">Next »</a></li>\n<li class="disabled controls pageC">Page <input type="text" value="1" onkeypress="var e=window.event||event;var c=e.keyCode||e.which;if(c==13)page(this.value,10,\'\');" onclick="this.select();"/> Total 2 Records</ul>\n<div style="clear:both;"></div>',
        "status": "success",
    }
    return plant_info


def get_esolar_data_static_h1_r5(
    region, username, password, plant_list, use_pv_grid_attributes
):
    """SAJ eSolar Data Update - STATIC #3 TEST VERSION."""
    plant_info = {
        "pageNo": 1,
        "pageSize": 10,
        "plantList": [
            {
                "plantuid": "99999999-9999-9999-9999-999999999999",
                "plantname": "R5 Solar Inverter System",
                "systempower": 5.6,
                "currency": "\u20ac",
                "type": 0,
                "installername": "",
                "countryCode": "DK",
                "country": "Denmark",
                "province": "",
                "city": "",
                "county": "",
                "foreignRemark": "",
                "address": "",
                "latitude": 54.7897259,
                "longitude": 15.0732433,
                "createDateStr": "2022-03-12 09:47:27",
                "isOnline": "N",
                "runningState": 3,
                "nowPower": 0.0,
                "todayElectricity": 0.77,
                "totalElectricity": 5835.27,
                "enableEdit": "Y",
                "enableDelete": "Y",
                "enableVisitor": "Y",
                "isFavorite": "0",
                "isRename": 0,
                "isMulBind": 0,
                "isTimeError": 0,
                "plantDetail": {
                    "type": 0,
                    "runningState": 3,
                    "nowPower": 0.0,
                    "todayElectricity": 0.77,
                    "monthElectricity": 11.81,
                    "yearElectricity": 5835.27,
                    "totalElectricity": 5835.27,
                    "income": 2042.34,
                    "todayGridIncome": 0.27,
                    "devOnlineNum": 0,
                    "devTotalNum": 1,
                    "totalPlantTreeNum": 10.35,
                    "totalReduceCo2": 5.82,
                    "todayAlarmNum": 0,
                    "lastUploadTime": "2022-12-04 16:19:42",
                    "userType": 2,
                    "snList": ["R59999999999999999"],
                    "energyCompareYearList": ["2022"],
                },
                "status": "success",
                "peakList": [{"devicesn": "R59999999999999999", "peakPower": 289.0}],
                "kitList": [
                    {
                        "invType": "",
                        "kitType": "N/A",
                        "monthSellEnergyStr": "11.81",
                        "todaySellEnergy": 0.77,
                        "kitSn": "M539999999999999",
                        "updateDateStr": "2022-12-04 23:19:42",
                        "ifShowAFCI": 0,
                        "powernower": "N/A",
                        "mastermcufw": "V1.188",
                        "type": 0,
                        "devicetype": "R5-5K-S2",
                        "onLineStr": "3",
                        "displayfw": "V2.068",
                        "devicepc": "0202999999EN999999",
                        "powernow": 0.0,
                        "isShowBattery": 1,
                        "owner": "N/A",
                        "todaySellEnergyStr": "0.77",
                        "index": 0,
                        "monthSellEnergy": 11.81,
                        "devicesn": "R59999999999999999",
                        "userId": "abd1234e-9999-9999-9999-999999999999",
                        "onLine": 0,
                        "slavemcufw": "V1.188",
                        "isModuleExpire": 0,
                        "totalSellEnergy": 5835.27,
                        "totalSellEnergyStr": "5,835.27",
                        "isShowHighVoltBat": 0,
                        "isHistory": 0,
                        "mark": 1,
                        "plantName": "N/A",
                        "dataTimeStr": "2022-12-04 16:20:00",
                        "findRawdataPageList": {
                            "nowPrower": 0.0,
                            "rOutPowerWattStr": "N/A",
                            "batPower": 0.0,
                            "rBackupPowerWatt": 0.0,
                            "pV3StrCurr1Str": "N/A",
                            "timeStart": "null 00:00:00",
                            "pV4Curr": 0.0,
                            "currSelfConsumePowerStr": "0",
                            "rOutVolt": 0.0,
                            "totalPVEnergy": 5835.27,
                            "tOutVolt": 0.0,
                            "createTimeStr": "2022-12-04 23:19:42",
                            "deviceType": 0,
                            "pV4StrCurr2Str": "N/A",
                            "pv3SeriesCurrent": "0.0-0.0-N/A-N/A",
                            "rGridFreqStr": "49.97",
                            "totalBatDisEnergy": 0.0,
                            "tOutFreqStr": "N/A",
                            "sGridPowerWattStr": "N/A",
                            "totalBatChgEnergy": 0.0,
                            "isAdmin": "N",
                            "pV1StrCurr4": 0.0,
                            "pV1StrCurr3": 0.0,
                            "pV1StrCurr2": 0.0,
                            "pV1StrCurr1": 0.0,
                            "pv2SeriesCurrent": "0.0-0.0-N/A-N/A",
                            "POP": 0.0,
                            "RST": 1,
                            "pvInputMode": "0",
                            "rGridFreq": 49.97,
                            "sGridFreqStr": "N/A",
                            "sGridVoltStr": "N/A",
                            "tOutPowerVAStr": "0",
                            "pV4VoltStr": "N/A",
                            "batEnergyPercent": 0.0,
                            "backupTotalLoadPowerWatt": 0.0,
                            "tableStoreTimeEnd": "",
                            "tOutVoltStr": "N/A",
                            "rGridVoltStr": "235",
                            "batVoltStr": "N/A",
                            "tGridCurrStr": "N/A",
                            "rGridCurr": 0.13,
                            "rOutFreqStr": "N/A",
                            "userId": "",
                            "partitionName": "",
                            "sGridVolt": 0.0,
                            "pV3PowerStr": "N/A",
                            "tOnGridOutVolt": 0.0,
                            "tGridPowerWattStr": "0",
                            "pV2StrCurr4Str": "N/A",
                            "ctPVPowerWattStr": "N/A",
                            "pV4StrCurr3Str": "N/A",
                            "tOutPowerWatt": 0.0,
                            "pV3Power": 0.0,
                            "pV1CurrStr": "0",
                            "pV2CurrStr": "0",
                            "pV4CurrStr": "N/A",
                            "onLineStr": "N",
                            "pV2Power": 0.0,
                            "todayBatDisEnergy": 0.0,
                            "pac": 0.0,
                            "officeId": "",
                            "rOutPowerWatt": 0.0,
                            "pacStr": "0",
                            "powernow": 0.0,
                            "ctPvCurr": 0.0,
                            "tGridVoltStr": "N/A",
                            "powerNower": "N/A",
                            "pvChannelList": [],
                            "pv1SeriesCurrent": "0.0-0.0-N/A-N/A",
                            "pV1Power": 0.0,
                            "pV4Volt": 0.0,
                            "pV3StrCurr2Str": "N/A",
                            "deviceTempStr": "18.5",
                            "rOutCurr": 0.0,
                            "tOutCurr": 0.0,
                            "todayFeedInEnergyStr": "N/A",
                            "totalPVEnergyStr": "5,835.27",
                            "pV3Curr": 0.0,
                            "sOnGridOutPowerWatt": 0.0,
                            "tGridFreqStr": "N/A",
                            "todayBatChgEnergy": 0.0,
                            "pV1StrCurr1Str": "N/A",
                            "tGridFreq": 0.0,
                            "totalFeedInEnergy": 0.0,
                            "sOutPowerVAStr": "0",
                            "gridDirection": 0,
                            "batCurrStr": "0.0",
                            "powerNow": 0.0,
                            "rOutPowerVA": 0.0,
                            "kitType": "N/A",
                            "pV1VoltStr": "250",
                            "todayLoadEnergy": 0.0,
                            "sOutPowerWattStr": "N/A",
                            "pV4StrCurr1": 0.0,
                            "sGridPowerVA": 0.0,
                            "pV4StrCurr2": 0.0,
                            "pV4StrCurr3": 0.0,
                            "pV4StrCurr4": 0.0,
                            "sOutPowerVA": 0.0,
                            "batType": "",
                            "pV3Volt": 0.0,
                            "rGridPowerVAStr": "N/A",
                            "tGridPowerVAStr": "N/A",
                            "tGridCurr": 0.0,
                            "rOnGridOutFreq": 0.0,
                            "pV4StrCurr4Str": "N/A",
                            "tOutFreq": 0.0,
                            "todayPVEnergy": 0.77,
                            "tGridPowerWatt": 0.0,
                            "sGridPowerVAStr": "N/A",
                            "tOutCurrStr": "0.0",
                            "ctPvCurrStr": "0",
                            "pV2Curr": 0.0,
                            "totalLoadEnergy": 0.0,
                            "pV2PowerStr": "N/A",
                            "datetimeStr": "2022-12-04 16:20:00",
                            "powernower": "N/A",
                            "PVP": 0.0,
                            "rGridCurrStr": "0.13",
                            "totalLoadPowerWattStr": "N/A",
                            "pV1StrCurr2Str": "N/A",
                            "nowProwerStr": "N/A",
                            "totalLoadEnergyStr": "5,835.27",
                            "sOutVolt": 0.0,
                            "ctGridPowerWattStr": "N/A",
                            "rGridPowerVA": 0.0,
                            "index": 1,
                            "tGridVolt": 0.0,
                            "todayFeedInEnergy": 0.0,
                            "totalBatChgEnergyStr": "N/A",
                            "tOnGridOutPowerWatt": 0.0,
                            "pV3VoltStr": "N/A",
                            "batPowerStr": "N/A",
                            "pV2Volt": 24.4,
                            "deviceSn": "R59999999999999999",
                            "todayPVEnergyStr": "0.77",
                            "pV3StrCurr3Str": "N/A",
                            "rGridPowerWattStr": "0",
                            "batCapicity": "",
                            "sGridCurrStr": "N/A",
                            "sOutCurrStr": "0.0",
                            "pV2StrCurr2": 0.0,
                            "timeEnd": "null 23:59:59",
                            "pV2StrCurr1": 0.0,
                            "pV2StrCurr3Str": "N/A",
                            "tOutPowerWattStr": "N/A",
                            "tOutPowerVA": 0.0,
                            "pV2StrCurr4": 0.0,
                            "pV2StrCurr3": 0.0,
                            "rOutFreq": 0.0,
                            "plantuid": "",
                            "endUser": "",
                            "totalSellEnergy": 0.0,
                            "sGridPowerWatt": 0.0,
                            "pV1StrCurr3Str": "N/A",
                            "rOnGridOutVolt": 0.0,
                            "totalSellEnergyStr": "N/A",
                            "deviceModel": "N/A",
                            "batVolt": 0.0,
                            "todaySellEnergy": 0.0,
                            "totalFeedInEnergyStr": "N/A",
                            "sOutVoltStr": "N/A",
                            "timeStr": "",
                            "pV3CurrStr": "N/A",
                            "pV1Curr": 0.0,
                            "sOutPowerWatt": 0.0,
                            "pV3StrCurr1": 0.0,
                            "pV3StrCurr2": 0.0,
                            "rOnGridOutPowerWatt": 0.0,
                            "pV3StrCurr3": 0.0,
                            "pV3StrCurr4": 0.0,
                            "pv4SeriesCurrent": "N/A-N/A-N/A-N/A",
                            "kitSN": "N/A",
                            "pV2StrCurr1Str": "N/A",
                            "pV4Power": 0.0,
                            "todaySellEnergyStr": "N/A",
                            "sOutFreq": 0.0,
                            "sGridCurr": 0.0,
                            "typeStr": "\u5e76\u7f51\u9006\u53d8\u5668",
                            "rGridVolt": 235.0,
                            "rOutPowerVAStr": "0",
                            "rOutCurrStr": "0.0",
                            "pV4PowerStr": "N/A",
                            "userUid": "",
                            "pV2StrCurr2Str": "N/A",
                            "pV4StrCurr1Str": "N/A",
                            "ctGridPowerWatt": 0.0,
                            "deviceTemp": 18.5,
                            "pV2VoltStr": "24.4",
                            "sOutFreqStr": "N/A",
                            "batCurr": 0.0,
                            "totalBatDisEnergyStr": "N/A",
                            "pV1PowerStr": "0",
                            "batEnergyPercentStr": "N/A",
                            "pV1StrCurr4Str": "N/A",
                            "ctPVPowerWatt": 0.0,
                            "totalLoadPowerWatt": 0.0,
                            "todaySelfConsumpEnergy": 0.0,
                            "rOutVoltStr": "N/A",
                            "todayLoadEnergyStr": "0.77",
                            "rGridPowerWatt": 0.0,
                            "sOutCurr": 0.0,
                            "pV3StrCurr4Str": "N/A",
                            "sGridFreq": 0.0,
                            "tGridPowerVA": 0.0,
                            "meterAStatus": 0,
                            "pV1Volt": 250.0,
                            "sOnGridOutVolt": 0.0,
                            "todaySelfConsumpEnergyStr": "N/A",
                            "plantName": "",
                        },
                    }
                ],
            },
            {
                "plantuid": "88888888-8888-8888-8888-888888888888",
                "plantname": "H1 Battery Inverter System",
                "systempower": 10.0,
                "currency": "$",
                "type": 3,
                "installername": "",
                "countryCode": "DK",
                "country": "Denmark",
                "city": "",
                "county": "",
                "foreignRemark": "",
                "address": "***HIDDEN***",
                "createDateStr": "2022-02-24 11:07:18",
                "isOnline": "Y",
                "runningState": 1,
                "nowPower": 2.0,
                "todayElectricity": 0.63,
                "totalElectricity": 5491.7,
                "enableEdit": "N",
                "enableDelete": "N",
                "enableVisitor": "N",
                "isFavorite": "0",
                "isRename": 0,
                "isMulBind": 0,
                "isTimeError": 0,
                "plantDetail": {
                    "type": 3,
                    "runningState": 1,
                    "nowPower": -2.0,
                    "todayElectricity": 0.63,
                    "monthElectricity": 10.99,
                    "yearElectricity": 5491.7,
                    "totalElectricity": 5491.7,
                    "totalConsumpElec": 2677.7,
                    "totalBuyElec": 703.22,
                    "totalSellElec": 3002.64,
                    "selfUseRate": "45.32%",
                    "devOnlineNum": 1,
                    "devTotalNum": 2,
                    "totalPlantTreeNum": 9.74,
                    "totalReduceCo2": 5.48,
                    "lastUploadTime": "2022-12-04 20:30:42",
                    "userType": 2,
                    "snList": ["ASS999999999999999", "ASS111111111111111"],
                    "energyCompareYearList": ["2021", "2022"],
                },
                "status": "success",
                "beanList": [
                    {
                        "pvElec": 0,
                        "useElec": 0,
                        "buyElec": 0,
                        "sellElec": 0,
                        "chargeElec": 0,
                        "dischargeElec": 0,
                        "buyRate": "0%",
                        "sellRate": "0%",
                        "selfConsumedRate1": "0%",
                        "selfConsumedRate2": "0%",
                        "selfConsumedEnergy1": 0,
                        "selfConsumedEnergy2": 0,
                        "plantTreeNum": 0,
                        "reduceCo2": 0,
                        "devicesn": "ASS999999999999999",
                    },
                    {
                        "pvElec": 0.63,
                        "useElec": 12.55,
                        "buyElec": 12.06,
                        "sellElec": 0.0,
                        "chargeElec": 0.14,
                        "dischargeElec": 0.0,
                        "buyRate": "96.10%",
                        "sellRate": "0%",
                        "selfConsumedRate1": "100%",
                        "selfConsumedRate2": "3.90%",
                        "selfConsumedEnergy1": 0.63,
                        "selfConsumedEnergy2": 0.49,
                        "plantTreeNum": 0.001,
                        "reduceCo2": 0.001,
                        "dataTime": 1670083200000,
                        "devicesn": "ASS111111111111111",
                    },
                ],
                "kitList": [
                    {
                        "invType": "",
                        "kitType": "N/A",
                        "monthSellEnergyStr": "10.99",
                        "todaySellEnergy": 0.0,
                        "kitSn": "N/A",
                        "updateDateStr": "2022-12-05 03:30:42",
                        "ifShowAFCI": 0,
                        "powernower": "2",
                        "mastermcufw": "v5.052",
                        "type": 2,
                        "devicetype": "AS1-3KS-5.1",
                        "onLineStr": "1",
                        "displayfw": "v3.098",
                        "devicepc": "1020666666EN373737",
                        "powernow": 2.0,
                        "isShowBattery": 1,
                        "owner": "N/A",
                        "todaySellEnergyStr": "N/A",
                        "index": 0,
                        "monthSellEnergy": 10.99,
                        "devicesn": "ASS111111111111111",
                        "userId": "abd1234e-9999-9999-9999-999999999999",
                        "onLine": 0,
                        "slavemcufw": "v5.052",
                        "isModuleExpire": 0,
                        "totalSellEnergy": 12.44,
                        "totalSellEnergyStr": "12.44",
                        "isShowHighVoltBat": 0,
                        "isHistory": 0,
                        "mark": 1,
                        "plantName": "N/A",
                        "dataTimeStr": "2022-12-04 20:30:00",
                        "findRawdataPageList": {
                            "nowPrower": -2.0,
                            "rOutPowerWattStr": "1,186",
                            "batPower": 0.0,
                            "rBackupPowerWatt": 0.0,
                            "pV3StrCurr1Str": "N/A",
                            "timeStart": "null 00:00:00",
                            "pV4Curr": 0.0,
                            "currSelfConsumePowerStr": "146",
                            "rOutVolt": 233.3,
                            "totalPVEnergy": 12.44,
                            "tOutVolt": 0.0,
                            "createTimeStr": "2022-12-05 03:30:42",
                            "deviceType": 2,
                            "pV4StrCurr2Str": "N/A",
                            "pv3SeriesCurrent": "0.0-0.0-0.0-0.0",
                            "rGridFreqStr": "49.97",
                            "totalBatDisEnergy": 3.94,
                            "tOutFreqStr": "0",
                            "sGridPowerWattStr": "0",
                            "totalBatChgEnergy": 4.95,
                            "isAdmin": "N",
                            "pV1StrCurr4": 0.0,
                            "pV1StrCurr3": 0.0,
                            "pV1StrCurr2": 0.0,
                            "pV1StrCurr1": 0.0,
                            "pv2SeriesCurrent": "0.0-0.0-0.0-0.0",
                            "POP": 0.0,
                            "RST": 1,
                            "pvInputMode": "0",
                            "rGridFreq": 49.97,
                            "sGridFreqStr": "0",
                            "sGridVoltStr": "0",
                            "tOutPowerVAStr": "0",
                            "pV4VoltStr": "N/A",
                            "batEnergyPercent": 7.0,
                            "backupTotalLoadPowerWatt": 0.0,
                            "tableStoreTimeEnd": "",
                            "tOutVoltStr": "0",
                            "rGridVoltStr": "232.8",
                            "batVoltStr": "50.3",
                            "tGridCurrStr": "0.0",
                            "rGridCurr": -0.35,
                            "rOutFreqStr": "49.97",
                            "userId": "",
                            "partitionName": "",
                            "sGridVolt": 0.0,
                            "pV3PowerStr": "0",
                            "tOnGridOutVolt": 0.0,
                            "tGridPowerWattStr": "0",
                            "pV2StrCurr4Str": "N/A",
                            "ctPVPowerWattStr": "N/A",
                            "pV4StrCurr3Str": "N/A",
                            "tOutPowerWatt": 0.0,
                            "pV3Power": 0.0,
                            "pV1CurrStr": "0.0",
                            "pV2CurrStr": "0.0",
                            "pV4CurrStr": "0.0",
                            "onLineStr": "Y",
                            "pV2Power": 0.0,
                            "todayBatDisEnergy": 0.0,
                            "pac": 0.0,
                            "officeId": "",
                            "rOutPowerWatt": 1186.0,
                            "pacStr": "0",
                            "powernow": 0.0,
                            "ctPvCurr": 0.0,
                            "tGridVoltStr": "0",
                            "powerNower": "N/A",
                            "pvChannelList": [],
                            "pv1SeriesCurrent": "0.0-0.0-0.0-0.0",
                            "pV1Power": -1.0,
                            "pV4Volt": 0.0,
                            "pV3StrCurr2Str": "N/A",
                            "deviceTempStr": "N/A",
                            "rOutCurr": 0.63,
                            "tOutCurr": 0.0,
                            "todayFeedInEnergyStr": "12.06",
                            "totalPVEnergyStr": "12.44",
                            "pV3Curr": 0.0,
                            "sOnGridOutPowerWatt": 0.0,
                            "tGridFreqStr": "0",
                            "todayBatChgEnergy": 0.14,
                            "pV1StrCurr1Str": "N/A",
                            "tGridFreq": 0.0,
                            "totalFeedInEnergy": 49.79,
                            "sOutPowerVAStr": "0",
                            "gridDirection": -1,
                            "batCurrStr": "0.0",
                            "powerNow": 0.0,
                            "rOutPowerVA": 146.0,
                            "kitType": "N/A",
                            "pV1VoltStr": "236.5",
                            "todayLoadEnergy": 12.58,
                            "sOutPowerWattStr": "0",
                            "pV4StrCurr1": 0.0,
                            "sGridPowerVA": 0.0,
                            "pV4StrCurr2": 0.0,
                            "pV4StrCurr3": 0.0,
                            "pV4StrCurr4": 0.0,
                            "sOutPowerVA": 0.0,
                            "batType": "1",
                            "pV3Volt": 0.0,
                            "rGridPowerVAStr": "81",
                            "tGridPowerVAStr": "0",
                            "tGridCurr": 0.0,
                            "rOnGridOutFreq": 49.97,
                            "pV4StrCurr4Str": "N/A",
                            "tOutFreq": 0.0,
                            "todayPVEnergy": 0.63,
                            "tGridPowerWatt": 0.0,
                            "sGridPowerVAStr": "0",
                            "tOutCurrStr": "0.0",
                            "ctPvCurrStr": "0",
                            "pV2Curr": 0.0,
                            "totalLoadEnergy": 60.42,
                            "pV2PowerStr": "0",
                            "datetimeStr": "2022-12-04 20:30:00",
                            "powernower": "N/A",
                            "PVP": -1.0,
                            "rGridCurrStr": "0.0",
                            "totalLoadPowerWattStr": "1,186",
                            "pV1StrCurr2Str": "N/A",
                            "nowProwerStr": "-2",
                            "totalLoadEnergyStr": "60.45",
                            "sOutVolt": 0.0,
                            "ctGridPowerWattStr": "N/A",
                            "rGridPowerVA": 81.0,
                            "index": 1,
                            "tGridVolt": 0.0,
                            "todayFeedInEnergy": 12.06,
                            "totalBatChgEnergyStr": "4.95",
                            "tOnGridOutPowerWatt": 0.0,
                            "pV3VoltStr": "0",
                            "batPowerStr": "0",
                            "pV2Volt": 0.0,
                            "deviceSn": "ASS111111111111111",
                            "todayPVEnergyStr": "0.63",
                            "pV3StrCurr3Str": "N/A",
                            "rGridPowerWattStr": "0",
                            "batCapicity": "100.00",
                            "sGridCurrStr": "0.0",
                            "sOutCurrStr": "0.0",
                            "pV2StrCurr2": 0.0,
                            "timeEnd": "null 23:59:59",
                            "pV2StrCurr1": 0.0,
                            "pV2StrCurr3Str": "N/A",
                            "tOutPowerWattStr": "0",
                            "tOutPowerVA": 0.0,
                            "pV2StrCurr4": 0.0,
                            "pV2StrCurr3": 0.0,
                            "rOutFreq": 49.97,
                            "plantuid": "",
                            "endUser": "",
                            "totalSellEnergy": 0.77,
                            "sGridPowerWatt": 0.0,
                            "pV1StrCurr3Str": "N/A",
                            "rOnGridOutVolt": 232.8,
                            "totalSellEnergyStr": "0.77",
                            "deviceModel": "AS1-3KS-5.1",
                            "batVolt": 50.3,
                            "todaySellEnergy": 0.0,
                            "totalFeedInEnergyStr": "49.79",
                            "sOutVoltStr": "0",
                            "timeStr": "",
                            "pV3CurrStr": "0.0",
                            "pV1Curr": 0.04,
                            "sOutPowerWatt": 0.0,
                            "pV3StrCurr1": 0.0,
                            "pV3StrCurr2": 0.0,
                            "rOnGridOutPowerWatt": 1186.0,
                            "pV3StrCurr3": 0.0,
                            "pV3StrCurr4": 0.0,
                            "pv4SeriesCurrent": "0.0-0.0-N/A-N/A",
                            "kitSN": "M5380G2122007045",
                            "pV2StrCurr1Str": "N/A",
                            "pV4Power": 0.0,
                            "todaySellEnergyStr": "0",
                            "sOutFreq": 0.0,
                            "sGridCurr": 0.0,
                            "typeStr": "\u5e76\u7f51\u9006\u53d8\u5668",
                            "rGridVolt": 232.8,
                            "rOutPowerVAStr": "146",
                            "rOutCurrStr": "5.08",
                            "pV4PowerStr": "N/A",
                            "userUid": "",
                            "pV2StrCurr2Str": "N/A",
                            "pV4StrCurr1Str": "N/A",
                            "ctGridPowerWatt": 0.0,
                            "deviceTemp": 0.0,
                            "pV2VoltStr": "0",
                            "sOutFreqStr": "0",
                            "batCurr": 0.0,
                            "totalBatDisEnergyStr": "3.94",
                            "pV1PowerStr": "-1",
                            "batEnergyPercentStr": "7",
                            "pV1StrCurr4Str": "N/A",
                            "ctPVPowerWatt": 0.0,
                            "totalLoadPowerWatt": 1186.0,
                            "todaySelfConsumpEnergy": 0.0,
                            "rOutVoltStr": "233.3",
                            "todayLoadEnergyStr": "12.55",
                            "rGridPowerWatt": 0.0,
                            "sOutCurr": 0.0,
                            "pV3StrCurr4Str": "N/A",
                            "sGridFreq": 0.0,
                            "tGridPowerVA": 0.0,
                            "meterAStatus": 0,
                            "pV1Volt": 236.5,
                            "sOnGridOutVolt": 0.0,
                            "todaySelfConsumpEnergyStr": "0",
                            "plantName": "",
                        },
                        "storeDevicePower": {
                            "pvPower": 2.0,
                            "gridPower": 1188.0,
                            "inputOutputPower": 0.0,
                            "batteryPower": 0.0,
                            "totalLoadPower": 1190.0,
                            "homeLoadPower": 1186.0,
                            "backupLoadPower": 0.0,
                            "solarPower": 7.0,
                            "batCurr": 0.0,
                            "batEnergyPercent": 7.0,
                            "runningState": 1,
                            "isOnline": 1,
                            "isAlarm": 0,
                            "mark": 1,
                            "batCapcity": 100.0,
                            "batCapcityStr": "100.00Ah",
                            "hasMeter": True,
                            "hasBattery": True,
                            "pvDirection": 1,
                            "gridDirection": -1,
                            "batteryDirection": 0,
                            "outPutDirection": 1,
                            "dataTime": 1670157000000,
                            "updateDate": 1670182242000,
                        },
                        "status": "success",
                    },
                    {
                        "invType": "",
                        "kitType": "N/A",
                        "monthSellEnergyStr": "N/A",
                        "todaySellEnergy": 0.0,
                        "kitSn": "N/A",
                        "updateDateStr": "2022-11-30 16:52:35",
                        "ifShowAFCI": 0,
                        "powernower": "N/A",
                        "mastermcufw": "v5.057",
                        "type": 2,
                        "devicetype": "AS1-3KS-5.1",
                        "onLineStr": "3",
                        "displayfw": "v3.100",
                        "devicepc": "0104999999EN666666",
                        "powernow": 0.0,
                        "isShowBattery": 1,
                        "owner": "N/A",
                        "todaySellEnergyStr": "N/A",
                        "index": 0,
                        "monthSellEnergy": 0.0,
                        "devicesn": "ASS999999999999999",
                        "userId": "abd1234e-9999-9999-9999-999999999999",
                        "onLine": 0,
                        "slavemcufw": "v5.057",
                        "isModuleExpire": 0,
                        "totalSellEnergy": 5479.26,
                        "totalSellEnergyStr": "5,479.26",
                        "isShowHighVoltBat": 0,
                        "isHistory": 0,
                        "mark": 1,
                        "plantName": "N/A",
                        "dataTimeStr": "2022-11-30 09:50:00",
                        "findRawdataPageList": None,
                        "storeDevicePower": {
                            "devicesn": "ASS999999999999999",
                            "pvPower": 0,
                            "gridPower": 0,
                            "inputOutputPower": 0,
                            "batteryPower": 0,
                            "totalLoadPower": 0,
                            "homeLoadPower": 0,
                            "backupLoadPower": 0,
                            "solarPower": 3.0,
                            "batEnergyPercent": 0,
                            "batCapcity": 100,
                            "batCapcityStr": "100Ah",
                            "hasMeter": True,
                            "hasBattery": True,
                            "pvDirection": 0,
                            "gridDirection": 0,
                            "batteryDirection": 0,
                        },
                        "status": "success",
                    },
                ],
            },
        ],
        "pageHtml": '<ul>\n<li class="disabled"><a href="javascript:;">\u00ab Previous</a></li>\n<li class="active"><a href="javascript:;">1</a></li>\n<li class="disabled"><a href="javascript:;">Next \u00bb</a></li>\n<li class="disabled controls pageC">Page <input type="text" value="1" onkeypress="var e=window.event||event;var c=e.keyCode||e.which;if(c==13)page(this.value,10,\'\');" onclick="this.select();"/> Total 2 Records</ul>\n<div style="clear:both;"></div>',
        "status": "success",
    }
    return plant_info
