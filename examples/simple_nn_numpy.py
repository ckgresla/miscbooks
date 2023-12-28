"""
A simple implementation of a neural network in numpy
* ala Dr. Jason Brownlee
* it works, kinda, would like a better refactor that is fully my own in the future

"""


import numpy as np
from typing import Any, List
from sklearn.datasets import make_circles
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# small float, avoid division be zero in softmax
epsilon = np.finfo(float).eps

## activation functions & derivatives (sigmod, relu, tanh) + dict to retrieve
def sigmoid(z: np.ndarray):
    return 1/(1+np.exp(-z.clip(-500, 500))) #clip the range of func, stability++
def d_sigmoid(z: np.ndarray):
    s = sigmoid(z)
    return 2 * s * (1-s)
        # TODO: determine if this 2* in the derivative is correct
        #       might not be correct, see answer here- https://math.stackexchange.com/questions/78575/derivative-of-sigmoid-function-sigma-x-frac11e-x

def relu(z: np.ndarray):
    return np.maximum(0, z)
def d_relu(z: np.ndarray):
    return (z > 0).astype(float)

def tanh(z: np.ndarray):
    return np.tanh(z)
def d_tanh(z: np.ndarray):
    s = tanh(z)
    return 1 - s**2

activation_funcs = {
    "relu": (relu, d_relu),
    "tanh": (tanh, d_tanh),
    "sigmoid": (sigmoid, d_sigmoid),
}


## loss functions & differentiations (BCE, MSE)
def binary_cross_entropy(y: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Binary cross entropy: 
        L = -y * log(yhat) - (1-y) * log(1-yhat)

    * both of the args ought to be [1, n] dimensional arrays! 
    * this function returns a SCALAR loss value, average loss across n instances
    * This function computes the Average BCE, over a batch of samples
    """
    loss = -(y.T @ np.log(y_pred.clip(epsilon)) + (1-y.T) @ np.log((1-y_pred).clip(epsilon))) / y.shape[1]
    return loss
def d_bce(y: np.ndarray, y_pred: np.ndarray): 
    """ dL/dypred """
    return -np.divide(y, y_pred.clip(epsilon)) + np.divide(1-y, (1-y_pred).clip(epsilon))

# TODO: implement the MSE w same shapes as BCE


loss_funcs = {
    "bce": (binary_cross_entropy, d_bce)
}


## datastructs 
class Layer:
    def __init__(self, input_sz: int, output_sz: int):
        self.w = np.random.uniform(low=-1, high=1, size=(input_sz, output_sz))
        self.b = np.random.uniform(low=-1, high=1, size=(1, output_sz))
        self.a = None

        self.dw = None
        self.db = None
        self.da = None

class mlp:
    '''Multilayer perceptron using numpy
    '''
    def __init__(self, layersizes, activations, derivatives, lossderiv):
        """remember config, then initialize array to hold NN parameters without init"""
        # hold NN config
        self.layersizes = layersizes
        self.activations = activations
        self.derivatives = derivatives
        self.lossderiv = lossderiv
        # parameters, each is a 2D numpy array
        L = len(self.layersizes)
        self.z = [None] * L
        self.W = [None] * L
        self.b = [None] * L
        self.a = [None] * L
        self.dz = [None] * L
        self.dW = [None] * L
        self.db = [None] * L
        self.da = [None] * L

    def initialize(self, seed=42):
        np.random.seed(seed)
        sigma = 0.1
        for l, (insize, outsize) in enumerate(zip(self.layersizes, self.layersizes[1:]), 1):
            self.W[l] = np.random.randn(insize, outsize) * sigma
            self.b[l] = np.random.randn(1, outsize) * sigma

    def forward(self, x):
        self.a[0] = x
        for l, func in enumerate(self.activations, 1):
            # z = W a + b, with `a` as output from previous layer
            # `W` is of size rxs and `a` the size sxn with n the number of data instances, `z` the size rxn
            # `b` is rx1 and broadcast to each column of `z`
            self.z[l] = (self.a[l-1] @ self.W[l]) + self.b[l]
            # a = g(z), with `a` as output of this layer, of size rxn
            self.a[l] = func(self.z[l])
        return self.a[-1]

    def __call__(self, x):
        return model.forward(x)

    def backward(self, y, yhat):
        # first `da`, at the output
        self.da[-1] = self.lossderiv(y, yhat)
        for l, func in reversed(list(enumerate(self.derivatives, 1))):
            # compute the differentials at this layer
            self.dz[l] = self.da[l] * func(self.z[l])
            self.dW[l] = self.a[l-1].T @ self.dz[l]
            self.db[l] = np.mean(self.dz[l], axis=0, keepdims=True)
            self.da[l-1] = self.dz[l] @ self.W[l].T
 
    def optimize_sgd(self, eta):
        for l in range(1, len(self.W)):
            self.W[l] -= eta * self.dW[l]
            self.b[l] -= eta * self.db[l]

## Train it up
# Make data: Two circles on x-y plane as a classification problem
x, y = make_circles(n_samples=1000, factor=.1, noise=0.1)
y = y.reshape(-1,1) # our model expects a 2D array of (n_sample, n_dim)

# model = Network(
#     layershapes=[3, 2, 4, 1],
#     activations=["relu", "relu", "sigmoid"],
# )
model = mlp(
    layersizes=[2, 12, 12, 12, 1],
    activations=[relu, relu, relu, sigmoid],
    derivatives=[d_relu, d_relu, d_relu, d_sigmoid],
    lossderiv=d_bce,
)
model.initialize()

y_pred = model(x)
loss = binary_cross_entropy(y, y_pred)
print("loss value @ time of model init: ", f"loss: {loss} accuracy: {accuracy_score(y, (y_pred  > 0.5))}")


# train for each epoch
n_epochs = 57
learning_rate = 0.005
for n in range(n_epochs):
    y_pred = model(x)
    model.backward(y, y_pred)
    model.optimize_sgd(learning_rate)
    loss = binary_cross_entropy(y, y_pred)
    print("Iteration {} - loss value {} accuracy {}".format(n, loss[0][0], accuracy_score(y, (y_pred > 0.5))))


# Visualize boundry of final trained model  --> thank you @ karpathy
h = 0.25
x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
Xmesh = np.c_[xx.ravel(), yy.ravel()]
inputs = [list(map(float, xrow)) for xrow in Xmesh]
scores = list(map(model, inputs))
Z = np.array([s > 0.5 for s in scores])
Z = Z.reshape(xx.shape)

fig = plt.figure()
plt.contourf(xx, yy, Z, cmap=plt.cm.viridis, alpha=0.8)
plt.scatter(x[:, 0], x[:, 1], c=y, s=40, cmap=plt.cm.viridis)
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.savefig('foo.png', bbox_inches='tight')

