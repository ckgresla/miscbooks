#!/usr/bin/env python
# Using the 'trange' Func instead of regular 'range' in python, very nice
# as per- https://stackoverflow.com/questions/37506645/can-i-add-message-to-the-tqdm-progressbar

from tqdm import trange
from time import sleep


t = trange(100, desc='Bar desc', leave=True)

for i in t:
    t.set_description("Bar desc (file %i)" % i)
    t.refresh() # to show immediately the update
    sleep(0.01)
