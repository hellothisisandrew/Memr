import numpy as np

# WARNING THESE FUNCTIONS ONLY WORK IF STEPS < 1

# only use multiples of ten here
steps = 0.001 # each step reprsents .0001 seconds
start = 0.0     # start
stop = 1.0      # Stop
totalParts = int(stop/steps)   # total number of steps


# this gets the index from a given time say eg .03s
def getIndexFromT(t):
    return int(t /steps)

# get time from index
def getTimeFromIndex(index):
    return index * steps
