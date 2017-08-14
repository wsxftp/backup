import random
import time
import datetime


def data_source():
    while True:
        yield random.randint(0, 100)
        time.sleep(0.1)


def top_k(k, time=1):
    lst = []
    ds = data_source()
    start_time = datetime.datetime.now()
    while True:
        e = next(ds)
        for i, v in enumerate(lst):
            if e > v:
                lst.insert(i, e)
                break
        else:
            lst.append(e)
        stop_time = datetime.datetime.now()
        if (stop_time - start_time).total_seconds() >= (time - 0.1):
            yield lst[0:k]


g = top_k(k=3)
print(next(g))
