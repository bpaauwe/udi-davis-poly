
def get_trend(trend):
    if trend == 'Falling':
        return 0
    elif trend == 'Steady':
        return 1
    elif trend == 'Rising':
        return 2
    elif trend == 'Rising Slowly':
        return 3
    elif trend == 'Falling Slowly':
        return 4
    elif trend == 'Rising Rapidly':
        return 5
    elif trend == 'Falling Rapidly':
        return 6

    return 1
