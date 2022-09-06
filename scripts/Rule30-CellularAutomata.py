"""
Adopted from this StackOverFlow post- https://stackoverflow.com/questions/59773795/generating-rows-of-a-rule-30-cellular-automaton

Quick viewing of one of the most prolific (and potentially Turing Complete) Cellular Automatons
"""

import matplotlib.pyplot as plt  
import numpy as np


# Functions
def initial_state(width):
	initial = np.zeros((1, width), dtype=int) #vector of length "width" for first step of CA
	if width % 2 == 0:
		initial = np.insert(initial, int(width/2), values=0, axis=1) #if issues with even vals, add additional
		initial[0, int(width/2)] = 1
		return initial 
	else:
		initial[0, int(width/2)] = 1
		return initial

# Apply Rule 30 & return next row in CA Sequence
def rule_30(array):
	r1 = np.pad(array, [(0,0), (1,1)], mode="constant")
	next_row = array.copy()

	# Apply Rule to Each Array
	for i in range(1, array.shape[0]+1):
		for j in range(1, array.shape[1]+1):
			if r1[i-1][j-1] == 1 ^ (r1[i-1][j] == 1 or r1[i-1][j+1] == 1):
				next_row[i-1, j-1] = 1
			else:
				next_row[i-1, j-1] = 0
		return np.array(next_row)

def apply_rule(n):
	rv = initial_state(n)
	while rv[-1][0]==0:
		rv = np.append(rv, rule_30(rv[-1].reshape(1, -1)), axis=0)
	return rv


print("starting vector: ", initial_state(12))



print("\n\nRunning Rule 30:\n")
applied_rule = apply_rule(50)
#print(apply_rule(12))

plt.imshow(applied_rule, cmap="hot")
plt.show(block=True)
