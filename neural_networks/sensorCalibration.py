__author__ = 'estsauver'


def temperature(pins):
    #We only need one pin to get the temp
    assert len(pins) == 1

    # If the arduino hasn't returned any data, send back a False value so it won't be processed.
    if pins[0] == None:
        return (False, -1)
    value = pins[0] * 100
    error = 2
    return (value, error)


def pH(pins):
    ''' Takes a list of pin values and returns the value and the error.
    '''
    assert len(pins) == 2
    #If either pin has no
    if pins[0] == None or pins[1] == None:
        return (False, -1)
    value = (pins[0] - pins[1]) * 1000
    error = 3
    return (value, error)