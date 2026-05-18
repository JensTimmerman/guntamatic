"""
This module implements the functionality to contact a guntamatic wood heater e.g. BMK 20
"""

import logging
import sys

import requests

PROTOCOL = 'http://'

DESCURL = 'daqdesc.cgi'
DATAURL = 'daqdata.cgi'

RESERVED = ['reserved', 'reservado', 'réservé']
SERIAL = 'Serial'

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
    # german
    "Störung 1"
    "Störung 2"
    "Betriebsstunden"
    "Servicezeit"
    "Zusatzwarmw. 1"
    "Zusatzwarmw. 2"
    "P Zusatzwarmw. 0"
    "P Zusatzwarmw. 1"
    "P Zusatzwarmw. 3"
    "Puffer oben 0"
    "Puffer unten 0"
    "Puffer oben 1"
    "Puffer unten 1"
    "Puffer oben 2"
    "Puffer unten 2"
    "Fernpumpe 0"
    "Fernpumpe 1"
    "Fernpumpe 2"
]

TRANSLATE = {
    #TODO: add translations for all languages, not just English and german
    "Running": "status",
    "Betrieb": "status",
    "Boiler temperature": "boiler_temperature",
    "Kesseltemperatur": "boiler_temperature",
    "Outside Temp.": "outdoor_temperature",
    "Aussentemperatur": "outdoor_temperature",
    "Buffer load.": "buffer_load",
    "Pufferladung": "buffer_load",
    "Buffer Top": "buffer_top_temperature",
    "Puffer oben": "buffer_top_temperature",
    "Buffer Mid": "buffer_center_temperature",
    "Puffer mitte": "buffer_center_temperature",
    "Buffer Btm": "buffer_bottom_temperature",
    "Puffer unten": "buffer_bottom_temperature",
    "DHW 0": "domestic_hot_water_0_temperature",
    "Warmwasser 0": "domestic_hot_water_0_temperature",
    "DHW 1": "domestic_hot_water_1_temperature",
    "Warmwasser 1": "domestic_hot_water_1_temperature",
    "DHW 2": "domestic_hot_water_2_temperature",
    "Warmwasser 2": "domestic_hot_water_2_temperature",
    "Room Temp:HC 0": "room_0_temperature",
    "Raumtemp. HK 0": "room_0_temperature",
    "Room Temp:HC 1": "room_1_temperature",
    "Raumtemp. HK 1": "room_1_temperature",
    "Room Temp:HC 2": "room_2_temperature",
    "Raumtemp. HK 2": "room_2_temperature",
    "Room Temp:HC 3": "room_3_temperature",
    "Raumtemp. HK 3": "room_3_temperature",
    "Room Temp:HC 4": "room_4_temperature",
    "Raumtemp. HK 4": "room_4_temperature",
    "Room Temp:HC 5": "room_5_temperature",
    "Raumtemp. HK 5": "room_5_temperature",
    "Room Temp:HC 6": "room_6_temperature",
    "Raumtemp. HK 6": "room_6_temperature",
    "Room Temp:HC 7": "room_7_temperature",
    "Raumtemp. HK 7": "room_7_temperature",
    "Room Temp:HC 8": "room_8_temperature",
    "Raumtemp. HK 8": "room_8_temperature",
    "Program": "program",
    "Programm": "program",
    SERIAL: "serial",
    "Version": "version",
    "Boil.shunt pump": "boiler_shunt_pump",
    "Kesselladepumpe": "boiler_shunt_pump",
    "Suction fun": "suction_fan",
    "Saugzug": "suction_fan",
    "Primary air": "primary_air",
    "Primärluft": "primary_air",
    "Seconday air": "secondary_air",
    "Sekundärluft": "secondary_air",
    "CO2 Content": "co2_content",
    "CO2 Gehalt": "co2_content",
    "DHW Pump 0": "dhw_pump_0",
    "Warmwasserpumpe 0": "dhw_pump_0",
    "DHW Pump 1": "dhw_pump_1",
    "Warmwasserpumpe 1": "dhw_pump_1",
    "DHW Pump 2": "dhw_pump_2",
    "Warmwasserpumpe 2": "dhw_pump_2",
    "Heating circulation pump 0": "heating_circulation_pump_0",
    "Heizkreispumpe 0": "heating_circulation_pump_0",
    "Heating circulation pump 1": "heating_circulation_pump_1",
    "Heizkreispumpe 1": "heating_circulation_pump_1",
    "Heating circulation pump 2": "heating_circulation_pump_2",
    "Heizkreispumpe 2": "heating_circulation_pump_2",
    "Heating circulation pump 3": "heating_circulation_pump_3",
    "Heizkreispumpe 3": "heating_circulation_pump_3",
    "Heating circulation pump 4": "heating_circulation_pump_4",
    "Heizkreispumpe 4": "heating_circulation_pump_4",
    "Heating circulation pump 5": "heating_circulation_pump_5",
    "Heizkreispumpe 5": "heating_circulation_pump_5",
    "Heating circulation pump 6": "heating_circulation_pump_6",
    "Heizkreispumpe 6": "heating_circulation_pump_6",
    "Heating circulation pump 7": "heating_circulation_pump_7",
    "Heizkreispumpe 7": "heating_circulation_pump_7",
    "Heating circulation pump 8": "heating_circulation_pump_8",
    "Heizkreispumpe 8": "heating_circulation_pump_8",
    "Flow is 0": "circuit_0_temp",
    "Vorlauf Ist 0": "circuit_0_temp",
    "Flow is 1": "circuit_1_temp",
    "Vorlauf Ist 1": "circuit_1_temp",
    "Flow is 2": "circuit_2_temp",
    "Vorlauf Ist 2": "circuit_2_temp",
    "Flow is 3": "circuit_3_temp",
    "Vorlauf Ist 3": "circuit_3_temp",
    "Flow is 4": "circuit_4_temp",
    "Vorlauf Ist 4": "circuit_4_temp",
    "Flow is 5": "circuit_5_temp",
    "Vorlauf Ist 5": "circuit_5_temp",
    "Flow is 6": "circuit_6_temp",
    "Vorlauf Ist 6": "circuit_6_temp",
    "Flow is 7": "circuit_7_temp",
    "Vorlauf Ist 7": "circuit_7_temp",
    "Flow is 8": "circuit_8_temp",
    "Vorlauf Ist 8": "circuit_8_temp",
    "Program HC0": "heating_circulation_program_0",
    "Progamm HK0": "heating_circulation_program_0",
    "Program HC1": "heating_circulation_program_1",
    "Progamm HK1": "heating_circulation_program_1",
    "Program HC2": "heating_circulation_program_2",
    "Progamm HK2": "heating_circulation_program_2",
    "Program HC3": "heating_circulation_program_3",
    "Progamm HK3": "heating_circulation_program_3",
    "Program HC4": "heating_circulation_program_4",
    "Progamm HK4": "heating_circulation_program_4",
    "Program HC5": "heating_circulation_program_5",
    "Progamm HK5": "heating_circulation_program_5",
    "Program HC6": "heating_circulation_program_6",
    "Progamm HK6": "heating_circulation_program_6",
    "Program HC7": "heating_circulation_program_7",
    "Progamm HK7": "heating_circulation_program_7",
    "Program HC8": "heating_circulation_program_8",
    "Progamm HK8": "heating_circulation_program_8",
    # german
    "Störung 1": "interruption_1",
    "Störung 2": "interruption_2",
    "Betriebsstunden": "operating_time",
    "Servicezeit": "service_hours",
    "Zusatzwarmw. 1": "extra_dhw_1_temperature",
    "Zusatzwarmw. 2": "extra_dhw_2_temperature",
    "P Zusatzwarmw. 0": "extra_dhw_boost_0",
    "P Zusatzwarmw. 1": "extra_dhw_boost_1",
    "P Zusatzwarmw. 2": "extra_dhw_boost_2",
    "Puffer oben 0": "buffer_top_0_temperature",
    "Puffer unten 0": "buffer_bottom_0_temperature",
    "Puffer oben 1": "buffer_top_1_temperature",
    "Puffer unten 1": "buffer_bottom_1_temperature",
    "Puffer oben 2": "buffer_top_2_temperature",
    "Puffer unten 2": "buffer_bottom_2_temperature",
    "Fernpumpe 0": "auxiliary_pump_0",
    "Fernpumpe 1": "auxiliary_pump_1",
    "Fernpumpe 2": "auxiliary_pump_2",
    # english
    "Interuption 1": "interruption_1",
    "Interuption 2": "interruption_2",
    "Operat. time": "operating_time",
    "Service Hrs": "service_hours",
    "extra-WW. 1": "extra_dhw_1_temperature",
    "extra-WW. 2": "extra_dhw_2_temperature",
    "B extra-WW. 0": "extra_dhw_boost_0",
    "B extra-WW. 1": "extra_dhw_boost_1",
    "B extra-WW. 2": "extra_dhw_boost_2",
    "Buffer Top 0": "buffer_top_0_temperature",
    "Buffer Btm 0": "buffer_bottom_0_temperature",
    "Buffer Top 1": "buffer_top_1_temperature",
    "Buffer Btm 1": "buffer_bottom_1_temperature",
    "Buffer Top 2": "buffer_top_2_temperature",
    "Buffer Btm 2": "buffer_bottom_2_temperature",
    "Auxiliary pump 0": "auxiliary_pump_0",
    "Auxiliary pump 1": "auxiliary_pump_1",
    "Auxiliary pump 2": "auxiliary_pump_2",
    # spanish
    "Modo": "status",
    "Tª caldera": "boiler_temperature",
    "Tª exterior": "outdoor_temperature",
    "Nivel dep. inercia": "buffer_load",
    "Tª inercia superior (T3)": "buffer_top_temperature",
    "Tª inercia p. medio": "buffer_center_temperature",
    "Tª inercia inferior (T2)": "buffer_bottom_temperature",
    "ACS 0": "domestic_hot_water_0_temperature",
    "ACS 1": "domestic_hot_water_1_temperature",
    "ACS 2": "domestic_hot_water_2_temperature",
    "Tª amb. CC 0": "room_0_temperature",
    "Tª amb. CC 1": "room_1_temperature",
    "Tª amb. CC 2": "room_2_temperature",
    "Tª amb. CC 3": "room_3_temperature",
    "Tª amb. CC 4": "room_4_temperature",
    "Tª amb. CC 5": "room_5_temperature",
    "Tª amb. CC 6": "room_6_temperature",
    "Tª amb. CC 7": "room_7_temperature",
    "Tª amb. CC 8": "room_8_temperature",
    "Programa": "program",
    "Versión": "version",
    "Bomba caldera": "boiler_shunt_pump",
    "Extractor humos": "suction_fan",
    "Aire primario": "primary_air",
    "Aire secundario": "secondary_air",
    "Contenido CO2": "co2_content",
    "Bomba ACS 0": "dhw_pump_0",
    "Bomba ACS 1": "dhw_pump_1",
    "Bomba ACS 2": "dhw_pump_2",
    "Bomba CC 0": "heating_circulation_pump_0",
    "Bomba CC 1": "heating_circulation_pump_1",
    "Bomba CC 2": "heating_circulation_pump_2",
    "Bomba CC 3": "heating_circulation_pump_3",
    "Bomba CC 4": "heating_circulation_pump_4",
    "Bomba CC 5": "heating_circulation_pump_5",
    "Bomba CC 6": "heating_circulation_pump_6",
    "Bomba CC 7": "heating_circulation_pump_7",
    "Bomba CC 8": "heating_circulation_pump_8",
    "Tª imp. real 0": "circuit_0_temp",
    "Tª imp. real 1": "circuit_1_temp",
    "Tª imp. real 2": "circuit_2_temp",
    "Tª imp. real 3": "circuit_3_temp",
    "Tª imp. real 4": "circuit_4_temp",
    "Tª imp. real 5": "circuit_5_temp",
    "Tª imp. real 6": "circuit_6_temp",
    "Tª imp. real 7": "circuit_7_temp",
    "Tª imp. real 8": "circuit_8_temp",
    "Programa CC0": "heating_circulation_program_0",
    "Programa CC1": "heating_circulation_program_1",
    "Programa CC2": "heating_circulation_program_2",
    "Programa CC3": "heating_circulation_program_3",
    "Programa CC4": "heating_circulation_program_4",
    "Programa CC5": "heating_circulation_program_5",
    "Programa CC6": "heating_circulation_program_6",
    "Programa CC7": "heating_circulation_program_7",
    "Programa CC8": "heating_circulation_program_8",
    "horas trabajo": "operating_time",
    "t. servicio": "service_hours",
    "ACS adic. 1": "extra_dhw_1_temperature",
    "ACS adic. 2": "extra_dhw_2_temperature",
    "B ACS adic. 0": "extra_dhw_boost_0",
    "B ACS adic. 1": "extra_dhw_boost_1",
    "B ACS adic. 2": "extra_dhw_boost_2",
    "Tª inercia superior (T3) 0": "buffer_top_0_temperature",
    "Tª inercia superior (T3) 1": "buffer_top_1_temperature",
    "Tª inercia superior (T3) 2": "buffer_top_2_temperature",
    "Tª inercia inferior (T2) 0": "buffer_bottom_0_temperature",
    "Tª inercia inferior (T2) 1": "buffer_bottom_1_temperature",
    "Tª inercia inferior (T2) 2": "buffer_bottom_2_temperature",
    "Bomba circ. primario 0": "auxiliary_pump_0",
    "Bomba circ. primario 1": "auxiliary_pump_1",
    "Bomba circ. primario 2": "auxiliary_pump_2",
    "Avería 1": "interruption_1",
    "Avería 2": "interruption_2",
    # french
    "fonction": "status",
    "Temp. chaudiere": "boiler_temperature",
    "temp.exterieure": "outdoor_temperature",
    "charge accu": "buffer_load",
    "accu haut": "buffer_top_temperature",
    "accu milieu": "buffer_center_temperature",
    "accu bas": "buffer_bottom_temperature",
    "Pompe charge chaud.": "boiler_shunt_pump",
    "Aspiration": "suction_fan",
    "Air primaire": "primary_air",
    "Air secondaire": "secondary_air",
    "Teneur CO2": "co2_content",
    "Eau chaude 0": "domestic_hot_water_0_temperature",
    "Eau chaude 1": "domestic_hot_water_1_temperature",
    "Eau chaude 2": "domestic_hot_water_2_temperature",
    "Pompe eau chaude 0": "dhw_pump_0",
    "Pompe eau chaude 1": "dhw_pump_1",
    "Pompe eau chaude 2": "dhw_pump_2",
    "Pompe circ.chauf. 0": "heating_circulation_pump_0",
    "Pompe circ.chauf. 1": "heating_circulation_pump_1",
    "Pompe circ.chauf. 2": "heating_circulation_pump_2",
    "Pompe circ.chauf. 3": "heating_circulation_pump_3",
    "Pompe circ.chauf. 4": "heating_circulation_pump_4",
    "Pompe circ.chauf. 5": "heating_circulation_pump_5",
    "Pompe circ.chauf. 6": "heating_circulation_pump_6",
    "Pompe circ.chauf. 7": "heating_circulation_pump_7",
    "Pompe circ.chauf. 8": "heating_circulation_pump_8",
    "temp.amb. CH 0": "room_0_temperature",
    "temp.amb. CH 1": "room_1_temperature",
    "temp.amb. CH 2": "room_2_temperature",
    "temp.amb. CH 3": "room_3_temperature",
    "temp.amb. CH 4": "room_4_temperature",
    "temp.amb. CH 5": "room_5_temperature",
    "temp.amb. CH 6": "room_6_temperature",
    "temp.amb. CH 7": "room_7_temperature",
    "temp.amb. CH 8": "room_8_temperature",
    "aller effect. 0": "circuit_0_temp",
    "aller effect. 1": "circuit_1_temp",
    "aller effect. 2": "circuit_2_temp",
    "aller effect. 3": "circuit_3_temp",
    "aller effect. 4": "circuit_4_temp",
    "aller effect. 5": "circuit_5_temp",
    "aller effect. 6": "circuit_6_temp",
    "aller effect. 7": "circuit_7_temp",
    "aller effect. 8": "circuit_8_temp",
    "program.": "program",
    "Programme CH0": "heating_circulation_program_0",
    "Programme CH1": "heating_circulation_program_1",
    "Programme CH2": "heating_circulation_program_2",
    "Programme CH3": "heating_circulation_program_3",
    "Programme CH4": "heating_circulation_program_4",
    "Programme CH5": "heating_circulation_program_5",
    "Programme CH6": "heating_circulation_program_6",
    "Programme CH7": "heating_circulation_program_7",
    "Programme CH8": "heating_circulation_program_8",
    "Defaut 1": "interruption_1",
    "Defaut 2": "interruption_2",
    "Série": "serial",
    "Heures de fonctionnemment": "operating_time",
    "temps de service": "service_hours",
    "ECS Suppl. 1": "extra_dhw_1_temperature",
    "ECS Suppl. 2": "extra_dhw_2_temperature",
    "P ECS Suppl. 0": "extra_dhw_boost_0",
    "P ECS Suppl. 1": "extra_dhw_boost_1",
    "P ECS Suppl. 2": "extra_dhw_boost_2",
    "accu haut 0": "buffer_top_0_temperature",
    "accu haut 1": "buffer_top_1_temperature",
    "accu haut 2": "buffer_top_2_temperature",
    "accu bas 0": "buffer_bottom_0_temperature",
    "accu bas 1": "buffer_bottom_1_temperature",
    "accu bas 2": "buffer_bottom_2_temperature",
    "Pompe réseau 0": "auxiliary_pump_0",
    "Pompe réseau 1": "auxiliary_pump_1",
    "Pompe réseau 2": "auxiliary_pump_2",
    # italian
    "funzion.": "status",
    "temp.caldaia": "boiler_temperature",
    "temp.est": "outdoor_temperature",
    "caric.accum.": "buffer_load",
    "accum.in alto": "buffer_top_temperature",
    "accu milieu": "buffer_center_temperature",
    "accum.in basso": "buffer_bottom_temperature",
    "pom.caric.cald.": "boiler_shunt_pump",
    "soffiante": "suction_fan",
    "aria primaria": "primary_air",
    "aria secundaria": "secondary_air",
    "concentrazione CO2": "co2_content",
    "acqua calda 0": "domestic_hot_water_0_temperature",
    "acqua calda 1": "domestic_hot_water_1_temperature",
    "acqua calda 2": "domestic_hot_water_2_temperature",
    "pompa per acqua calda sanitaria 0": "dhw_pump_0",
    "pompa per acqua calda sanitaria 1": "dhw_pump_1",
    "pompa per acqua calda sanitaria 2": "dhw_pump_2",
    "pompa per circuito riscaldamento 0": "heating_circulation_pump_0",
    "pompa per circuito riscaldamento 1": "heating_circulation_pump_1",
    "pompa per circuito riscaldamento 2": "heating_circulation_pump_2",
    "pompa per circuito riscaldamento 3": "heating_circulation_pump_3",
    "pompa per circuito riscaldamento 4": "heating_circulation_pump_4",
    "pompa per circuito riscaldamento 5": "heating_circulation_pump_5",
    "pompa per circuito riscaldamento 6": "heating_circulation_pump_6",
    "pompa per circuito riscaldamento 7": "heating_circulation_pump_7",
    "pompa per circuito riscaldamento 8": "heating_circulation_pump_8",
    "temp.amb.CR 0": "room_0_temperature",
    "temp.amb.CR 1": "room_1_temperature",
    "temp.amb.CR 2": "room_2_temperature",
    "temp.amb.CR 3": "room_3_temperature",
    "temp.amb.CR 4": "room_4_temperature",
    "temp.amb.CR 5": "room_5_temperature",
    "temp.amb.CR 6": "room_6_temperature",
    "temp.amb.CR 7": "room_7_temperature",
    "temp.amb.CR 8": "room_8_temperature",
    "mandata eff 0": "circuit_0_temp",
    "mandata eff 1": "circuit_1_temp",
    "mandata eff 2": "circuit_2_temp",
    "mandata eff 3": "circuit_3_temp",
    "mandata eff 4": "circuit_4_temp",
    "mandata eff 5": "circuit_5_temp",
    "mandata eff 6": "circuit_6_temp",
    "mandata eff 7": "circuit_7_temp",
    "mandata eff 8": "circuit_8_temp",
    "progr.": "program",
    "programma CR0": "heating_circulation_program_0",
    "programma CR1": "heating_circulation_program_1",
    "programma CR2": "heating_circulation_program_2",
    "programma CR3": "heating_circulation_program_3",
    "programma CR4": "heating_circulation_program_4",
    "programma CR5": "heating_circulation_program_5",
    "programma CR6": "heating_circulation_program_6",
    "programma CR7": "heating_circulation_program_7",
    "programma CR8": "heating_circulation_program_8",
    "disturbo 1": "interruption_1",
    "disturbo 2": "interruption_2",
    "Versione": "version",
    "temp.funz.": "operating_time",
    "time serviz": "service_hours",
    "boll.add. 1": "extra_dhw_1_temperature",
    "boll.add. 2": "extra_dhw_2_temperature",
    "P boll.add. 0": "extra_dhw_boost_0",
    "P boll.add. 1": "extra_dhw_boost_1",
    "P boll.add. 2": "extra_dhw_boost_2",
    "accum.in alto 0": "buffer_top_0_temperature",
    "accum.in basso 0": "buffer_bottom_0_temperature",
    "accum.in alto 1": "buffer_top_1_temperature",
    "accum.in basso 1": "buffer_bottom_1_temperature",
    "accum.in alto 2": "buffer_top_2_temperature",
    "accum.in basso 2": "buffer_bottom_2_temperature",
}

