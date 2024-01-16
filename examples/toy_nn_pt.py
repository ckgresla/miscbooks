#!/usr/bin/env python3 
# a toy neural network with pytorch 

import torch
from torch import nn
from torch.optim import SGD
import random
from typing import Callable


# Data, Devices & Hyperparameters
n_samples_per_dist = 10000
n_test_size = round(n_samples_per_dist * 0.1)

data_distribution_1 = torch.randint(0, 5, (n_samples_per_dist, 2)) * torch.rand(n_samples_per_dist, 2), torch.zeros(n_samples_per_dist)
data_distribution_2 = torch.randint(4, 9, (n_samples_per_dist, 2)) * torch.rand(n_samples_per_dist, 2),  torch.ones(n_samples_per_dist)

samples = torch.cat((data_distribution_1[0], data_distribution_2[0]), dim=0)
labels  = torch.cat((data_distribution_1[1], data_distribution_2[1]), dim=0)
# [200, 2] and [200] --> dataset dims (sample shapes x labels), based entirely on 'n_samples_per_dist'

# random sample of the data for train/test
test_idxs = random.choices(range(len(samples)), k=n_test_size)
train_idxs = [i for i in range(len(samples)) if i not in test_idxs]
train_idxs, test_idxs = torch.Tensor(train_idxs).to(dtype=torch.int32), torch.Tensor(test_idxs).to(dtype=torch.int32)
train = {
    "x": samples.index_select(0, train_idxs),
    "y":  labels.index_select(0, train_idxs)
}
test = {
    "x": samples.index_select(0, test_idxs),
    "y":  labels.index_select(0, test_idxs)
}

device = ("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

learning_rate = 3e-4
batch_size    = 16
epochs        = 1000




# nice lil network class
class BasicNetwork(nn.Module):
    def __init__(self, input: int, output: int, hidden: int, n_layers: int, activation: Callable):
        super().__init__()

        # assemble the network as a sequence of layers
        self.layers = [
            nn.Linear(input, hidden), 
            activation(),
        ]
        for i in range(n_layers-1):
            self.layers.append(nn.Linear(hidden, hidden))
            self.layers.append(activation())


        self.layers.append(nn.Linear(hidden, output))
        self.layers = nn.Sequential(*self.layers)

    def forward(self, x): 
        if type(x) != torch.Tensor:
            x = torch.Tensor(x)
        logits = self.layers(x)
        return logits





# Business Time!
net = BasicNetwork(2, 1, 10, 0, nn.ReLU)
loss_fn = nn.MSELoss()
# loss_fn = nn.L1Loss()
optimizer = SGD(net.parameters(), lr=learning_rate)

for _ in range(epochs):
    net.train()
    for i, s in enumerate(train["x"]):
        pred = net.forward(s)
        label = train["y"][i]
        loss = loss_fn(pred, label) 
    loss.backward()
    optimizer.step()

    eval_loss = 0
    for i, s in enumerate(test["x"]):
        pred = net.forward(s)
        eval_loss += loss_fn(pred, test["y"][i])

    # printables
    print(f"epoch: {_}")
    print(f"training loss: {loss}")
    print(f"    eval loss: {eval_loss}")


