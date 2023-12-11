"""
Example usage of the `tenacity` python module -- a nice library that facilitates retrying code with decoration!

get it via- `pip install tenacity`
docs- https://tenacity.readthedocs.io/en/latest/
* they have some nice support for chaining together retry modifiers
  * things like wait 10 seconds per retry and only retry 4 times...

"""

import random
import time
from tenacity import retry


# this function is likely to break --> tenacity provides nice api for accepting that this function will occasionally break and handling that 
def rather_unpredictable_function():
    if random.randint(0, 3) > 1:
        raise Exception("val was greater than 1! how could you?")
    else: 
        return "amazing"

@retry #this method retries indefinitely --> might lead to odd behaviors 
def unpredictable_function_with_tenacity():
    if random.randint(0, 10) > 1:
        raise Exception("val was greater than 1! how could you?")
    else: 
        return "amazing"

# here we sleep if there happens to be an exception raised
@retry(wait=time.sleep(10))
def unpredictable_with_backoff():
    if random.randint(0, 10) > 1:
        raise Exception("val was greater than 1! how could you?")
    else: 
        return "amazing"


for i in range(2):
    # result = rather_unpredictable_function() #this oughta break alot!
    # result = unpredictable_function_with_tenacity()
    result = unpredictable_with_backoff()

    print(result)


