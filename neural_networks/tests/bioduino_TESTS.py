from nose.tools import *
import unittest
import bioduino
import pyfirmata
import pyfirmata.mockup
from sensorCalibration import  sensorPins
class ReactorBaseTest(unittest.TestCase):

    def setup(self):
        pyfirmata.serial.Serial = pyfirmata.mockup.MockupSerial
        self.reactor = bioduino.Bioreactor(sensorPins)
        self.reactor.startExperiment()



class InputTest(ReactorBaseTest):
    def test_testing(self):
        self.assertEqual(1,1)
        self.assertEqual(self.reactor.__class__ ,"Bioreactor")