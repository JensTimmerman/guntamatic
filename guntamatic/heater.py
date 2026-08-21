"""
This module implements the functionality to contact a guntamatic wood heater e.g. BMK 20
"""

import logging
import sys

import requests

PROTOCOL = 'http://'

DESCURL = 'daqdesc.cgi'
DATAURL = 'daqdata.cgi'

RESERVED = ['reserved', 'reservado', 'réservé', 'gereserveerd']
SERIAL = 'Serial'

TRANSLATE = {
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
    # czech
    "Rezim": "status",
    "Teplota kotle": "boiler_temperature",
    "Venkov.tepl.": "outdoor_temperature",
    "Ohrev AKU": "buffer_load",
    "AKU nahore": "buffer_top_temperature",
    "AKU uprostred": "buffer_center_temperature",
    "AKU dole": "buffer_bottom_temperature",
    "Pomoc.crp.kotle": "boiler_shunt_pump",
    "Odtah": "suction_fan",
    "Primar.vzduch": "primary_air",
    "Sekundarni vzduch": "secondary_air",
    "Obsah CO2": "co2_content",
    "TUV 0": "domestic_hot_water_0_temperature",
    "TUV 1": "domestic_hot_water_1_temperature",
    "TUV 2": "domestic_hot_water_2_temperature",
    "Cerp. TUV 0": "dhw_pump_0",
    "Cerp. TUV 1": "dhw_pump_1",
    "Cerp. TUV 2": "dhw_pump_2",
    "Cerp. top.okruhu 0": "heating_circulation_pump_0",
    "Cerp. top.okruhu 1": "heating_circulation_pump_1",
    "Cerp. top.okruhu 2": "heating_circulation_pump_2",
    "Cerp. top.okruhu 3": "heating_circulation_pump_3",
    "Cerp. top.okruhu 4": "heating_circulation_pump_4",
    "Cerp. top.okruhu 5": "heating_circulation_pump_5",
    "Cerp. top.okruhu 6": "heating_circulation_pump_6",
    "Cerp. top.okruhu 7": "heating_circulation_pump_7",
    "Cerp. top.okruhu 8": "heating_circulation_pump_8",
    "Pok.tepl. TO 0": "room_0_temperature",
    "Pok.tepl. TO 1": "room_1_temperature",
    "Pok.tepl. TO 2": "room_2_temperature",
    "Pok.tepl. TO 3": "room_3_temperature",
    "Pok.tepl. TO 4": "room_4_temperature",
    "Pok.tepl. TO 5": "room_5_temperature",
    "Pok.tepl. TO 6": "room_6_temperature",
    "Pok.tepl. TO 7": "room_7_temperature",
    "Pok.tepl. TO 8": "room_8_temperature",
    "Top.voda skut. 0": "circuit_0_temp",
    "Top.voda skut. 1": "circuit_1_temp",
    "Top.voda skut. 2": "circuit_2_temp",
    "Top.voda skut. 3": "circuit_3_temp",
    "Top.voda skut. 4": "circuit_4_temp",
    "Top.voda skut. 5": "circuit_5_temp",
    "Top.voda skut. 6": "circuit_6_temp",
    "Top.voda skut. 7": "circuit_7_temp",
    "Top.voda skut. 8": "circuit_8_temp",
    "Program TO0": "heating_circulation_program_0",
    "Program TO1": "heating_circulation_program_1",
    "Program TO2": "heating_circulation_program_2",
    "Program TO3": "heating_circulation_program_3",
    "Program TO4": "heating_circulation_program_4",
    "Program TO5": "heating_circulation_program_5",
    "Program TO6": "heating_circulation_program_6",
    "Program TO7": "heating_circulation_program_7",
    "Program TO8": "heating_circulation_program_8",
    "Porucha 1": "interruption_1",
    "Porucha 2": "interruption_2",
    "Serie": "serial",
    "Verze": "version",
    "Doba provozu": "operating_time",
    "Dny od serv": "service_hours",
    "TUV extra 1": "extra_dhw_1_temperature",
    "TUV extra 2": "extra_dhw_2_temperature",
    "C TUV extra 0": "extra_dhw_boost_0",
    "C TUV extra 1": "extra_dhw_boost_1",
    "C TUV extra 2": "extra_dhw_boost_2",
    "AKU nahore 0": "buffer_top_0_temperature",
    "AKU dole 0": "buffer_bottom_0_temperature",
    "AKU nahore 1": "buffer_top_1_temperature",
    "AKU dole 1": "buffer_bottom_1_temperature",
    "AKU nahore 2": "buffer_top_2_temperature",
    "AKU dole 2": "buffer_bottom_2_temperature",
    "Dalkove cerpadlo 0": "auxiliary_pump_0",
    "Dalkove cerpadlo 1": "auxiliary_pump_1",
    "Dalkove cerpadlo 2": "auxiliary_pump_2",
    # slovenian
    "rezim": "status",
    "Temperatura kotla": "boiler_temperature",
    "zunanja tempera.": "outdoor_temperature",
    "Polnj.hrani.": "buffer_load",
    "hranilnik zgoraj": "buffer_top_temperature",
    "Hrani. sred.": "buffer_center_temperature",
    "hranilnik spod.": "buffer_bottom_temperature",
    "Crpalka peci": "boiler_shunt_pump",
    "ventilator": "suction_fan",
    "primarni zrak": "primary_air",
    "sekundarni zrak": "secondary_air",
    "CO2 vsebnost": "co2_content",
    "topla voda 0": "domestic_hot_water_0_temperature",
    "topla voda 1": "domestic_hot_water_1_temperature",
    "topla voda 2": "domestic_hot_water_2_temperature",
    "crpalka t. vode 0": "dhw_pump_0",
    "crpalka t. vode 1": "dhw_pump_1",
    "crpalka t. vode 2": "dhw_pump_2",
    "Ogrevalna cpralka 0": "heating_circulation_pump_0",
    "Ogrevalna cpralka 1": "heating_circulation_pump_1",
    "Ogrevalna cpralka 2": "heating_circulation_pump_2",
    "Ogrevalna cpralka 3": "heating_circulation_pump_3",
    "Ogrevalna cpralka 4": "heating_circulation_pump_4",
    "Ogrevalna cpralka 5": "heating_circulation_pump_5",
    "Ogrevalna cpralka 6": "heating_circulation_pump_6",
    "Ogrevalna cpralka 7": "heating_circulation_pump_7",
    "Ogrevalna cpralka 8": "heating_circulation_pump_8",
    "T prostor OK 0": "room_0_temperature",
    "T prostor OK 1": "room_1_temperature",
    "T prostor OK 2": "room_2_temperature",
    "T prostor OK 3": "room_3_temperature",
    "T prostor OK 4": "room_4_temperature",
    "T prostor OK 5": "room_5_temperature",
    "T prostor OK 6": "room_6_temperature",
    "T prostor OK 7": "room_7_temperature",
    "T prostor OK 8": "room_8_temperature",
    "Dvi. vod merjena 0": "circuit_0_temp",
    "Dvi. vod merjena 1": "circuit_1_temp",
    "Dvi. vod merjena 2": "circuit_2_temp",
    "Dvi. vod merjena 3": "circuit_3_temp",
    "Dvi. vod merjena 4": "circuit_4_temp",
    "Dvi. vod merjena 5": "circuit_5_temp",
    "Dvi. vod merjena 6": "circuit_6_temp",
    "Dvi. vod merjena 7": "circuit_7_temp",
    "Dvi. vod merjena 8": "circuit_8_temp",
    "Progamm OK0": "heating_circulation_program_0",
    "Progamm OK1": "heating_circulation_program_1",
    "Progamm OK2": "heating_circulation_program_2",
    "Progamm OK3": "heating_circulation_program_3",
    "Progamm OK4": "heating_circulation_program_4",
    "Progamm OK5": "heating_circulation_program_5",
    "Progamm OK6": "heating_circulation_program_6",
    "Progamm OK7": "heating_circulation_program_7",
    "Progamm OK8": "heating_circulation_program_8",
    "MOTNJA 1": "interruption_1",
    "MOTNJA 2": "interruption_2",
    "delovne ure": "operating_time",
    "cas servis": "service_hours",
    "doda. bojler 1": "extra_dhw_1_temperature",
    "doda. bojler 2": "extra_dhw_2_temperature",
    "T doda. bojler 0": "extra_dhw_boost_0",
    "T doda. bojler 1": "extra_dhw_boost_1",
    "T doda. bojler 2": "extra_dhw_boost_2",
    "hranilnik zgoraj 0": "buffer_top_0_temperature",
    "hranilnik spod. 0": "buffer_bottom_0_temperature",
    "hranilnik zgoraj 1": "buffer_top_1_temperature",
    "hranilnik spod. 1": "buffer_bottom_1_temperature",
    "hranilnik zgoraj 2": "buffer_top_2_temperature",
    "hranilnik spod. 2": "buffer_bottom_2_temperature",
    # hungarian
    "Üzem": "status",
    "Kazánhõmérséklet": "boiler_temperature",
    "Külsõ hõm.": "outdoor_temperature",
    "Puffertöltés": "buffer_load",
    "Puffer fent": "buffer_top_temperature",
    "Puffer középen": "buffer_center_temperature",
    "Puffer lent": "buffer_bottom_temperature",
    "Kazántöltõ szivattyú": "boiler_shunt_pump",
    "Szívó huzat": "suction_fan",
    "Primer levegõ": "primary_air",
    "Szekunder levegõ": "secondary_air",
    "CO2 tartalom": "co2_content",
    "Meleg víz 0": "domestic_hot_water_0_temperature",
    "Meleg víz 1": "domestic_hot_water_1_temperature",
    "Meleg víz 2": "domestic_hot_water_2_temperature",
    "Meleg-vízszivattyú 0": "dhw_pump_0",
    "Meleg-vízszivattyú 1": "dhw_pump_1",
    "Meleg-vízszivattyú 2": "dhw_pump_2",
    "Fûtõköri szivattyú 0": "heating_circulation_pump_0",
    "Fûtõköri szivattyú 1": "heating_circulation_pump_1",
    "Fûtõköri szivattyú 2": "heating_circulation_pump_2",
    "Fûtõköri szivattyú 3": "heating_circulation_pump_3",
    "Fûtõköri szivattyú 4": "heating_circulation_pump_4",
    "Fûtõköri szivattyú 5": "heating_circulation_pump_5",
    "Fûtõköri szivattyú 6": "heating_circulation_pump_6",
    "Fûtõköri szivattyú 7": "heating_circulation_pump_7",
    "Fûtõköri szivattyú 8": "heating_circulation_pump_8",
    "Helyiség hõm. HK 0": "room_0_temperature",
    "Helyiség hõm. HK 1": "room_1_temperature",
    "Helyiség hõm. HK 2": "room_2_temperature",
    "Helyiség hõm. HK 3": "room_3_temperature",
    "Helyiség hõm. HK 4": "room_4_temperature",
    "Helyiség hõm. HK 5": "room_5_temperature",
    "Helyiség hõm. HK 6": "room_6_temperature",
    "Helyiség hõm. HK 7": "room_7_temperature",
    "Helyiség hõm. HK 8": "room_8_temperature",
    "Elõrem.hõm. 0": "circuit_0_temp",
    "Elõrem.hõm. 1": "circuit_1_temp",
    "Elõrem.hõm. 2": "circuit_2_temp",
    "Elõrem.hõm. 3": "circuit_3_temp",
    "Elõrem.hõm. 4": "circuit_4_temp",
    "Elõrem.hõm. 5": "circuit_5_temp",
    "Elõrem.hõm. 6": "circuit_6_temp",
    "Elõrem.hõm. 7": "circuit_7_temp",
    "Elõrem.hõm. 8": "circuit_8_temp",
    "Program HK0": "heating_circulation_program_0",
    "Program HK1": "heating_circulation_program_1",
    "Program HK2": "heating_circulation_program_2",
    "Program HK3": "heating_circulation_program_3",
    "Program HK4": "heating_circulation_program_4",
    "Program HK5": "heating_circulation_program_5",
    "Program HK6": "heating_circulation_program_6",
    "Program HK7": "heating_circulation_program_7",
    "Program HK8": "heating_circulation_program_8",
    "Zavar 1": "interruption_1",
    "Zavar 2": "interruption_2",
    "Széria": "serial",
    "Verzió": "version",
    "Üzemórák": "operating_time",
    "Szervizidõ": "service_hours",
    "Kiegészít meleg víz 1": "extra_dhw_1_temperature",
    "Kiegészít meleg víz 2": "extra_dhw_2_temperature",
    "P Kiegészítõ meleg víz 0": "extra_dhw_boost_0",
    "P Kiegészítõ meleg víz 1": "extra_dhw_boost_1",
    "P Kiegészítõ meleg víz 2": "extra_dhw_boost_2",
    "Puffer fent 0": "buffer_top_0_temperature",
    "Puffer lent 0": "buffer_bottom_0_temperature",
    "Puffer fent 1": "buffer_top_1_temperature",
    "Puffer lent 1": "buffer_bottom_1_temperature",
    "Puffer fent 2": "buffer_top_2_temperature",
    "Puffer lent 2": "buffer_bottom_2_temperature",
    "táv. szivattyú 0": "auxiliary_pump_0",
    "táv. szivattyú 1": "auxiliary_pump_1",
    "táv. szivattyú 2": "auxiliary_pump_2",
    # dutch
    "Bedrijf": "status",
    "Keteltemperatuur": "boiler_temperature",
    "Buitentemperatuur": "outdoor_temperature",
    "Bufferlading": "buffer_load",
    "Buffer boven": "buffer_top_temperature",
    "Buffer midden": "buffer_center_temperature",
    "Buffer onder": "buffer_bottom_temperature",
    "Ketellaadpomp": "boiler_shunt_pump",
    "zuig/blaas ventilator": "suction_fan",
    "Primaire lucht": "primary_air",
    "Secundaire lucht": "secondary_air",
    "CO2 gehalte": "co2_content",
    "Warmwater 0": "domestic_hot_water_0_temperature",
    "Warmwater 1": "domestic_hot_water_1_temperature",
    "Warmwater 2": "domestic_hot_water_2_temperature",
    "warmwaterpomp 0": "dhw_pump_0",
    "warmwaterpomp 1": "dhw_pump_1",
    "warmwaterpomp 2": "dhw_pump_2",
    "Verwarmingskring pomp 0": "heating_circulation_pump_0",
    "Verwarmingskring pomp 1": "heating_circulation_pump_1",
    "Verwarmingskring pomp 2": "heating_circulation_pump_2",
    "Verwarmingskring pomp 3": "heating_circulation_pump_3",
    "Verwarmingskring pomp 4": "heating_circulation_pump_4",
    "Verwarmingskring pomp 5": "heating_circulation_pump_5",
    "Verwarmingskring pomp 6": "heating_circulation_pump_6",
    "Verwarmingskring pomp 7": "heating_circulation_pump_7",
    "Verwarmingskring pomp 8": "heating_circulation_pump_8",
    "Ruimtetemp. HK 0": "room_0_temperature",
    "Ruimtetemp. HK 1": "room_1_temperature",
    "Ruimtetemp. HK 2": "room_2_temperature",
    "Ruimtetemp. HK 3": "room_3_temperature",
    "Ruimtetemp. HK 4": "room_4_temperature",
    "Ruimtetemp. HK 5": "room_5_temperature",
    "Ruimtetemp. HK 6": "room_6_temperature",
    "Ruimtetemp. HK 7": "room_7_temperature",
    "Ruimtetemp. HK 8": "room_8_temperature",
    "Aanvoer_is 0": "circuit_0_temp",
    "Aanvoer_is 1": "circuit_1_temp",
    "Aanvoer_is 2": "circuit_2_temp",
    "Aanvoer_is 3": "circuit_3_temp",
    "Aanvoer_is 4": "circuit_4_temp",
    "Aanvoer_is 5": "circuit_5_temp",
    "Aanvoer_is 6": "circuit_6_temp",
    "Aanvoer_is 7": "circuit_7_temp",
    "Aanvoer_is 8": "circuit_8_temp",
    "Programma": "program",
    "Progamma HK0": "heating_circulation_program_0",
    "Progamma HK1": "heating_circulation_program_1",
    "Progamma HK2": "heating_circulation_program_2",
    "Progamma HK3": "heating_circulation_program_3",
    "Progamma HK4": "heating_circulation_program_4",
    "Progamma HK5": "heating_circulation_program_5",
    "Progamma HK6": "heating_circulation_program_6",
    "Progamma HK7": "heating_circulation_program_7",
    "Progamma HK8": "heating_circulation_program_8",
    "Storing 1": "interruption_1",
    "Storing 2": "interruption_2",
    "Versie": "version",
    "Bedrijfsuren": "operating_time",
    "Servicetijd": "service_hours",
    "extra warmw. 1": "extra_dhw_1_temperature",
    "extra warmw. 2": "extra_dhw_2_temperature",
    "P extra warmw. 0": "extra_dhw_boost_0",
    "P extra warmw. 1": "extra_dhw_boost_1",
    "P extra warmw. 2": "extra_dhw_boost_2",
    "Buffer boven 0": "buffer_top_0_temperature",
    "Buffer onder 0": "buffer_bottom_0_temperature",
    "Buffer boven 1": "buffer_top_1_temperature",
    "Buffer onder 1": "buffer_bottom_1_temperature",
    "Buffer boven 2": "buffer_top_2_temperature",
    "Buffer onder 2": "buffer_bottom_2_temperature",
}

