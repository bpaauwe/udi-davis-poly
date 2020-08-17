
# Davis Weatherlink polyglot

This is the Davis WeatherLink Poly for the [Universal Devices ISY994i](https://www.universal-devices.com/residential/ISY) [Polyglot interface](http://www.universal-devices.com/developers/polyglot/docs/) with  [Polyglot V2](https://github.com/Einstein42/udi-polyglotv2) or [Polisy](https://www.universal-devices.com/product/polisy/)
(c) 2020 Robert Paauwe
MIT license.

This node server is intended to support [Davis Weather Stations](http://www.davisinstruments.com/).  This is for use with the WeatherLinkIP, the Serial/USB Data Logger with the WeatherLink Computer Software, or the Vantage Connect weather station solutions.  [API documentation](https://www.weatherlink.com/static/docs/APIdocumentation.pdf). 

## Installation

1. Backup Your ISY in case of problems!
   * Really, do the backup, please
2. Go to the Polyglot Store in the UI and install the Davis WeatherLink node server.
3. From the Polyglot menu, Add NodeServer in Polyglot Web
4. From the Polyglot dashboard, select DavisWeatherLink node server and configure (see configuration options below).
5. Once configured, the DavisWeatherLink node server should update the ISY with the proper nodes and begin filling in the node data. Note that it can take up to 1 minute for data to appear.
6. Restart the Admin Console so that it can properly display the new node server nodes.

### Node Settings
The settings for this node are:

#### Short Poll
   * How often to poll the Davis server
#### Long Poll
   * Sends a heartbeat as DON/DOF
#### Token
   * Your token that allows access to the data at api.weatherlink.com
#### Device ID
   * Your device id (mac address without colons) that allows access to the data at api.wetherlink.com
#### Password
   * Your password that allows access to the data at api.wetherlink.com
#### Units
   * Display data in either 'metric', 'us' units. Note that day, month, year observations are only available in 'us' units per documentation.
#### Station
   * The Davis station ID. Not currently used.


## Requirements

1. Polyglot V2 itself should be run on Raspian Stretch.
  To check your version, ```cat /etc/os-release``` and the first line should look like
  ```PRETTY_NAME="Raspbian GNU/Linux 9 (stretch)"```. It is possible to upgrade from Jessie to
  Stretch, but I would recommend just re-imaging the SD card.  Some helpful links:
   * https://www.raspberrypi.org/blog/raspbian-stretch/
   * https://linuxconfig.org/raspbian-gnu-linux-upgrade-from-jessie-to-raspbian-stretch-9
2. ISY firmware 5.0.x or later.

# Upgrading

Open the Polyglot web page, go to nodeserver store and click "Update" for "DavisWeatherLink".

Then restart the DavisWeatherLink nodeserver by selecting it in the Polyglot dashboard and select Control -> Restart, then watch the log to make sure everything goes well.

The DavisWeatherLink nodeserver keeps track of the version number and when a profile rebuild is necessary.  The profile/version.txt will contain the DavisWeatherLink profile_version which is updated in server.json when the profile should be rebuilt.

# Release Notes

- 1.0.5 08/17/2020
   - Don't use the request results in the error message when request fails
- 1.0.4 08/04/2020
   - Changed "User" to "Device ID" as that represents what configuration is really needed.
- 1.0.3 07/05/2020
   - Remove call to set_hub_timestamp since it doesn't exist and causes error.
- 1.0.2 04/05/2020
   - Add a bunch of error checking.
- 1.0.1 04/05/2020
   - Add some additional error reporting to query failures.
- 1.0.0 04/04/2020
   - Initial version published to github
