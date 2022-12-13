# Sample Usage of Args and Kwargs in Python
# Reference- https://www.geeksforgeeks.org/args-kwargs-python/




# Args 
def misc_print(*args):
    for arg in args:
        print("on Arg:", arg)
        print(arg**2)

def multi_square(a1, *args):
    print(f"a1 = {a1}: ", a1**2)
    for arg in args:
        print(f"{arg}: {arg**2}")


# Kwargs
def kwarg_mapper(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}, {value}")


if __name__ == "__main__":
    misc_print(2, 3, 4, 5)
    multi_square(2, 4, 5, 2)

    print("\n\n")

    kwarg_mapper(first=1, second=2, third=3)
