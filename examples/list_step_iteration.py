# Magic to iterate over a list of items and produce lists of equal lengths (of some step size) with a final one in case there is a uneven number of steps
# Taken from- https://stackoverflow.com/questions/8991506/iterate-an-iterator-by-chunks-of-n-in-python

my_list = ["t", "1", "tat", 'asdfadf', 'asdfasdfasdsafdsf', "testing", "lets hope"]
chunk_size = 2
out = list((my_list[i:i + chunk_size] for i in range(0, len(my_list), chunk_size)))
print(out)

