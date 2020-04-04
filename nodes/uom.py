#
#  Unit of Measure configuration function
#
#  Return a dictionary with driver names as the key and the UOM for
#  the requested unit configuration.
#
#  valid unit configurations are:
#   metric, imperial, si (same as metric), us (same as imperial), uk
#
#  Ideally, there should be no conflicts between forecast and current
#  condition driver types


def get_uom(units):
    unit_cfg = units.lower()

    if unit_cfg == 'metric' or unit_cfg == 'si' or unit_cfg.startswith('m'):
        uom = {
            'ST': 2,   # node server status
            'CLITEMP': 4,   # temperature
            'CLIHUM': 22,   # humidity
            'BARPRES': 117, # pressure
            'WINDDIR': 76,  # direction
            'DEWPT': 4,     # dew point
            'SOLRAD': 74,   # solar radiation
            'RAINRT': 46,   # rain rate
            'SPEED': 32,    # wind speed
            'DISTANC': 83,  # visibility (kilometers)
            'UV': 71,       # UV index
            'GV0': 4,       # max temp
            'GV1': 4,       # min temp
            'GV2': 4,       # max dewpoint
            'GV3': 4,       # min dewpoint
            'GV4': 4,       # heat index
            'GV5': 4,       # windchill
            'GV6': 82,      # n/a 
            'GV7': 49,      # n/a 
            'GV8': 22,      # humidity high
            'GV9': 22,      # humidity low
            'GV10': 117,    # pressure high
            'GV11': 117,    # pressure low
            'GV12': 82,     # rain
            'GV13': 32,     # gusts
            'GV14': 22,     # N/A
            'GV15': 82,     # N/A
            'GV16': 25,     # pressure trend
            'GV17': 56,     # N/A
            'GV18': 22,     # N/A
            'GV19': 25,     # N/A
            'GV20': 106,    # ETo
        }
    else:
        uom = {
            'ST': 2,   # node server status
            'CLITEMP': 17,  # temperature
            'CLIHUM': 22,   # humidity
            'BARPRES': 23,  # pressure
            'WINDDIR': 76,  # direction
            'DEWPT': 17,    # dew point
            'SOLRAD': 74,   # solar radiation
            'RAINRT': 24,   # rain rate
            'SPEED': 48,    # wind speed
            'DISTANC': 116, # visibility
            'UV': 71,       # UV index
            'GV0': 17,      # max temp
            'GV1': 17,      # min temp
            'GV2': 17,      # max dewpoint
            'GV3': 17,      # min dewpoint
            'GV4': 17,      # heat index
            'GV5': 17,      # windchill
            'GV6': 105,     # N/A
            'GV7': 48,      # N/A
            'GV8': 22,      # min humidity
            'GV9': 22,      # max humidity
            'GV10': 23,     # min pressure
            'GV11': 23,     # max pressure
            'GV12': 105,    # precipitation
            'GV13': 48,     # gust
            'GV14': 22,     # N/A
            'GV15': 105,    # N/A
            'GV16': 25,     # pressure trend
            'GV17': 56,     # N/A
            'GV18': 22,     # N/A
            'GV19': 25,     # N/A
            'GV20': 120,    # ETo
        }

    return uom

# convert knots to KPH
def kt2kph(kt):
    return kt * 1.852
