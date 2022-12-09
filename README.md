# Home Assistant SAJ eSolar Custom Integration
This integration uses cloud polling from the SAJ eSolar portal using reverse engineered private API.

# Installation
### HACS
HACS installation is not yet supported.

### Manual
- Copy directory `custom_components/esolar` to your `<config dir>/custom_components` directory.
- Restart Home-Assistant.

## Enable the integration
Go to Settings / Devices & Services / Integrations. Click + ADD INTERATION

![alt text](https://github.com/faanskit/ha-esolar/blob/main/images/setup_step_1.png)

Search for eSolar and click on it

![alt text](https://github.com/faanskit/ha-esolar/blob/main/images/setup_step_2.png)

Enter your SAJ eSolar username and password

![alt text](https://github.com/faanskit/ha-esolar/blob/main/images/setup_step_3.png)

If you have more than one site, select which sites that shall be installed

![alt text](https://github.com/faanskit/ha-esolar/blob/main/images/setup_step_4.png)

Following a succesful installation, a device per plant will be created

![alt text](https://github.com/faanskit/ha-esolar/blob/main/images/setup_step_5.png)

You can see that a number of devices and entites has been created at the SAJ eSolar integration

![alt text](https://github.com/faanskit/ha-esolar/blob/main/images/setup_done_1.PNG)

If you click on the devices, you can see this also in the Devices section

![alt text](https://github.com/faanskit/ha-esolar/blob/main/images/setup_done_2.png)

Your home screen will now have a number of new entities depending on your system. A R5 system will have two sensors (Status and Energy) and a H1 System will have five sensors (Status, Sell Energy, Buy, Energy, Charge Energy, Discharge Energy)

![alt text](https://github.com/faanskit/ha-esolar/blob/main/images/setup_done_3.png)

## Configuration
If you need more sensor and more detailed attributes in the sensors, you can configure the integration as follows
Go to Settings / Devices & Services / SAL eSola. Click CONFIGURE.
Select if you want additional inverter sensors and if you want Photovoltaics and Grid attributes.
Take note that the Photovoltaics and Grid attributes will pull additional data from the SAJ servers.

![alt text](https://github.com/faanskit/ha-esolar/blob/main/images/configure_step_1.png)

After the configuration is done, you need to restart the integration. Click ... and select Reload

![alt text](https://github.com/faanskit/ha-esolar/blob/main/images/configure_step_2.png)

The system will now reload and add two new sensors per inverter (Energy Total and Power)

![alt text](https://github.com/faanskit/ha-esolar/blob/main/images/configure_step_3.png)

## Final result
When the system is fully set-up it can look something like this

![alt text](https://github.com/faanskit/ha-esolar/blob/main/images/all_done.png)
