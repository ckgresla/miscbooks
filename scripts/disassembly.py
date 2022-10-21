# Play with the `dis` Module (and see the low level happenings in python execution)
# Docs- https://docs.python.org/3/library/dis.html

import dis 


# Toy Func
def exponentiate(lst: [int or float], exp=2):
    return [i**exp for i in lst]

l = [1, 2, 121, 4, 7, 420]
res = exponentiate(l, 36) #all is normal...
print(res, "Now we inspect:")

dis.dis(exponentiate)