TRANSLATE_PROGRAM = {
    # english
    "off": "off",
    "timer": "timer",
    "dhw": "dhw",
    "heat": "heat",
    "hibernat": "hibernate",
    "hibernate to": "hibernate_to",
    "dhw boost": "dhw_boost",
    # spanish
    "acs": "dhw",
    "calentar": "heat",
    "reducido": "hibernate",
    "reducido hasta": "hibernate_to",
    "impulsión acs": "dhw_boost",
    # German
    "aus": "off",
    "normal": "timer",
    "warmwasser": "dhw",
    "heizen": "heat",
    "absenken": "hibernate",
    "absenken bis": "hibernate_to",
    "ww-nachladen": "dhw_boost",
    # french
    "ecs": "dhw",
    "chauffage": "heat",
    "dimin.": "hibernate",
    "dimin.jusq.": "hibernate_to",
    "recharge ecs": "dhw_boost",
    # italian
    "normale": 'timer',
    "bollit": 'dhw',
    "risc": 'heat',
    'ridur': 'hibernate',
    'ridurre fino': 'hibernate_to',
    'cari.bollit': 'dhw_boost',
    # czech
    "tuv": "dhw",
    "topeni": "heat",
    "utlum": "hibernate",
    "utlum do": "hibernate_to",
    "tuv dohrev": "dhw_boost",
    # Slovenian
    "izklop": "off",
    "topla voda": "dhw",
    "normalno": "timer",
    "gretje": "heat",
    "znizaj": "hibernate",
    "znizaj do": "hibernate_to",
    "ogrej vodo": "dhw_boost",
    # hungarian
    "ki": "off",
    "normál": "timer",
    "meleg víz": "dhw",
    "fûtés": "heat",
    "csökkent": "hibernate",
    "csökkent -ig": "hibernate_to",
    "hmv utántöltés": "dhw_boost",
    # nederlands
    "uit": "off",
    "normaal": "timer",
    "warmwater": "dhw",
    "verwarmen": "heat",
    "reduceren": "hibernate",
    "reduceren tot": "hibernate_to",
    "ww-naloop": "dhw_boost",
}

