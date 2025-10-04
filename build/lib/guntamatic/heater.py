"""
This module implements the functionality to contact a guntamatic wood heater e.g. BMK 20
"""

import requests
import logging
import sys

PROTOCOL = 'http://'

DESCURL = 'daqdesc.cgi'
DATAURL = 'daqdata.cgi'

RESERVED = 'reserved'


class Heater(object):
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

        data = requests.get(self.protocol + self.host + '/' + self.dataurl).text.split('\n')
        logging.debug(data)
        desc = requests.get(self.protocol + self.host + '/' + self.descurl).text.split('\n')
        logging.debug(desc)

        returndata = {}
        for datum, description in zip(data, desc):
            if RESERVED in description:
                continue
            key, *unit = description.split(';')
            unit = ''.join(unit)

            returndata[key] = [datum, unit]
        return returndata


def main():
    verbose = False
    if len(sys.argv) < 2:
        print("usage: ", sys.argv[0] + ' hostname')
        sys.exit(2)
    if '-v' in sys.argv:
        verbose = True
        logging.basicConfig(level=logging.INFO)

    if '-vv' in sys.argv:
        verbose = True
        logging.basicConfig(level=logging.DEBUG)

    VERBOSE = ['Program', 'DHW', '0', '3', '4', '5', '6', '7', '8', 'extra', 'Interuption', 'Serial', 'Auxiliary',
               'Top ', 'Btm ', 'Version', 'Suction', 'air']
    heater = Heater(sys.argv[1])

    for key, values in heater.get_data().items():
        cont = False
        for verb in VERBOSE:
            if verb in key and not verbose:
                cont = True
        if not cont:
            print(key + ' ' + str(values[0]) + str(values[1]))

if __name__ == '__main__':
    main()
