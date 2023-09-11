# Example of using tqdm with a dynamic description -- useful for updating the desc with each iter of a loop
# https://stackoverflow.com/questions/60336079/changing-description-after-a-for-cycle-in-tqdm
from tqdm import tqdm
import time

pbar = tqdm(range(100), desc='description')

x = 0
for i in pbar:
    x += i
    y = x**2
    pbar.set_description("y = %d" % y)
    time.sleep(0.5)

