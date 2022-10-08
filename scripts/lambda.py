# Getting Functional in Python
# Ref- https://realpython.com/python-lambda/


# Lambda & Python Equivalents

# Identity Function 
def identity(v):
    return v 
a = identity(1)

a = lambda x: x
  #lambda functions effectively map the "function" that we want to apply at "x" (like calculus, more about the func than the changing of the actual val)

# Squaring a Number (2)
a = 2
a = a**2 #now 4

a = (lambda x: x**2)(2) #returns 4

# Even or Odd
def e_or_o(num):
    if num%2 == 0:
        return "even"
    else:
        return "odd"

a = (lambda x: x%2 and "odd" or "even")(5)



# Conventions --> things to do with Lambda Functions
square_val = lambda x: x**2 #creating a named function (kinda clean syntax for shorter stuff)
square_val(3) #calling the func


# Multi-Argument Lambdas 
person_does = lambda name, job: f"{name.title()} is a {job}" #take multi-arguments via comma separated args (not like a list)
#a = person_does("kevin", "wizard") #call like a regular func


# Immediately Invoked Function Expression (IFFE, pronounced iffy)
(lambda x, y, z: x + y * z)(1, 12, 3) #returns 39, gets evaluated immediately
  #cool kids apparently don't like this since it is 'anonymous' (not explicitly creating a function and then evaluating it on vars)


# Passing in Arguments to Lambdas (many ways of doing this)
a = (lambda x, y, z: x + y + z)(1, 4, 4)

a = (lambda x, u=5: x**u)(2) #can set "constant" vars for the func, could overwrite though


# Usage with map() function
a = list(map(lambda x: x**2, range(12)))
  #maps the squaring operation for all elements in range(12) & returns a list of the squared values


# Usage with filter() function
a = list(filter(lambda val: "i" in val, ["wiz", "bang"])) #filters the list (2nd arg) by the string bool in the lambda


# Get Proportions of List (pos, neg & zeros) w a Cool Lambda
def desc_list(lst):
    pos = sum(map(lambda x: x<0, lst))/len(lst)
    neg = sum(map(lambda x: x>0, lst))/len(lst)
    zed = sum(map(lambda x: x==0, lst))/len(lst)
    return [pos, neg, zed] #proportions of list

a = desc_list([1, 2, -1, -23, 1, 2, 3, 0])


print(a)

