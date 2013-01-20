__author__ = 'estsauver@gmail.com'

import sys
import pyfirmata
import pyfirmata.mockup
import dataProcessing
from sensorCalibration import temperature, pH, sensorPins

#########################################################
# CONSTANTS
#########################################################
#This defines our sampling interval in seconds. I'm not sure if this includes the rest of the time
#the code takes to execute or not.
sampling_interval = 10

#This is the port that the arduino is on. This may be different on different operating systems.
port = "/dev/tty.usbmodem621"

#This code defines the testing data
ISTESTING = True

class Bioreactor(object):
    def __init__(self, sensorPins):
        '''Initializes the bioreactor, the board iterator, and the SQLAlchemy session for storage.

         sensorPins is a dictionary of the functions in sensorCalibration.py to the pins that they're connected to.
        '''
        self.sensorPinDict = sensorPins
        try:
            self.board = pyfirmata.Arduino(port)
            #THe iterator construct keeps the board from sending *too much* data to the serial. This causes it to just update very
            # regular instead of continuously streaming to the serial.
            it = pyfirmata.util.Iterator(self.board)
            it.start()
            # For every sensor and their pins in our dictionary...
            for sensorType, pins in sensorPins.iteritems():
            #   For every pin in the list of pins...
                for pin in pins:
                #       Turn on reporting.
                    self.board.analog[pin].enable_reporting()
        except AttributeError:
            print "Board connection failed"
            sys.exit("Could not connect to arduino board")
            # This starts the datbase session that we save things to.
        self.session = dataProcessing.Session()

    def startExperiment(self):
        #create a new experiment to assosciate the datapoints with
        self.experiment = dataProcessing.Experiment()
        #Moves the experiment into the sessions temporary storage.
        self.session.add(self.experiment)
        #Commits the experiment to memory.
        self.session.commit()
        self.runloop()

    def runloop(self):
        """This is the eventloop. It goes for forever, until the program is killed. We might replace this with a
        Qt Application Core loop since it seems like it might handle abrupt exits better."""
        dataPointNumber = 0
        while True:
            self.record_data(dataPointNumber)
            self.session.commit()
            dataPointNumber += 1

            #Waits 10 seconds, this is ~approximately our sampling interval.
            self.board.pass_time(sampling_interval)

    def record_data(self,dataPointNumber):
        for sensortype, pins in self.sensorPinDict.iteritems():
            #readpins is an inline function that we apply to every pin we have for a sensor to get all of the readings.
            readpins = lambda x: self.board.analog[x].read()
            pinvalues = map(readpins, pins)

            #        This calls the sensor calibration function for whatever sensor is being iteratred through on the pinvalues we
            #        just read in. For example this will call temperature(pinvalues) when it's handling the tempearture sensor.
            (value, valueerror) = sensortype(pinvalues)

            #        Sometimes when the board is first initialized the board will have value errors where it will send None values.

            if value != False:
            #            type.__name__ returns the string that's the function name which, in our case equals the sensor name.
                newPoint = dataProcessing.Datapoint(value, valueerror, type.__name__, self.experiment,dataPointNumber)
                self.session.add(newPoint)
                print newPoint
            else:
                #        TODO: Add error handler.
                print "Bad Data of type %s with pin values %s" % (type.__name__, pinvalues)
                #   We commit the data after we have read for every sensor. This drops the database overhead. If it turns out to be a
                #   problem we can commit more occasionally.
if __name__=="__main__":
    reactor = Bioreactor(sensorPins)
    reactor.startExperiment()