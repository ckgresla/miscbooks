#!/usr/bin/env python
# I would like to branch out from the i in range(len()) and indexing habit


words = ["hello", "my", "fellow", "FOSS", "enthusiast"]

# Iterating over a List, returning index and item at each iter
for i, w in enumerate(words):
    print(i, w)


# Call function and get back a list of tuples like [(idx, item), ...]
enum_words = list(enumerate(words)) #returns an 'enumerator' object, nest in list to evalutate the function
print(enum_words)

