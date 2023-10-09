# Use a pool of processes to do the work of some function, applied to an iterable -- i.e; distribute a map func over many workers/data

import math
import time
from multiprocessing import Pool
 

n_workers = 1

# define a cpu-intensive task
def task(arg):
    return sum([math.sqrt(i) for i in range(1, arg)])

# protect the entry point
if __name__ == '__main__':
    # report a message
    print(f'Starting task with {n_workers} workers...')
    st = time.monotonic()
    # create the process pool
    with Pool(n_workers) as pool:
        # perform calculations
        results = pool.map(task, range(1,50000))
    # report a message
    print(f'Done in {time.monotonic() - st:.2f}s')
