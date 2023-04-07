#!/usr/bin/env python3 
# ASYNCHRONISITY IN PYTHON, as per- https://realpython.com/async-io-python/


import asyncio

async def count():
    print(1)
    await asyncio.sleep(1) #YOU CAN WAIT 3 SECONDS IN 1 SECOND! 
    print(2)


async def main():
    await asyncio.gather(count(), count(), count())




# Methods for Using Async Funcs (valid programming paradigms)
async def f(x):
    y = await z(x)  # OK - `await` and `return` allowed in coroutines
    return y

async def g(x):
    yield x  # OK - this is an async generator




if __name__=="__main__":
    import time
    start_time = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start_time
    print(f"Executed the file in {elapsed:0.2f}s")



