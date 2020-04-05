#!/usr/bin/env python3
"""
Polyglot v2 node server for Davis WeatherLink Weather Station data.
Copyright (c) 2020 Robert Paauwe
"""
import polyinterface
import sys
import time
import datetime
import requests
import json
import socket
import math
import threading
import node_funcs
from nodes import day
from nodes import month
from nodes import year
from nodes import uom
from nodes import trend

LOGGER = polyinterface.LOGGER

@node_funcs.add_functions_as_methods(node_funcs.functions)
class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        # are these overriding the class variables?
        self.name = 'WeatherLink' 
        self.address = 'wl'
        self.primary = self.address
        self.stopping = False
        self.stopped = True
        self.poly.onConfig(self.process_config)
        self.devices = []
        self.discovered = ""
        self.configured = False
        self.tags = {}
        self.hb = 0
        self.params = node_funcs.NSParameters([{
            'name': 'User',
            'default': 'set me',
            'isRequired': True,
            'notice': 'User ID must be set',
            },
            {
            'name': 'Password',
            'default': 'set me',
            'isRequired': True,
            'notice': 'Password must be set',
            },
            {
            'name': 'API Token',
            'default': 'set me',
            'isRequired': True,
            'notice': 'API Token must be set',
            },
            {
            'name': 'Station ID',
            'default': '',
            'isRequired': False,
            'notice': '',
            },
            {
            'name': 'Units',
            'default': 'us',
            'isRequired': False,
            'notice': '',
            },
            ])

    def process_config(self, config):
        (valid, changed) = self.params.update_from_polyglot(config)
        if changed and not valid:
            LOGGER.debug('-- configuration not yet valid')
            self.removeNoticesAll()
            self.params.send_notices(self)
        elif changed and valid:
            LOGGER.debug('-- configuration is valid')
            self.removeNoticesAll()
            self.configured = True
            # Really need to do better at detecting what changed and
            # respond accordingly
        elif valid:
            LOGGER.debug('-- configuration not changed, but is valid')

    def start(self):
        LOGGER.info('Starting Davis WeatherLink Node Server')
        self.set_logging_level()
        self.check_params()
        self.discover()
        self.uom = uom.get_uom(self.params.get('Units'))
        self.set_tags(self.params.get('Units'))

        # do initial query to get data
        if self.configured:
            self.get_data()

    def shortPoll(self):
        if self.configured:
            self.get_data()

    def longPoll(self):
        self.heartbeat()

    def query(self):
        for node in self.nodes:
            self.nodes[node].reportDrivers()
        self.set_hub_timestamp()

    def discover(self, *args, **kwargs):

        node = day.DayNode(self, self.address, 'day', 'Daily Observations')
        node.SetUnits(self.params.get('Units'))
        self.addNode(node)

        node = month.MonthNode(self, self.address, 'month', 'Month Observations')
        node.SetUnits(self.params.get('Units'))
        self.addNode(node)

        node = year.YearNode(self, self.address, 'year', 'Yearly Observations')
        node.SetUnits(self.params.get('Units'))
        self.addNode(node)

    def heartbeat(self):
        LOGGER.debug('heartbeat hb={}'.format(self.hb))
        if self.hb == 0:
            self.reportCmd("DON",2)
            self.hb = 1
        else:
            self.reportCmd("DOF",2)
            self.hb = 0

    def delete(self):
        self.stopping = True
        LOGGER.info('Removing Davis WeatherLink node server.')

    def stop(self):
        self.stopping = True
        LOGGER.debug('Stopping Davis WeatherLink node server.')

    def check_params(self):
        self.removeNoticesAll()

        if self.params.get_from_polyglot(self):
            LOGGER.debug('All required parameters are set!')
            self.configured = True
        else:
            LOGGER.debug('Configuration required.')
            self.params.send_notices(self)

    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all:')
        # Remove all existing notices
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st

    def parse_current_conditions(self, jdata):
        try:
            self.update_driver('CLITEMP', jdata[self.tags['temp']])
            self.update_driver('CLIHUM', jdata[self.tags['humidity']])
            self.update_driver('DEWPT', jdata[self.tags['dewpoint']])
            self.update_driver('GV3', jdata[self.tags['heat_index']])
            self.update_driver('GV4', jdata[self.tags['windchill']])
            self.update_driver('BARPRES', jdata[self.tags['pressure']])
            self.update_driver('WINDDIR', jdata[self.tags['wind_dir']])
            if self.params.get('Units') == 'us':
                self.update_driver('SPEED', jdata[self.tags['wind_speed']])
            else:
                speed = uom.kt2kph(float(jdata[self.tags['wind_speed']]))
                self.update_driver('SPEED', speed)
            trending = trend.get_trend(jdata['davis_current_observation']['pressure_tendency_string'])
            self.update_driver('GV16', trending)
            self.update_driver('SOLRAD', jdata['davis_current_observation']['solar_radiation'])
        except Exception as e:
            LOGGER.error('Parsing failed, current conditions: ' + str(e))
            LOGGER.debug(jdata)


    def get_data(self):
        path = 'https://api.weatherlink.com/v1/NoaaExt.json?'
        path += 'user=' + self.params.get('User')
        path += '&pass=' + self.params.get('Password')
        path += '&apiToken=' + self.params.get('API Token')

        try:
            c = requests.get(path)
            LOGGER.debug('Query response = ' + str(c.status_code))
            jdata = c.json()
            c.close()
        except Exception as e:
            LOGGER.error('request failed: ' + str(e))
            LOGGER.error(c.text)
            return

        try:
            self.parse_current_conditions(jdata)
            self.nodes['day'].parse(jdata)
            self.nodes['month'].parse(jdata)
            self.nodes['year'].parse(jdata)
        except Exception as e:
            LOGGER.error('parsing failed: ' + str(e))


    def set_logging_level(self, level=None):
        if level is None:
            try:
                level = self.get_saved_log_level()
            except:
                LOGGER.error('set_logging_level: get saved log level failed.')

        if level is None:
            level = 10
            level = int(level)
        else:
            level = int(level['value'])

        self.save_log_level(level)

        LOGGER.info('set_logging_level: Setting log level to %d' % level)
        LOGGER.setLevel(level)

    def set_tags(self, units):
        if units == 'us':
            self.tags = {
                    'dewpoint':'dewpoint_f',
                    'heat_index': 'heat_index_f',
                    'pressure': 'pressure_in',
                    'humidity': 'relative_humidity',
                    'temp': 'temp_f',
                    'wind_dir': 'wind_degrees',
                    'wind_speed': 'wind_mph',
                    'windchill': 'windchill_f'
                    }
        else:
            self.tags = {
                    'dewpoint':'dewpoint_c',
                    'heat_index': 'heat_index_c',
                    'pressure': 'pressure_mb',
                    'humidity': 'relative_humidity',
                    'temp': 'temp_c',
                    'wind_dir': 'wind_degrees',
                    'wind_speed': 'wind_kt',
                    'windchill': 'windchill_c'
                    }

    id = 'WeatherLink'
    name = 'WeatherLink'
    address = 'wl'
    stopping = False
    hint = [1, 11, 0, 0]
    commands = {
        'DISCOVER': discover,
        'UPDATE_PROFILE': update_profile,
        'REMOVE_NOTICES_ALL': remove_notices_all,
        'DEBUG': set_logging_level,
    }
    # Current conditions
    drivers = [
            {'driver': 'ST', 'value': 1, 'uom': 2},
            {'driver': 'CLITEMP', 'value': 0, 'uom': 17}, # temperature
            {'driver': 'CLIHUM', 'value': 0, 'uom': 22},  # humidity
            {'driver': 'DEWPT', 'value': 0, 'uom': 17},   # dewpoint
            {'driver': 'GV3', 'value': 0, 'uom': 17},     # heat index
            {'driver': 'GV4', 'value': 0, 'uom': 17},     # windchill
            {'driver': 'BARPRES', 'value': 0, 'uom': 23}, # pressure
            {'driver': 'WINDDIR', 'value': 0, 'uom': 76}, # wind dir
            {'driver': 'SPEED', 'value': 0, 'uom': 48},   # wind speed
            {'driver': 'GV16', 'value': 0, 'uom': 25},    # pressure trend
            {'driver': 'SOLRAD', 'value': 0, 'uom': 74},  # solar radiation
            ]


