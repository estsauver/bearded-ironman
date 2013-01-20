from nose.tools import *
import unittest
import bioduino
import pyfirmata
import pyfirmata.mockup
import dataProcessing
from sqlalchemy.sql import desc
from sensorCalibration import  sensorPins

class ReactorBaseTest(unittest.TestCase):

    def setUp(self):
        bioduino.sampling_interval = 0.5
        bioduino.pyfirmata.BOARD_SETUP_WAIT_TIME = 0
        bioduino.pyfirmata.serial.Serial = pyfirmata.mockup.MockupSerial
        self.reactor = bioduino.Bioreactor(sensorPins,1)
        self.reactor.board = pyfirmata.mockup.MockupBoard("",pyfirmata.BOARDS["arduino"])
        self.reactor.board.values_dict = {
            "a":
            #Analog Pins
                {1:100,
                 2:50,
                 3:10
                }

        }
        self.reactor.board.update_values_dict
        self.reactor.startExperiment()



class InputTest(ReactorBaseTest):
    def testSaveExperiment(self):
        dbExperiment = self.reactor.session.query(dataProcessing.Experiment).order_by(desc(dataProcessing.Experiment.id)).first()
        print "Saved Experiment: %s, Current Experiment: %s" % (dbExperiment.id, self.reactor.experiment.id)
        self.assertEqual(dbExperiment,self.reactor.experiment,"Experiment not saved")

    def testSaveDatapoint(self):
        dbDatapoint = self.reactor.session.query(dataProcessing.Datapoint).order_by(desc(dataProcessing.Datapoint.id)).first()
        assert(isinstance(dbDatapoint,dataProcessing.Datapoint))
        assert(isinstance(dbDatapoint.value, float ))
        self.assertEqual(1,2,msg=dbDatapoint.id)