# Values for the heating circulation program (HK001, Program HCx)
# as reported in daqdata.cgi, for all languages supported by the heater.
# Discovered from the internal parameter file (par.cgi) in each language.
TRANSLATE_HC_PROGRAM = {
    # english
    "off": "off",
    "timer": "timer",
    "heat": "heat",
    "hibernat": "hibernate",
    "hibernate to": "hibernate_to",
    # spanish
    "normal": "timer",
    "calentar": "heat",
    "reducido": "hibernate",
    "reducido hasta": "hibernate_to",
    # german
    "aus": "off",
    "heizen": "heat",
    "absenken": "hibernate",
    "absenken bis": "hibernate_to",
    # french
    "chauffage": "heat",
    "dimin.": "hibernate",
    "dimin.jusq.": "hibernate_to",
    # italian
    "normale": "timer",
    "risc": "heat",
    "ridur": "hibernate",
    "ridurre fino": "hibernate_to",
    # czech
    "vypnuto": "off",
    "topeni": "heat",
    "utlum": "hibernate",
    "utlum do": "hibernate_to",
    # slovenian
    "izklop": "off",
    "normalno": "timer",
    "gretje": "heat",
    "znizaj": "hibernate",
    "znizaj do": "hibernate_to",
    # hungarian
    "ki": "off",
    "normál": "timer",
    "fûtés": "heat",
    "csökkent": "hibernate",
    "csökkent -ig": "hibernate_to",
    # dutch
    "uit": "off",
    "normaal": "timer",
    "verwarmen": "heat",
    "reduceren": "hibernate",
    "reduceren tot": "hibernate_to",
}

