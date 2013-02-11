__author__ = ['estsauver', 'johnabel']

#scale 0 --> 1 sensor input

def temperature(pins):
    #We only need one pin to get the temp
    assert len(pins) == 1
    # If the arduino hasn't returned any data, send back a False value so it won't be processed.
    if pins[0] == None:
        return (False, -1)
    value = 100*pins[0]/(1024*5)
    error = 2
    return (value, error)


def pH(pins):
    ''' Takes a list of pin values and returns the value and the error.
    '''
    assert len(pins) == 1
    if pins[0] == None:
        return (False, -1)
    value = 2+10*pins[1]/(1024*5)
    error = 3
    return (value, error)

def DO(pins):
    ''' Takes a list of pin values and returns the value and the error.
    '''
    assert len(pins) == 1
    if pins[0] == None:
        return (False, -1)
    value = 200*pins[2]/1024*5)
    error = 4

def Agitation(pins):
    ''' Takes a list of pin values and returns the value and the error.
    '''
    assert len(pins) == 1
    if pins[0] == None:
        return (False, -1)
    value = 1500*pins[3]/(1024*5)
    error = 5
    
sensorPins = {temperature: [1], pH: [2], DO: [3], Agitataion: [4]}
