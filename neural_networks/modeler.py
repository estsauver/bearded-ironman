__author__ = 'estsauver'

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from scipy.spatial import cKDTree
import scipy
from math import fabs
from sensorCalibration import sensorPins


#Constants for our program.
hiddenLayerSize = 3
nInp = 3
kNearest = 4

#We initialize the dataset container for the neural network here.
dataset = SupervisedDataSet(nInp, 1)


#Temporarily generated datapoints.
tempPoints = [100,99,99,100,101,102,100,104, 100,99,99,100,101,102,100,104]
tPoints = [1,2,3,1,5,6,7,8,  100,99,99,100,101,102,100,104]
doPoints = [20,20,20,19,20,20,15,15, 100,99,99,100,101,102,100,104]

#Alcohol points, outputs
alcoholPoints = scipy.random.random(16).transpose()
#Normalize alcohol


data = scipy.transpose(scipy.array([tempPoints,tPoints, doPoints],dtype=float))

#Normalization
data = (data-data.min(axis=0))/(data.max(axis=0)-data.min(axis=0))

##Create an empty object to hold the output of the standard deivation test
#filteredPoints = scipy.empty(3)

#kDTree's initialization
kTree = cKDTree(data)

#Running through each of the data points and calculating standard deviation
#For their kNearest neighbors.
for i in data:
#    print i
    #Get the kNearest = 3 points from the tree, the +1 is because this query
    # will return the point itself as well.

    nearestThree = kTree.query(i, k= kNearest+1)

    #The query function returns a tuple, and the second value is the list of indexes for
    #the three datapoints. This gets their actual values.
    test= alcoholPoints[nearestThree[1]]


    #Calculate it's standard deviation
    dev = scipy.std(test)

    mean = scipy.mean(test)
    yi = alcoholPoints[nearestThree[1][0]]
    if yi == mean:
        distance = 0
    else:
        distance = fabs((yi-mean)/dev)
    print "Distance for row {} is {}".format(i,distance )

    #This section of the code appends the arrays. it uses a try/catch block to create the array if
    # it does not exist when the code first runs. vstack is an append like function.
    if distance < 1:
        try:
            filteredPoints = scipy.vstack((filteredPoints,i))
        except NameError:
            filteredPoints = i

        try:
            alcoholFilteredPoints = scipy.vstack((alcoholFilteredPointsPoints, yi))
        except NameError:
            alcoholFilteredPoints = yi

        try:
            importanceWeights = scipy.vstack((importanceWeights,distance))
        except NameError:
            importanceWeights = distance

        dataset.addSample(i.tolist(), yi.tolist())



# Information about the dataset
print "Length of dataset: {}".format(len(dataset))
print "Dataset Inputs: {}".format(dataset['input'])
print "Dataset Ouptuts: {}".format(dataset['target'])


# Neural Network Part
net = buildNetwork(nInp, 1, 1, bias=True)
trainer = BackpropTrainer(net, dataset)
trainer.trainUntilConvergence(dataset)
print "Nerual net generates {}".format(net.activate([12,1,5]))