# Operating mode values reported for pumps (heating_circulation_pump_x,
# auxiliary_pump_x, extra_dhw_boost_x): AUTO, OFF, NONSTP in each language.
TRANSLATE_PUMP_MODE = {
    # english
    "auto": "auto",
    "off": "off",
    "nonstp": "nonstop",
    # spanish
    "duración": "nonstop",
    # german
    "aus": "off",
    "dauer": "nonstop",
    # french
    "duree": "nonstop",
    # italian
    "contin": "nonstop",
    # czech
    "vyp": "off",
    "trvale": "nonstop",
    # slovenian
    "avto": "auto",
    "izkklop": "off",  # typo present in slovenian firmware
    "trajno": "nonstop",
    # hungarian
    "ki": "off",
    "tartós": "nonstop",
    # dutch
    "uit": "off",
    "continue": "nonstop",
}


# Placeholder temperatures reported for unconfigured sensors. Compared
# numerically, as the number of decimals differs between firmwares.
DEFAULT_TEMPERATURES = {-20.0, -9.0, 43.0, 44.0, 49.0, 60.0, 120.0}

# Placeholder temperatures reported by absent buffer stages.
BUFFER_PLACEHOLDER_TEMPERATURES = {-20.0, 120.0}


def _is_default_temperature(entry: list) -> bool:
    """Return whether a sensor entry holds a placeholder temperature."""
    if not entry or len(entry) < 2 or entry[1] != "\u00b0C":
        return False
    try:
        return float(entry[0]) in DEFAULT_TEMPERATURES
    except ValueError:
        return False


