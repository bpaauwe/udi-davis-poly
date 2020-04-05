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
    id = 'year'
    hint = [1,11,4,0]
    units = 'us'
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


    def SetUnits(self, units):
        LOGGER.debug('set units info')
        self.uom = uom.get_uom(self.units)

    def parse(self, jdata):
        LOGGER.debug('Parse jdata for year data here')
        try:
            obs = jdata['davis_current_observation']
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
            if 'un_index_year_high' in obs:
                self.update_driver('UV', obs['uv_index_year_high'])
            if 'et_year' in obs:
                self.update_driver('GV20', obs['et_year'])
        except Exception as e:
            LOGGER.error('Parse failure for year: ' + str(e))
            LOGGER.debug(obs)



