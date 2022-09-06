"""
Efficient-ish implementation of the Fibonacci Sequence in Python, as explained in the dynamic programming Wiki Page-https://en.wikipedia.org/wiki/Dynamic_programming

"""

# Fibonacci w 'Memoization' -- Top Down Approach
def fib(n):

	if n <= 1: return n #nothing to calc
	else:
		# The Interesting Implementation (use a map to store sub-calculations of Sequence)
		if n in calc_dict:
			return calc_dict[n]
		else:	
			calculation = fib(n-1) + fib(n-2)
			calc_dict[n] = calculation #reassign to dict
			#print(calculation) #view the output 

			return calc_dict[n]


# Func call
calc_dict = {} #for interesting storing of values

# Fibonacci Call for Single Val
#n = int(input("Please Input 'n' for Fibonacci Sequence Calculation: "))
#fib(n)

# Call for List of Vals
print([fib(n) for n in range(0, 1000)])
