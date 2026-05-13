"""
This module implements the functionality to contact a guntamatic wood heater e.g. BMK 20
"""

import logging
import sys

import requests

PROTOCOL = 'http://'

DESCURL = 'daqdesc.cgi'
DATAURL = 'daqdata.cgi'

RESERVED = 'reserved'
SERIAL = 'Serial'

# List of sensors we want to always give
SENSORS = [
    "Running",
    "Boiler temperature",
    "Outside Temp.",
    "Buffer load.",
    "Buffer Top",
    "Buffer Mid",
    "Buffer Btm",
    "DHW 0",
    "Room Temp:HC 0",
    "Room Temp:HC 1",
    "Room Temp:HC 2",
    "Program",
    SERIAL,
    "Version",
    "Boil.shunt pump",
    "Suction fun",
    "Primary air",
    "Seconday air",
    "CO2 Content",
    "DHW Pump 0",
    "DHW 1",
    "DHW Pump 1",
    "DHW 2",
    "DHW Pump 2",
    "Heating circulation pump 0",
    "Flow is 0",
    "Flow is 1",
    "Heating circulation pump 1",
    "Flow is 2",
    "Heating circulation pump 2",
    "Heating circulation pump 3",
    "Flow is 3",
    "Room Temp:HC 3",
    "Room Temp:HC 4",
    "Flow is 4",
    "Heating circulation pump 4",
    "Room Temp:HC 5",
    "Flow is 5",
    "Heating circulation pump 5",
    "Heating circulation pump 6",
    "Room Temp:HC 6",
    "Flow is 6",
    "Room Temp:HC 7",
    "Flow is 7",
    "Heating circulation pump 7",
    "Room Temp:HC 8",
    "Flow is 8",
    "Heating circulation pump 8",
    "Program HC0",
    "Program HC1",
    "Program HC2",
    "Program HC3",
    "Program HC4",
    "Program HC5",
    "Program HC6",
    "Program HC7",
    "Program HC8",

]

DIAGNOSTIC_SENSORS = [
    "Interuption 1",
    "Operat. time",
    "Service Hrs",
    "extra-WW. 1",
    "extra-WW. 2",
    "B extra-WW. 0",
    "B extra-WW. 1",
    "B extra-WW. 2",
    "Buffer Top 0",
    "Buffer Btm 0",
    "Buffer Top 1",
    "Buffer Btm 1",
    "Buffer Top 2",
    "Buffer Btm 2",
    "Auxiliary pump 0",
    "Auxiliary pump 1",
    "Auxiliary pump 2",
]

TRANSLATE = {
    #TODO: add translatiosn for all languages, not just English
    "Running": "status",
    "Boiler temperature": "boiler_temperature",
    "Outside Temp.": "outdoor_temperature",
    "Buffer load.": "buffer_load",
    "Buffer Top": "buffer_top_temperature",
    "Buffer Mid": "buffer_center_temperature",
    "Buffer Btm": "buffer_bottom_temperature",
    "DHW 0": "domestic_hot_water_0_temperature",
    "DHW 1": "domestic_hot_water_1_temperature",
    "DHW 2": "domestic_hot_water_2_temperature",
    "Room Temp:HC 0": "room_0_temperature",
    "Room Temp:HC 1": "room_1_temperature",
    "Room Temp:HC 2": "room_2_temperature",
    "Room Temp:HC 3": "room_3_temperature",
    "Room Temp:HC 4": "room_4_temperature",
    "Room Temp:HC 5": "room_5_temperature",
    "Room Temp:HC 6": "room_6_temperature",
    "Room Temp:HC 7": "room_7_temperature",
    "Room Temp:HC 8": "room_8_temperature",
    "Program": "program",
    SERIAL: "serial",
    "Version": "version",
    "OFF": "off",
    "TIMER": "timer",
    "DHW": "dhw",
    "HEAT": "heat",
    "HIBERNAT": "hibernate",
    "HIBERNATE TO": "hibernate_to",
    "DHW BOOST": "dhw_boost",
    "Boil.shunt pump": 'boiler_shunt_pump',
    "Suction fun": 'suction_fan',
    "Primary air": 'primary_air',
    "Seconday air": 'secondary_air',
    "CO2 Content": 'co2_content',
    "DHW Pump 0": 'dhw_pump_0',
    "DHW Pump 1": 'dhw_pump_1',
    "DHW Pump 2": 'dhw_pump_2',
    "Heating circulation pump 0": 'heating_circulation_pump_0',
    "Heating circulation pump 1": 'heating_circulation_pump_1',
    "Heating circulation pump 2": 'heating_circulation_pump_2',
    "Heating circulation pump 3": 'heating_circulation_pump_3',
    "Heating circulation pump 4": 'heating_circulation_pump_4',
    "Heating circulation pump 5": 'heating_circulation_pump_5',
    "Heating circulation pump 6": 'heating_circulation_pump_6',
    "Heating circulation pump 7": 'heating_circulation_pump_7',
    "Heating circulation pump 8": 'heating_circulation_pump_8',
    "Flow is 0": 'circuit_0_temp',
    "Flow is 1": 'circuit_1_temp',
    "Flow is 2": 'circuit_2_temp',
    "Flow is 3": 'circuit_3_temp',
    "Flow is 4": 'circuit_4_temp',
    "Flow is 5": 'circuit_5_temp',
    "Flow is 6": 'circuit_6_temp',
    "Flow is 7": 'circuit_7_temp',
    "Flow is 8": 'circuit_8_temp',
    "Program HC0": 'heating_circulation_program_0',
    "Program HC1": 'heating_circulation_program_1',
    "Program HC2": 'heating_circulation_program_2',
    "Program HC3": 'heating_circulation_program_3',
    "Program HC4": 'heating_circulation_program_4',
    "Program HC5": 'heating_circulation_program_5',
    "Program HC6": 'heating_circulation_program_6',
    "Program HC7": 'heating_circulation_program_7',
    "Program HC8": 'heating_circulation_program_8',
}
"""
    "Interuption 1",
    "Operat. time",
    "Service Hrs",
    "extra-WW. 1",
    "extra-WW. 2",
    "B extra-WW. 0",
    "B extra-WW. 1",
    "B extra-WW. 2",
    "Buffer Top 0",
    "Buffer Btm 0",
    "Buffer Top 1",
    "Buffer Btm 1",
    "Buffer Top 2",
    "Buffer Btm 2",
    "Auxiliary pump 0",
    "Auxiliary pump 1",
    "Auxiliary pump 2",

}

"""

