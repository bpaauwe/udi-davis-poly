#!/usr/bin/env python3
"""
Polyglot v2 node server for Davis  WeatherLink Station data.
Copyright (c) 2020 Robert Paauwe
"""
import polyinterface
import sys
import time
import datetime
import threading
from nodes import davis

LOGGER = polyinterface.LOGGER

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('Davis')
        polyglot.start()
        control = davis.Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
