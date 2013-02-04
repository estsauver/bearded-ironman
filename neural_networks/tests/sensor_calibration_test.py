__author__ = 'estsauver'
import unittest

from sensorCalibration import *

class SensorCalibrationTest(unittest.TestCase):

    def setUp(self):
        pass

    def testPH(self):
        lowValue = [0]
        self.assertEqual(temperature(lowValue),0)
        self.assertEquals(type(temperature(lowValue)), type(1.00))

    def testTemp(self):
        lowValue = [0]
        self.assertEqual(temperature(lowValue),0)

        highValue = [205]

        self.assertGreater(temperature(highValue),100)


