__author__ = 'estsauver'

from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import RecurrentNetwork, LinearLayer, SigmoidLayer, FullConnection, BiasUnit, FeedForwardNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.datasets.importance import ImportanceDataSet
from pybrain.supervised.trainers import BackpropTrainer, RPropMinusTrainer
from scipy.spatial import KDTree
import scipy.io as sio
import scipy
import csv
from math import fabs
import numpy as np
import matplotlib.pyplot as plt
from sensorCalibration import sensorPins


#Constants for our program.
hiddenLayerSize = 3
nInp = 2
kNearest = 3

#We initialize the dataset container for the neural network here.
dataset = SupervisedDataSet(nInp, 1)


#Temporarily generated datapoints.
matFile1 = sio.loadmat("t.mat")
print matFile1
tHolder = matFile1['t']
tPoints = tHolder[:,0]
matFile2 = sio.loadmat("y_noise40.mat")
print matFile2
a = matFile2['y_noise40']
cellMass = a[:,0]
substrate = a[:,1]
do = a[:,3]
ph = a[:,4]

matFile3 = sio.loadmat("y_no_noise.mat")
print matFile3
alcoholPoints = matFile3['y'][:,2]


#Alcohol points, outputs
noisyBooze  = a[:,2]


data = scipy.transpose(scipy.array([ do, ph],dtype=float))

#Normalization
data = (data-data.min(axis=0))/(data.max(axis=0)-data.min(axis=0))


##Create an empty object to hold the output of the standard deivation test
#filteredPoints = scipy.empty(3)

#kDTree's initialization
kTree = KDTree(data)

#Running through each of the data points and calculating standard deviation
#For their kNearest neighbors.
removedPoints = 0

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

    try:
        importanceWeights = scipy.vstack((importanceWeights,distance))
    except NameError:
        importanceWeights = distance
    if distance < 0.313891317477:
        try:
            filteredPoints = scipy.vstack((filteredPoints,i))
        except NameError:
            filteredPoints = i

        try:
            alcoholFilteredPoints = scipy.vstack((alcoholFilteredPointsPoints, yi))
        except NameError:
            alcoholFilteredPoints = yi


#        dataset.newSequence()
        dataset.appendLinked(i.tolist(), [yi.tolist()])
    else:
        removedPoints += 1

print "Removed Points {}".format(removedPoints)
print "Average distance = {} ".format(importanceWeights.mean())
print "Distance STDdev = {}".format(importanceWeights.std())
print importanceWeights


# Information about the dataset
#print "Length of dataset: {}".format(len(dataset))
#print "Dataset Inputs: {}".format(dataset['input'])
#print "Dataset Ouptuts: {}".format(dataset['target'])

# Neural Network Part
#This is the simple feed forward network that works, in case the recurrent network doesn't work when I'm done.

#net = buildNetwork(nInp, 1, 1, bias=True)
n = RecurrentNetwork()
n.addInputModule(LinearLayer(nInp, name='in'))
#n.addInputModule(BiasUnit(name="inputBias"))
n.addModule(SigmoidLayer(5, name='hidden1'))
n.addModule(SigmoidLayer(5, name='hidden2'))

#n.addModule(BiasUnit(name="internalBias"))
n.addOutputModule(LinearLayer(1, name='out'))
n.addConnection(FullConnection(n['in'], n['hidden1'], name='c1'))
#n.addConnection(FullConnection(n['inputBias'],n['hidden1']))
n.addConnection(FullConnection(n['hidden1'], n['hidden2'], name='c3'))
n.addConnection(FullConnection(n['hidden2'],n['out']))
n.addRecurrentConnection(FullConnection(n['hidden1'],n['hidden1'], name='r1'))

#print "Network Defined"
n.sortModules()
#print "Sorting Modules"

trainer = BackpropTrainer(n, dataset, verbose=True)# verbose=True,learningrate=0.1, maxEpochs=100)

#print "Neural net generates {}".format(n.activate([0,1,2,3,4]))
trainer.trainEpochs(epochs=10)
#print "Neural net generates {}".format(n.activate(data[1,:] ))
#alcoholMax = alcoholPoints.max(axis=0)
#alcoholMin = alcoholPoints.min(axis=0)
##alcoholPoints = (alcoholPoints-alcoholMin)/(alcoholMax-alcoholMin)

output = scipy.empty(len(alcoholPoints))
for i in range(len(alcoholPoints)):
    output[i] = n.activate(data[i,:] )
    print "Net value is {}, Actual Value is {}".format(output[i],alcoholPoints[i])
#print "Difference of net and alcohol {}".format(output-alcoholPoints)
#print n
#print "Removed n = {} total points".format(removedPoints)
#print "Neural net generates {}".format(n.activate(data[120,:] ))
#print "Actual Value is {}".format(alcoholPoints[120])
#print "alcohol points"
#print output
#print "T Points"
#print tPoints


plt.plot(tPoints,alcoholPoints, 'b-', tPoints, output, 'g-', tPoints, noisyBooze, 'r-')
plt.xlim(0,100)
plt.ylim(0,200)
plt.xlabel('Time (h)')
plt.title('Ethanol Concentration (%v/v)')
plt.grid(True)

plt.show()