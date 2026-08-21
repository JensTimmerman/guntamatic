This python module allows you to contact your Guntamatic BMK heater and get operational status information
It includes an example binary 'heater.py' which can be installed as the guntamatic binary to instantly get data in your cli.
The Guntamatic class can be used by IOT frameworks to be called regularly and plot data and the like.

The exact outputs might depend on your model and firmware.


## How parse_data works

`parse_data()` post-processes the raw device output in three steps:

**1. Stable keys.** Field labels are translated from the language configured
on the heater to fixed English snake_case keys, so you always get the same
keys (`boiler_temperature`, `room_1_temperature`, ...) regardless of the
language set on the heater's display.

**2. Canonical enum values.** Known enum values are translated from the
heater's language to canonical English values:

- `program`: `off`, `timer`, `dhw`, `heat`, `hibernate`, `hibernate_to`,
  `dhw_boost`
- heating circuit programs (`heating_circulation_program_x`): `off`, `timer`,
  `heat`, `hibernate`, `hibernate_to`
- pump operating modes (`heating_circulation_pump_x`, `auxiliary_pump_x`,
  `extra_dhw_boost_x`): `auto`, `off`, `nonstop`

Values that are not recognized are passed through unchanged and logged as a
warning.

**3. Placeholder filtering.** Unconfigured slots (e.g. heating circuits that
are not connected) report placeholder temperatures instead of real data.
`parse_data()` removes those sensors together with the diagnostics belonging
to the same slot:

- a placeholder **room temperature** (-9 or 60 °C) hides the entire circuit
  slot: flow temperature, circulation pump and program
- a placeholder **flow temperature** (-20 °C) hides the flow temperature,
  pump and program of that circuit
- a default **DHW temperature** (-20 °C) hides the DHW temperature and its
  pump and boost sensors
- absent **buffer stages** are filtered at -20 and 120 °C

Note: the flow temperature reported for an unused circuit is *not* a stable
placeholder — it tracks process temperatures. Circuits are therefore
considered unconfigured based on their room temperature placeholder.

**4. Service time normalization.** Models report the time before/between
service either in hours or in days depending on firmware. `parse_data()`
always exposes both: `service_days` (`[value, 'd']`) and `service_hours`
(`[value * 24, 'h']`).


## release history
- 1.0.1: don't generate an empty sensor as last line, skip empty lines
- 1.0.2: update homepage
- 1.0.3: clean up repo
- 1.1.0: Add a parse_data function that does translations and skips diagnostic values. We now only return relevant values that have a hardcoded description.
- 1.2.0: Raise an exception in parse_data if no Serial was present
- 1.3.0: Always return all default sensors, even if they have None as value
- 1.4.0: Translate to snake_case; Home Assistant prefers this, they are easier to split if you need to migrate.
- 1.5.0: Translate known values to snake_case as well
- 1.6.0: Add more sensors to get_data, rename domestic home water to domestic hot water
- 1.7.0: Added support for devices in german, french, italian and spanish with mapping to fixed english output, removed supurflious print
- 1.7.1: fix typo
- 1.8.0: more heater language translations (czech, slovenian, hungarian, dutch)
- 1.9.0: filter more placeholder temperatures; use pop with default to avoid KeyErrors on incomplete data
- 1.9.1 - 1.9.3: robustness fixes for incomplete data and looser label matching
- 1.10.0: translate heating circulation programs and pump operating modes to canonical english values in all supported heater languages; reference parameter dumps per language in doc/params/
- 1.11.0: expose the service time normalized as both service_days and service_hours
- 1.11.1: compare placeholder temperatures numerically (49 °C unconnected flows), cascade placeholder filtering from room temperature to the whole circuit slot, never filter realistic boiler/buffer readings

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
> `parse_data()` filters these placeholder slots automatically; the raw data
> from `get_data()` still contains them.