TRANSLATE_PROGRAM = {
    # english
    "OFF": "off",
    "TIMER": "timer",
    "DHW": "dhw",
    "HEAT": "heat",
    "HIBERNAT": "hibernate",
    "HIBERNATE TO": "hibernate_to",
    "DHW BOOST": "dhw_boost",
    # spanish
    "ACS": "dhw",
    "CALENTAR": "heat",
    "Reducido": "hibernate",
    "Reducido hasta": "hibernate_to",
    "Impulsión ACS": "dhw_boost",
    # German
    "Aus": "off",
    "Normal": "timer",
    "Warmwasser": "dhw",
    "Heizen": "heat",
    "Absenken": "hibernate",
    "Absenken bis": "hibernate_to",
    "WW-Nachladen": "dhw_boost",
    # french
    "NORMAL": "timer",
    "ECS": "dhw",
    "CHAUFFAGE": "heat",
    "DIMIN.": "hibernate",
    "DIMIN.JUSQ.": "hibernate_to",
    "Recharge ECS": "dhw_boost",
    # italian
    "NORMALE": 'timer',
    "BOLLIT": 'dhw',
    "RISC": 'heat',
    'RIDUR': 'hibernate',
    'RIDURRE FINO': 'hibernate_to',
    'CARI.BOLLIT': 'dhw_boost',
}

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
            if any(key in description for key in RESERVED):
                continue
            if not description or not description.strip():
                continue
            key, *unit = description.split(';')
            # skip empty lines
            if not key or not key.strip():
                continue

            unit = ''.join(unit)

            returndata[key.strip()] = [datum.strip(), unit.strip()]
        return returndata

    def parse_data(self):
        """
        Parse the data from the Heater.
        Only return relevant data and translate to known fixed format
        """
        data = self.get_data()
        out = {}
        for key, value in TRANSLATE.items():
            try:
                out[value] = data[key]
            except KeyError:
                pass

        # skip room temperature if it is 60: default value
        for key in list(out):
            if 'temp' in key and (out[key] ==  ["60.00", "\u00b0C"]
                                  or out[key] ==  ["-20.00", "\u00b0C"]
                                  or out[key] == ["43.00", "\u00b0C"]
                                  or out[key] ==  ["-9.00", "\u00b0C"]):
                if 'circuit' in key:
                    circuit_nr = key[8]
                    del out[f'heating_circulation_pump_{circuit_nr}']
                    del out[f'heating_circulation_program_{circuit_nr}']
                if 'domestic_hot_water' in key:
                    dhw_nr = key[19]
                    del out[f'dhw_pump_{dhw_nr}']
                    del out[f'extra_dhw_boost_{dhw_nr}']
                del out[key]
        if 'serial' not in out or not out['serial']:
            raise NoSerialException
        # Translate values as wel for known enums
        if 'program' in out:
            out['program'][0] = TRANSLATE_PROGRAM[out['program'][0]]
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
