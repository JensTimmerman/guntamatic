This python module allows you to contact your Guntamatic BMK heater and get operational status information
It includes an example binary 'heater.py' which can be installed as the guntamatic binary to instantly get data in your cli.
The Guntamatic class can be used by IOT frameworks to be called regularly and plot data and the like.

The exact outputs might depend on your model and firmware.


## release history
- 1.0.1: don't generate an empty sensor as last line, skip empty lines
- 1.0.2: update homepage
- 1.0.3: clean up repo
- 1.1.0: Add a parse_data function that does translations and skips diagnostic values. We now only return relevant values that have a hardcoded description.
- 1.2.0: Raise an exception in parse_data if no Serial was present
- 1.3.0: Always return all default sensors, even if they have None as value
- 1.4.0: Translate to snake_case; Home Assistant prefers this, they are easier to split if you need to migrate.
- 1.5.0: Translate known values to snake_case as well

## tests
PYTHONPATH=. pytest tests/test_heater.py

## roadmap
Currently this library only uses daqdata.cgi and dacdesc.cgi
There is also a status.cgi json interface, and probably a lot more is possible when you have an api key (https://github.com/openhab/openhab-addons/tree/main/bundles/org.openhab.binding.guntamatic )
To be added in the future.

par.cgi returns a full list of internal parameters

?key=$KEY parameter should give you more options according to rumors
You can get the key for your boiler from guntamatic tech Support.

ext/daqdesc.cgi?key=<key> should give this in json format according to rummors.
https://github.com/wolfgangr/guntaPERL


## Example Data

The following sensors are available for a Guntamatic BMK 20 heater:

| Sensor | Value | Unit |
|--------|-------|------|
| Running | Service Ign. | |
| Boiler temperature | 14.09 | °C |
| Outside Temp. | 16.15 | °C |
| Buffer load. | 22 | % |
| Buffer Top | 44.56 | °C |
| Buffer Mid | 43.48 | °C |
| Buffer Btm | 34.01 | °C |
| Boil.shunt pump | 0 | % |
| Suction fun | 0.00 | % |
| Primary air | 0.00 | % |
| Seconday air | 0.00 | % |
| CO2 Content | 18.05 | % |
| DHW 0 | 44.50 | °C |
| DHW Pump 0 | 0 | % |
| DHW 1 | -20.00 | °C |
| DHW Pump 1 | 0 | % |
| DHW 2 | -20.00 | °C |
| DHW Pump 2 | 0 | % |
| Heating circulation pump 0 | OFF | |
| Room Temp:HC 0 | 60.00 | °C |
| Room Temp:HC 1 | 24.68 | °C |
| Flow is 1 | 18.61 | °C |
| Heating circulation pump 1 | OFF | |
| Room Temp:HC 2 | 21.77 | °C |
| Flow is 2 | 17.72 | °C |
| Heating circulation pump 2 | OFF | |
| Heating circulation pump 3 | OFF | |
| Room Temp:HC 3 | -9.00 | °C |
| Room Temp:HC 4 | -9.00 | °C |
| Flow is 4 | -20.00 | °C |
| Heating circulation pump 4 | OFF | |
| Room Temp:HC 5 | -9.00 | °C |
| Flow is 5 | 44.00 | °C |
| Heating circulation pump 5 | OFF | |
| Heating circulation pump 6 | OFF | |
| Room Temp:HC 6 | -9.00 | °C |
| Room Temp:HC 7 | -9.00 | °C |
| Flow is 7 | -20.00 | °C |
| Heating circulation pump 7 | OFF | |
| Room Temp:HC 8 | -9.00 | °C |
| Flow is 8 | 44.00 | °C |
| Heating circulation pump 8 | OFF | |
| Program | HEAT | |
| Program HC0 | OFF | |
| Program HC1 | OFF | |
| Program HC2 | HEAT | |
| Program HC3 | OFF | |
| Program HC4 | OFF | |
| Program HC5 | OFF | |
| Program HC6 | OFF | |
| Program HC7 | OFF | |
| Program HC8 | OFF | |
| Interuption 1 | | |
| Interuption 2 | | |
| Serial | 959103 | |
| Version | 32a | |
| Operat. time | 1122 | h |
| Service Hrs | 1876 | d |
| extra-WW. 1 | -20.00 | °C |
| extra-WW. 2 | -20.00 | °C |
| B extra-WW. 0 | OFF | |
| B extra-WW. 1 | OFF | |
| B extra-WW. 2 | OFF | |
| Flow is 0 | 44.00 | °C |
| Flow is 3 | 44.00 | °C |
| Flow is 6 | 44.00 | °C |
| Buffer Top 0 | -20.00 | °C |
| Buffer Btm 0 | -20.00 | °C |
| Buffer Top 1 | -20.00 | °C |
| Buffer Btm 1 | -20.00 | °C |
| Buffer Top 2 | -20.00 | °C |
| Buffer Btm 2 | -20.00 | °C |
| Auxiliary pump 0 | OFF | |
| Auxiliary pump 1 | OFF | |
| Auxiliary pump 2 | OFF | |

> Note: Sensors with a value of `-20.00 °C` are typically not connected.
