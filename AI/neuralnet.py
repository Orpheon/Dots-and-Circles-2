from __future__ import division

import math, random

class Neuron(object):
    def __init__(self, neuralnet, activated=1):
        self.inputbuffer = 0
        self.ownernetwork = neuralnet
        self.connections = {}
        self.activated = activated

    def run(self):
        output = self.activation_function(self.inputbuffer)

        if self.activated:
            for index, weight in self.connections.items():
                self.ownernetwork.neuronlist[index].inputbuffer += output*weight
            self.inputbuffer = 0

    def activation_function(self, x):
        x = 1/(1+(math.e**(-x)))# Sigmoidal function, x is now between 0 and 1. http://www.ai-junkie.com/ann/evolved/images/sigmoid.jpg
        x = (2*x)-1# We want it between -1 and 1
        return x

    def destroy(self):
        self.neuralnet = None


class NeuralNetwork(object):
    NUM_LAYERS_IN_PART1 = 2
    NUM_LAYERS_IN_PART2 = 4
    PART2_LAYER_WIDTH = 100
    INPUT_SIZE = 160 # DEPENDENT ON EYE.FOV! Change both if you change one! Also, this is "per eye".
    OUTPUT_SIZE = 2

    def __init__(self, weights=[]):

        if weights == []:
            weights = self.get_random_weights()

        self.neuronlist = []
        # Create and connect the nodes from end to start

        # Create the last output neurons
        for i in range(self.OUTPUT_SIZE):
            self.neuronlist.append(Neuron(self, activated=0))

        # Mark the output neurons
        self.outputneurons = self.neuronlist[:]

        # Create the last layer of normal neurons
        for i in range(self.PART2_LAYER_WIDTH):
            neuron = Neuron(self)
            self.neuronlist.append(neuron)
            for j in range(self.OUTPUT_SIZE): # And connect them
                neuron.connections[j] = weights.pop()

        # Create the rest of the part2 layers
        for i in range(self.NUM_LAYERS_IN_PART2-1):
            for j in range(self.PART2_LAYER_WIDTH):
                neuron = Neuron(self)
                self.neuronlist.append(neuron)
                for k in range(self.PART2_LAYER_WIDTH):
                    pos =  k + i*self.PART2_LAYER_WIDTH + self.OUTPUT_SIZE # The position in the network list of the neurons of the next layer
                    neuron.connections[pos] = weights.pop()

        # Create the last layer of the left eye part
        for i in range(self.INPUT_SIZE):
            neuron = Neuron(self)
            self.neuronlist.append(neuron)
            for j in range(self.PART2_LAYER_WIDTH):
                pos = j + (self.NUM_LAYERS_IN_PART2)*self.PART2_LAYER_WIDTH + self.OUTPUT_SIZE
                neuron.connections[pos] = weights.pop()

        # Create the rest of the left eye processing
        for i in range(self.NUM_LAYERS_IN_PART1-1):
            for j in range(self.INPUT_SIZE):
                neuron = Neuron(self)
                self.neuronlist.append(neuron)
                for k in range(self.INPUT_SIZE):
                    pos = k + i*self.INPUT_SIZE + (self.NUM_LAYERS_IN_PART2)*self.PART2_LAYER_WIDTH + self.OUTPUT_SIZE
                    neuron.connections[pos] = weights.pop()

        # Mark the input neurons
        self.inputneurons = self.neuronlist[:self.INPUT_SIZE-1]

        # Create the last layer of the right eye part
        for i in range(self.INPUT_SIZE):
            neuron = Neuron(self)
            self.neuronlist.append(neuron)
            for j in range(self.PART2_LAYER_WIDTH):
                pos = j + self.INPUT_SIZE*self.NUM_LAYERS_IN_PART1 + self.NUM_LAYERS_IN_PART2*self.PART2_LAYER_WIDTH + self.OUTPUT_SIZE
                neuron.connections[pos] = weights.pop()

        # Create the rest of the right eye processing
        for i in range(self.NUM_LAYERS_IN_PART1-1):
            for j in range(self.INPUT_SIZE):
                neuron = Neuron(self)
                self.neuronlist.append(neuron)
                for k in range(self.INPUT_SIZE):
                    pos = k + i*self.INPUT_SIZE + self.INPUT_SIZE*self.NUM_LAYERS_IN_PART1 + self.NUM_LAYERS_IN_PART2*self.PART2_LAYER_WIDTH + self.OUTPUT_SIZE
                    neuron.connections[pos] = weights.pop()

        # Add these neurons to the input
        self.inputneurons += self.neuronlist[:self.INPUT_SIZE-1]

        # Flip the whole list, so the signal goes in the correct direction
        self.neuronlist.reverse()


    def run(self, input):
        # Set the input values
        for neuron in self.inputneurons:
            try:
                self.inputbuffer = input[self.inputneurons.index(neuron)]
            except KeyError:
                print("Wrong number of inputs given")

        # Propagate it through the network
        for neuron in self.neuronlist:
            neuron.run()

        # Output is now stored in the neurons of the self.outputneurons
        output = [neuron.inputbuffer for neuron in self.outputneurons]
        return output


        def process(self, leftimage, rightimage):
            input = leftimage+rightimage
            output = self.run(input)
            if len(output) != 2:
                print("Wrong output length")
            return output[0]*10, output[1]*10


    def get_random_weights(self):
        size = 2*((self.INPUT_SIZE**2)*(self.NUM_LAYERS_IN_PART1-1) + self.INPUT_SIZE*self.PART2_LAYER_WIDTH) + (self.PART2_LAYER_WIDTH**2)*(self.NUM_LAYERS_IN_PART2-1) + self.OUTPUT_SIZE*self.PART2_LAYER_WIDTH
        weights = []
        for i in range(int(size)):
            weights.append((random.random()*2)-1)
        return weights
