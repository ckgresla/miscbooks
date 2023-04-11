
# From- https://stackoverflow.com/questions/9671224/split-a-python-list-into-other-sublists-i-e-smaller-lists
# Given a list and a num to split it into, split the list into lists of length N or remainder
 
 
# Input list initialization
data = [1, 10, 33, 22, 11, 23, 12, 3, 123, 3, 5, 6, 533, 2, 3, 4, 5, 6, 7]
 
chunks = [data[x:x+10] for x in range(0, len(data), 10)]
print(chunks)