class UnexpectedDataEncounteredException(Exception):
    """
    Raised when unexpected data is encountered
    This should not happen, please open a bug against guntamatic library on pypi
    """

class NoSerialException(Exception):
    """
    Raised when no serial was present in the data
    """

class Heater():
    """This class represents a heater"""

    def __init__(self, host):
        """A heater has a hostname, can also be an ip"""
        self.host = host
        self.protocol = PROTOCOL
        self.descurl = DESCURL
        self.dataurl = DATAURL

    def get_data(self):
        """
        Contact the heater and get the data.

        returns a dict with {'description': [value, unit], ...}
        """

        data = requests.get(self.protocol + self.host + '/' + self.dataurl, timeout=10)
        logging.debug(data)
        data = data.text.split('\n')
        logging.debug(data)
        desc = requests.get(self.protocol + self.host + '/' + self.descurl, timeout=10)
        logging.debug(desc)
        desc= desc.text.split('\n')
        logging.debug(desc)

        returndata = {}
        for datum, description in zip(data, desc):
            if RESERVED in description:
                continue
            if not description or not description.strip():
                continue
            key, *unit = description.split(';')
            # skip empty lines
            if not key or not key.strip():
                continue

            unit = ''.join(unit)

            returndata[key] = [datum, unit]
        return returndata

    def parse_data(self):
        """
        Parse the data from the Heater.
        Only return relevant data and translate to known fixed format
        """
        data = self.get_data()
        out = {}
        for key in SENSORS:
            try:
                out[TRANSLATE[key]] = data.get(key, None)
            except KeyError as exc:
                raise UnexpectedDataEncounteredException from exc

        # skip room temperature if it is 60: default value
        for key in list(out):
            if 'room' in key and (out[key] ==  ["60.00", "\u00b0C"] or out[key] ==  ["-9.00", "\u00b0C"]):
                del out[key]
            if 'domestic_hot_water' in key and out[key] ==  ["-20.00", "\u00b0C"]:
                del out[key]
            if 'circuit' in key and (
                out[key] ==  ["43.00", "\u00b0C"] or out[key] == ["-20.00", "\u00b0C"]) :
                circuit_nr = key[8]
                del out[key]
                del out[f'heating_circulation_pump_{circuit_nr}']
                del out[f'heating_circulation_program_{circuit_nr}']
            if key in out:
             print(key, out[key])
        if 'serial' not in out or not out['serial']:
            raise NoSerialException
        # Translate values as wel for known enums
        if 'program' in out:
            out['program'][0] = TRANSLATE[out['program'][0]]
        return out


def main():
    """Main library entrypoint"""
    verbose = False
    if len(sys.argv) < 2:
        print("usage: ", sys.argv[0] + ' hostname')
        sys.exit(2)
    if '-v' in sys.argv:
        verbose = True
        logging.basicConfig(level=logging.INFO)

    if '-vv' in sys.argv or '--verbose' in sys.argv:
        verbose = True
        logging.basicConfig(level=logging.DEBUG)


    heater = Heater(sys.argv[1])
    if not verbose:
        out = heater.parse_data()
    else:
        out = heater.get_data()

    if '--json' in sys.argv:
        import json
        print(json.dumps(out))
        return
    for key, values in out.items():
        print(key + ' ' + str(values[0]) + str(values[1]))


if __name__ == '__main__':
    main()
