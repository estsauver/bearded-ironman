__author__ = 'estsauver@gmail.com'

import sys
import pyfirmata
import pyfirmata.mockup
import dataProcessing


#Here we grab the functions for all the sensors that we need.
from sensorCalibration import temperature, pH

#This defines our sampling interval in seconds. I'm not sure if this includes the rest of the time
#the code takes to execute or not.
sampling_interval = 10

#This code defines the testing data
ISTESTING = True


# This starts the datbase session that we save things to.
session = dataProcessing.Session()

#create a new experiment to assosciate the datapoints with
experiment = dataProcessing.Experiment()

#Moves the experiment into the sessions temporary storage.
session.add(experiment)
#Commits the experiment to memory.
session.commit()

# This is a dictionary that maps the functions from sensorCalibration.py to the pins their results come from. The
# pins must be a list.
sensorPins = {temperature: [1], pH: [2, 3]}

#This is the port that the arduino is on. This may be different on different operating systems.

#We try to connect to the board and if that fails we print a warning.
if ISTESTING:
    pyfirmata.pyfirmata.serial.Serial = pyfirmata.mockup.MockupSerial
    board=pyfirmata.mockup.MockupBoard("",pyfirmata.BOARDS["arduino"])
else:
    port = "/dev/tty.usbmodem621"
    try:
        board = pyfirmata.Arduino(port)
    except AttributeError:
        print "Board connection failed"
        sys.exit("Could not connect to arduino board")



#THe iterator construct keeps the board from sending *too much* data to the serial. This causes it to just update very
# regular instead of continuously streaming to the serial.
it = pyfirmata.util.Iterator(board)
it.start()




#For every sensor and their pins in our dictionary...
for sensorType, pins in sensorPins.iteritems():
#   For every pin in the list of pins...
    for pin in pins:
    #       Turn on reporting.
        board.analog[pin].enable_reporting()

# This is the eventloop. It goes for forever, until the program is killed. We might replace this with a
# Qt Application Core loop since it seems like it might handle abrupt exits better.
dataPointNumber = 0
while True:
    for type, pins in sensorPins.iteritems():
    #       readpins is an anonymous function that we apply to every pin we have for a sensor to get all of the readings.
        readpins = lambda x: board.analog[x].read()
        pinvalues = map(readpins, pins)

        #        This calls the sensor calibration function for whatever sensor is being iteratred through on the pinvalues we
        #        just read in. For example this will call temperature(pinvalues) when it's handling the tempearture sensor.
        (value, valueerror) = type(pinvalues)

        #        Sometimes when the board is first initialized the board will have value errors where it will send None values.

        if value != False:
        #            type.__name__ returns the string that's the function name which, in our case equals the sensor name.
            newPoint = dataProcessing.Datapoint(value, valueerror, type.__name__, experiment,dataPointNumber)
            session.add(newPoint)
            print newPoint
        else:
            #        TODO: Add error handler.
            print "Bad Data of type %s with pin values %s" % (type.__name__, pinvalues)
        #   We commit the data after we have read for every sensor. This drops the database overhead. If it turns out to be a
        #   problem we can commit more occasionally.
    session.commit()
    dataPointNumber += 1

    #Waits 10 seconds, this is ~approximately our sampling interval.
    board.pass_time(sampling_interval)

