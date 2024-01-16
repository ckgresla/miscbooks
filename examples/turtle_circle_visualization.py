# a toy example from one of the cooler modules in the python stdlib 
# one might need to do some installing on macos- `brew install python-tk`
# Docs- https://docs.python.org/3/library/turtle.html

from turtle import *

for steps in range(100):
    for c in ('blue', 'red', 'green'):
        color(c)
        forward(steps)
        right(30)

