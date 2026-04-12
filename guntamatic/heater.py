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
    "Room Temp:HC 1",
    "Room Temp:HC 2",
    "Program",
    "Serial",
    "Version",
]

DIAGNOSTIC_SENSORS = [
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
    "Room Temp:HC 0",
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
    "Running": "Status",
    "Boiler temperature": "Boiler Temperature",
    "Outside Temp.": "Outdoor Temperature",
    "Buffer load.": "Buffer Load",
    "Buffer Top": "Buffer Top Temperature",
    "Buffer Mid": "Buffer Center Temperature",
    "Buffer Btm": "Buffer Bottom Temperature",
    "DHW 0": "Domestic Home Water Temperature",
    "Room Temp:HC 1": "Room 1 Temperature",
    "Room Temp:HC 2": "Room 2 Temperature",
    "Program": "Program",
    "Serial": "Serial",
    "Version": "Version",
}


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
        for key, values in data.items():
            if key in SENSORS:
                out[TRANSLATE[key]] = values
        return out

def main():
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
