import math
import pandas as pd
from random import seed, random




# Init a Network ()
def initialize_network(n_inputs, n_hidden, n_outputs):
    network = list() #list of lists (layers) with dictionaries containing the weights for each layer
    hidden_layers = [{"weights":[random() for i in range(n_inputs + 1)]} for i in range(n_hidden)]
    network.append(hidden_layers)
    output_layer = [{"weights":[random() for i in range(n_hidden + 1)]} for i in range(n_outputs)]
    network.append(output_layer)
    return network


# Calculate neuron Values for an Input (called activate but really the w*x+b, per neuron or calculation)
def neuron_calculate(weights, inputs):
    activation = weights[-1] 
    for i in range(len(weights)-1):
        activation += weights[i] * inputs[i] #calculate element-wise neuron values (wx + b?)
    return activation

# An "Actual" Activation function?
def sigmoid(activation):
    return 1.0/(1.0 + math.exp(-activation))

def sigmoid_derivative(output):
    return output * (1.0 - output) #derivative of Sigmoid Func (ez activation for BackProp example)

# Forward Propagation (to get output for input from network)
def forward_pass(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = neuron_calculate(neuron["weights"], inputs)
            neuron["output"] = sigmoid(activation)
            new_inputs.append(neuron["output"])
        inputs = new_inputs
    return inputs

# BackProp Step (backward_pass)
def backprop(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network)-1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(neuron['output'] - expected[j])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * sigmoid_derivative(neuron['output'])

# Update network weights with error
def update_weights(network, row, l_rate):
    # Iterate over layers in the network
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] -= l_rate * neuron['delta'] * inputs[j] #acutal updating of neuron weights
            neuron['weights'][-1] -= l_rate * neuron['delta']


# Train a network for a fixed number of epochs
def train_network(network, train, l_rate, n_epoch, n_outputs):
    for epoch in range(n_epoch):
        sum_error = 0
        for row in train:
            outputs = forward_pass(network, row)
            expected = [0 for i in range(n_outputs)]
            expected[row[-1]] = 1
            sum_error += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
            backprop(network, expected)
            update_weights(network, row, l_rate)
        print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))

# Inference on a Single Example 
def predict(network, row):
    output = forward_pass(network, row)
    return output.index(max(output)) #returns the argmax of the output vector (numeric-encoded label for class outputed)

if __name__ == "__main__":
    print("Main Script")

    seed(1) #set seed
    df = pd.read_csv("iris.csv")
    print(f"Shape: {df.shape}\nColumns: {df.columns.values}")

    # Convert Class Names into Numerical Values (not strings)
    class_names = list(df["target"].unique())
    remapped, count = {}, 0
    for i in class_names:
        remapped[i] = count
        count += 1

    df.replace({"target":remapped}, inplace=True)
    # print("class_names: {}".format(class_names))
    print(df["target"].value_counts()) #perfectly balanced, as all things should be

    # Slice df into x & y Sets (one-hot encoded target classes)
    x, y = df.loc[:, df.columns!="target"].values, pd.get_dummies(df["target"]).values

    # Init NN
    net = initialize_network(4, 1, 3)

    # Sample Forward Pass for 1st Example in Data (zero-th element in list of x-data and y-labels)
    output = forward_pass(net, x[0])
    for layer in net:
        print(layer)
    print(f"\nOutput: {output}\nActual: {y[0]}\n")
    backprop(net, y[0])

    for layer in net:
        print(layer)

    # print(df.dtypes)

