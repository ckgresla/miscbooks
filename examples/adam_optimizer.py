#!/usr/bin/env python3
# Toy example of the Adam Optimizer in raw Numpy
# run cmds:
#   view the objective function: './adam_optimizer.py  --vizobj'
#   : '' 
"""
# References
- Adamm: A Method for Stochastic Optimization- https://arxiv.org/abs/1412.6980
- AV Tutorial- https://www.analyticsvidhya.com/blog/2023/09/what-is-adam-optimizer/

# Notes 
Adam is an momentum based improvement over SGD for optimization. Heavily used in deep learning -- the de facto standard for any and all architectures.
* the bias correction mechanism counters initializations biases in the early stages of training --> leading to faster convergence
* the algorithm tracks the first & second moments for each parameter it is optimizing, allow to be: (m1, m2)
* at initialization of the optimizer's state, m1 & m2 are set to zero
  * we update these moving averages of m1, m2 to make updates to the model --> these values are updated with an exponentially decaying average involving the same m1 or m2 value and the current gradient for that parameter being optimized
* a small epsilion value is typically added to the second moment for numeric stability, in the: m1/(m2 + eps) step


At any step `t` in the iteration for updating a parameter with its gradient, the Adam optimization algorithm updates two moment estimates, `m1` and `m2`, as follows:

1. **m1 (Running Average of Gradients):**
    - `m1_t = β1 * m1_(t-1) + (1 - β1) * g_t`
    - Where:
        - `m1_t` is the running average of gradients at step `t`.  - `β1` is the decay rate for `m1`. It controls the exponential decay rate for the moving average of the first moment (typically set to 0.9).
        - `g_t` is the gradient of the parameter at step `t`.
        - `m1_(t-1)` is the running average of gradients at step `t-1`.
   
2. **m2 (Uncentered Variance of Gradients):**
    - `m2_t = β2 * m2_(t-1) + (1 - β2) * g_t^2`
    - Where:
        - `m2_t` is the uncentered variance of gradients at step `t`.
        - `β2` is the decay rate for `m2`. It controls the exponential decay rate for the moving average of the second moment (typically set to 0.999).
        - `g_t^2` is the square of the gradient of the parameter at step `t`.
        - `m2_(t-1)` is the uncentered variance of gradients at step `t-1`.

Note: Both `m1` and `m2` are initialized as 0 at the beginning of the optimization.

After updating `m1` and `m2`, the algorithm proceeds to compute bias-corrected versions of the moment estimates to counteract their initialization at 0.

-  Bias-corrected `m1`: 
    - `m1_t_corrected = m1_t / (1 - β1^t)`
-  Bias-corrected `m2`: 
    - `m2_t_corrected = m2_t / (1 - β2^t)`

Finally, the parameter update uses the corrected `m1` and `m2` to adjust the parameter:
-  `parameter_t = parameter_(t-1) - learning_rate * m1_t_corrected / (sqrt(m2_t_corrected) + epsilon)`

Where:
-  `learning_rate` is a hyperparameter specifying the step size at each iteration.
-  `epsilon` is a small number to prevent division by zero (typically on the order of 1e-8).

"""

import argparse
import numpy as np
from numpy import arange
from numpy import meshgrid
from matplotlib import pyplot as plt


## funcs et al
def objective(x, y):
    return x**2.0 + y**2.0

def visualize_objective_space():
    # define range for input
    range_min, range_max = -1.0, 1.0

    # sample input range uniformly at 0.1 increments
    xaxis = arange(range_min, range_max, 0.1)
    yaxis = arange(range_min, range_max, 0.1)

    # create a mesh from the axis
    x, y = meshgrid(xaxis, yaxis)

    results = objective(x, y)

    figure = plt.figure()
    axis = figure.add_subplot(111, projection='3d')  
    axis.plot_surface(x, y, results, cmap='jet')

    # show the plot
    plt.show()

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def d_sigmoid(x):
    return x*(1-x)


class AdamOptimizer:
    def __init__(self, learning_rate=0.0001, beta1=0.9, beta2=0.999, epsilon=1e-7):
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon 
        self.m = 0  # moment 1
        self.v = 0  # moment 2  
        self.t = 0 

    def update(self, weights, grad):
        self.t += 1 # increment timestep
        self.m = self.beta1 + self.m + (1 - self.beta1) * grad
        self.v = self.beta2 + self.v + (1 - self.beta2) * np.square(grad)
        m_hat = self.m / (1 - self.beta1 ** self.t)
        v_hat = self.v / (1 - self.beta2 ** self.t)
        weights -= self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)
        return weights

def run_adam_optimization(n_data=1000):
    np.random.seed(42)

    # random data
    X = np.random.randn(n_data, 2)
    y = np.array([[1] if x[0] + x[1] > 0 else [0] for x in X])

    # Neural network parameters
    input_size = 2
    hidden_size = 4
    output_size = 1

    # Initialize weights
    hidden_weights = np.random.uniform(size=(input_size, hidden_size))
    output_weights = np.random.uniform(size=(hidden_size, output_size))
    hidden_bias = np.random.uniform(size=(1, hidden_size))
    output_bias = np.random.uniform(size=(1, output_size))

    # Adam optimizers for weights and biases
    adam_hidden_weights = AdamOptimizer()
    adam_output_weights = AdamOptimizer()
    adam_hidden_bias = AdamOptimizer()
    adam_output_bias = AdamOptimizer()

    # Training loop
    epochs = 1000

    for epoch in range(epochs):
        # Forward pass
        hidden_layer_input = np.dot(X, hidden_weights) + hidden_bias
        hidden_layer_output = sigmoid(hidden_layer_input)
        
        output_layer_input = np.dot(hidden_layer_output, output_weights) + output_bias
        predicted_output = sigmoid(output_layer_input)
        
        # Backpropagation
        error = y - predicted_output
        d_predicted_output = error * d_sigmoid(predicted_output)
        
        error_hidden_layer = d_predicted_output.dot(output_weights.T)
        d_hidden_layer = error_hidden_layer * d_sigmoid(hidden_layer_output)
        
        # Updating weights and biases with Adam optimizer
        output_weights = adam_output_weights.update(output_weights, hidden_layer_output.T.dot(d_predicted_output))
        hidden_weights = adam_hidden_weights.update(hidden_weights, X.T.dot(d_hidden_layer))
        
        output_bias = adam_output_bias.update(output_bias, np.sum(d_predicted_output, axis=0, keepdims=True))
        hidden_bias = adam_hidden_bias.update(hidden_bias, np.sum(d_hidden_layer, axis=0, keepdims=True))

        if epoch % 100 == 0:
            loss = np.mean(np.square(y - predicted_output))
            print(f'Epoch {epoch}, Loss {loss}')




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # visualize_objective_space()
    run_adam_optimization(10)