class UnexpectedDataEncounteredException(Exception):
    """
    Raised when unexpected data is encountered
    This should not happen, please open a bug against guntamatic library on pypi
    """


def _remove_placeholder_slots(data: dict[str, list]) -> None:
    """Remove sensors of slots that report a placeholder temperature.

    A placeholder room temperature hides the entire circuit slot; a
    placeholder flow temperature only hides the flow temperature, pump and
    program. A default DHW temperature hides the DHW temperature and pump.
    """
    for nr in range(10):
        room_key = f"room_{nr}_temperature"
        flow_key = f"circuit_{nr}_temp"
        pump_key = f"heating_circulation_pump_{nr}"
        program_key = f"heating_circulation_program_{nr}"
        if _is_default_temperature(data.get(room_key)):
            data.pop(room_key, None)
            related = (flow_key, pump_key, program_key)
        elif _is_default_temperature(data.get(flow_key)):
            related = (flow_key, pump_key, program_key)
        else:
            continue
        for key in related:
            data.pop(key, None)
    for nr in range(3):
        dhw_key = f"domestic_hot_water_{nr}_temperature"
        if _is_default_temperature(data.get(dhw_key)):
            data.pop(dhw_key, None)
            data.pop(f"dhw_pump_{nr}", None)
            data.pop(f"extra_dhw_boost_{nr}", None)
    for nr in range(3):
        for key in (f"buffer_top_{nr}_temperature", f"buffer_bottom_{nr}_temperature"):
            entry = data.get(key)
            if entry and entry[1] == "\u00b0C":
                try:
                    if float(entry[0]) in BUFFER_PLACEHOLDER_TEMPERATURES:
                        data.pop(key, None)
                except ValueError:
                    pass


