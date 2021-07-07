#!/usr/bin/env python3
"""
Polyglot v2 node server for Davis WeatherLink Weather Station data.
Copyright (c) 2020 Robert Paauwe
"""
import polyinterface
import sys
import time
import datetime
import json
import math
import node_funcs
from nodes import uom

LOGGER = polyinterface.LOGGER

@node_funcs.add_functions_as_methods(node_funcs.functions)
class YearNode(polyinterface.Node):
    
    def SetUnits(self, units):
        LOGGER.debug('set units info')
        self.units=units
        self.uom = uom.get_uom(self.units)

    def parse(self, jdata):
        LOGGER.debug('Parse jdata for year data here')
        try:
            obs = jdata['davis_current_observation']
            if self.units == 'us':
                if 'temp_year_high_f' in obs:
                    self.update_driver('GV0', obs['temp_year_high_f'])
                if 'temp_year_low_f' in obs:
                    self.update_driver('GV1', obs['temp_year_low_f'])
                if 'dewpoint_year_high_f' in obs:
                    self.update_driver('GV2', obs['dewpoint_year_high_f'])
                if 'dewpoint_year_low_f' in obs:
                    self.update_driver('GV3', obs['dewpoint_year_low_f'])
                if 'heat_index_year_high_f' in obs:
                    self.update_driver('GV4', obs['heat_index_year_high_f'])
                if 'windchill_year_low_f' in obs:
                    self.update_driver('GV5', obs['windchill_year_low_f'])
                if 'relative_humidity_year_high' in obs:
                    self.update_driver('GV8', obs['relative_humidity_year_high'])
                if 'relative_humidity_year_low' in obs:
                    self.update_driver('GV9', obs['relative_humidity_year_low'])
                if 'pressure_year_high_in' in obs:
                    self.update_driver('GV10', obs['pressure_year_high_in'])
                if 'pressure_year_low_in' in obs:
                    self.update_driver('GV11', obs['pressure_year_low_in'])
                if 'rain_year_in' in obs:
                    self.update_driver('GV12', obs['rain_year_in'])
                if 'rain_rate_year_high_in_per_hr' in obs:
                    self.update_driver('RAINRT', obs['rain_rate_year_high_in_per_hr'])
                if 'wind_year_high_mph' in obs:
                    self.update_driver('SPEED', obs['wind_year_high_mph'])
                if 'solar_radiation_year_high' in obs:
                    self.update_driver('SOLRAD', obs['solar_radiation_year_high'])
                if 'uv_index_year_high' in obs:
                    self.update_driver('UV', obs['uv_index_year_high'])
                if 'et_year' in obs:
                    self.update_driver('GV20', obs['et_year'])
            else:
                if 'temp_year_high_f' in obs:
                    tempyrh = uom.ftoc(float(obs['temp_year_high_f']))
                    self.update_driver('GV0', tempyrh)
                if 'temp_year_low_f' in obs:
                    tempyrl = uom.ftoc(float(obs['temp_year_low_f']))
                    self.update_driver('GV1',tempyrl)
                if 'dewpoint_year_high_f' in obs:
                    dewpointyrh = uom.ftoc(float(obs['dewpoint_year_high_f']))
                    self.update_driver('GV2',dewpointyrh)
                if 'dewpoint_year_low_f' in obs:
                    dewpointyrl = uom.ftoc(float(obs['dewpoint_year_low_f']))
                    self.update_driver('GV3',dewpointyrl)
                if 'heat_index_year_high_f' in obs:
                    heatiyrh = uom.ftoc(float(obs['heat_index_year_high_f']))
                    self.update_driver('GV4', heatiyrh)
                if 'windchill_year_low_f' in obs:
                    wincyrl = uom.ftoc(float(obs['windchill_year_low_f']))
                    self.update_driver('GV5', wincyrl)
                if 'relative_humidity_year_high' in obs:
                    self.update_driver('GV8', obs['relative_humidity_year_high'])
                if 'relative_humidity_year_low' in obs:
                    self.update_driver('GV9', obs['relative_humidity_year_low'])
                if 'pressure_year_high_in' in obs:
                    pressyrh = uom.inhgtomb(float(obs['pressure_year_high_in']))
                    self.update_driver('GV10', pressyrh)
                if 'pressure_year_low_in' in obs:
                    pressyrl = uom.inhgtomb(float(obs['pressure_year_low_in']))
                    self.update_driver('GV11', pressyrl)
                if 'rain_year_in' in obs:
                    rainyr = uom.inchtomm(float(obs['rain_year_in']))
                    self.update_driver('GV12', rainyr)
                if 'rain_rate_year_high_in_per_hr' in obs:
                    rainyrh = uom.inchtomm(float(obs['rain_rate_year_high_in_per_hr']))
                    self.update_driver('RAINRT', rainyrh)
                if 'wind_year_high_mph' in obs:
                    winyrh = uom.mphtokmh(float(obs['wind_year_high_mph']))
                    self.update_driver('SPEED', winyrh)
                if 'solar_radiation_year_high' in obs:
                    self.update_driver('SOLRAD', obs['solar_radiation_year_high'])
                if 'uv_index_year_high' in obs:
                    self.update_driver('UV', obs['uv_index_year_high'])
                if 'et_year' in obs:
                    etmoyrm= uom.inchtomm(float(obs['et_year']))
                    self.update_driver('GV20', etmoyrm)
            
        except Exception as e:
            LOGGER.error('Parse failure for year: ' + str(e))
            LOGGER.debug(obs)

    id = 'year'
    hint = [1,11,4,0]
    uom = {}
    drivers = [
            {'driver': 'GV0', 'value': 0, 'uom': 17}, # temp high
            {'driver': 'GV1', 'value': 0, 'uom': 17}, # temp low
            {'driver': 'GV2', 'value': 0, 'uom': 17}, # dewpt high
            {'driver': 'GV3', 'value': 0, 'uom': 17}, # dewpt low
            {'driver': 'GV4', 'value': 0, 'uom': 17}, # heatidx high
            {'driver': 'GV5', 'value': 0, 'uom': 17}, # windchill low
            {'driver': 'GV8', 'value': 0, 'uom': 22}, # humidity high
            {'driver': 'GV9', 'value': 0, 'uom': 22}, # humidity low
            {'driver': 'GV10', 'value': 0, 'uom': 23},  # pressure high
            {'driver': 'GV11', 'value': 0, 'uom': 23},  # pressure low
            {'driver': 'GV12', 'value': 0, 'uom': 105}, # preciptitation
            {'driver': 'RAINRT', 'value': 0, 'uom': 24},# rain rate
            {'driver': 'SPEED', 'value': 0, 'uom': 48}, # wind speed
            {'driver': 'SOLRAD', 'value': 0, 'uom': 74},# Solarradiation
            {'driver': 'UV', 'value': 0, 'uom': 71},    # UV Index
            {'driver': 'GV20', 'value': 0, 'uom': 120}, # ETo
            ]


