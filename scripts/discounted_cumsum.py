# A "Black Magic" Discounted Cumulative Sum Calculation from the folks at rllab
# By way of SpinningUp- https://github.com/openai/spinningup/blob/038665d62d569055401d91856abb287263096178/spinup/algos/pytorch/vpg/core.py#L29:L44 

import torch
import numpy as np


def discount_cumsum(x, discount):
    """
    magic from rllab for computing discounted cumulative sums of vectors.

    input:
        vector x,
        [x0,
         x1,
         x2]

    output:
        [x0 + discount * x1 + discount^2 * x2,
         x1 + discount * x2,
         x2]
    """
    import scipy.signal
    #print(x)
    #print(discount)
    return scipy.signal.lfilter([1], [1, float(-discount)], x[::-1], axis=0)[::-1]


t = torch.tensor([1, 2, 3, 4, 5, 6, 7]) #torch tensors don't play nice, numpy implements a diff method under the hood that does
t = np.array([1, 2, 3, 4, 5, 6, 7])
d = 0.96

ans = discount_cumsum(t, d)
print(ans) #works like a freaking charm

