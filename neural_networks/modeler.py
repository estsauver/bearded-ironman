__author__ = 'estsauver'

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets.importance import ImportanceDataSet

class reactor_modeler(object):
    def __init__(self, sensorPins, hiddenLayerSize=10):
        assert (type(sensorPins) == dict)

        self.net = buildNetwork(len(sensorPins.keys), hiddenLayerSize, len(sensorPins), bias=true)
        self.dataset = ImportanceDataSet(len(sensorPins.keys), len(sensorPins.keys))

    def add_trained_datapoint(self, inputDataPoint, outputDataPoint):
        self.dataset.addSample()