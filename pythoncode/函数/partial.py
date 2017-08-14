from functools import wraps


def add(x, y):
    return x + y


def partial(fn, *p_args, **p_kwarges):
    @wraps(fn)
    def wrap(*args, **kwarges):
        return fn(*args, *p_args, **kwarges, **p_kwarges)

    return wrap


inc = partial(add, y=1)
print(inc(6))