class NoSerialException(Exception):
    """
    Raised when no serial was present in the data
    """


class Heater:
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
        desc = desc.text.split('\n')
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

        # Unconfigured slots report placeholder temperatures.
        _remove_placeholder_slots(out)
        if 'serial' not in out or not out['serial']:
            raise NoSerialException
        # Translate values as wel for known enums
        if 'program' in out:
            try:
                out['program'][0] = TRANSLATE_PROGRAM[out['program'][0].lower()]
            except KeyError:
                logging.warning('Untranslated string detected for %s, please open an issue on '
                                'https://github.com/JensTimmerman/guntamatic/issues for this',
                                out['program'][0])
        for key in list(out):
            if key.startswith('heating_circulation_program_'):
                translation = TRANSLATE_HC_PROGRAM
            elif key.startswith(('heating_circulation_pump_',
                                 'auxiliary_pump_',
                                 'extra_dhw_boost_')):
                translation = TRANSLATE_PUMP_MODE
            else:
                continue
            try:
                out[key][0] = translation[out[key][0].strip().lower()]
            except KeyError:
                logging.warning('Untranslated string detected for %s, please open an issue on '
                                'https://github.com/JensTimmerman/guntamatic/issues for this',
                                out[key][0])

        # The heater reports the time until/before service either in days or in
        # hours depending on model/firmware. Normalize into both views so
        # consumers can rely on stable units.
        if 'service_hours' in out:
            value = out['service_hours'][0]
            unit = str(out['service_hours'][1]).strip().lower()
            try:
                amount = float(str(value).replace(',', '.'))
            except ValueError:
                amount = None
            if amount is not None and unit.startswith(('d', 'h')):
                days = amount if unit.startswith('d') else amount / 24
                hours = amount if unit.startswith('h') else amount * 24
                out['service_days'] = [f"{days:g}", "d"]
                out['service_hours'] = [f"{hours:g}", "h"]

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
