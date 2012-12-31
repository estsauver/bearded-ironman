__author__ = 'estsauver'

from pybrain import RecurrentNetwork, LinearLayer, SigmoidLayer, FullConnection

# Here we define the labels for our inputs. The length of these is used
# to calculate the size of the layers, so changing the number of these does impact the
# actual code
netInput = ["X", "V","T","time"]
netOutput = ["mAB", "XAlcohol"]

# This species the structure of the hidden layers. Currently, we default to one
# full connection between each layer to the next layer.
hiddenLayerSizes = [3,4]

#This initializes the network. Recurrent Networks should only be used if we're
# going to have a feedback loop at some point because they take more memory.
net = RecurrentNetwork()

#Defines initial input layer. It has as many inputs as there are measured netInputs.
inputLayer = LinearLayer(len(netInput), name="Input Layer")
#Adds input layer to the network.
net.addInputModule(inputLayer)

# hiddenLayers is a list that holds all of the layers that are created in order.
hiddenLayers=[]

#   Add a hidden layer for each hidden layer defined and give it a name.
for i in range(len(hiddenLayerSizes)):
    hiddenLayers.append(SigmoidLayer(hiddenLayerSizes[i],name="HL Number {}".format(i+1)))
    net.addModule(hiddenLayers[i])
#    Adds connections, either for the input to the first hidden or from hidden layer to hidden layer
    if i == 0:
        input_to_first_hidden = FullConnection(inputLayer,hiddenLayers[i])
        net.addConnection(input_to_first_hidden)
    else:
        hidden_to_hidden = FullConnection(hiddenLayers[i-1],hiddenLayers[i])
        net.addConnection(hidden_to_hidden)

net.addRecurrentConnection(FullConnection(net["HL Number 1"],net["HL Number 1"], name="Recurrent Connection"))

outputLayer = LinearLayer(len(netOutput), name="Output Layer")
net.addOutputModule(outputLayer)
hidden_to_output=FullConnection(hiddenLayers[-1],outputLayer)
net.addConnection(hidden_to_output)
net.sortModules()

print net.activate([1,1,1,1])
print net.activate([1,1,1,1])
print net.activate([1,1,1,1])
print net.activate([1,1,1,1])


