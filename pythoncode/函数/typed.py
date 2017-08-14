import inspect
from functools import wraps


def typed(fn):
    @wraps(fn)
    def wrap(*args, **kwarges):
        for i, param in enumerate(inspect.signature(fn).parameters.values()):
            if param.annotation:
                if param.name in kwarges.keys():
                    if not isinstance(kwarges[param.name], param.annotation):
                        raise TypeError(param.name)
                else:
                    if not isinstance(args[i], param.annotation):
                        raise TypeError(param.name)
        return fn(*args, **kwarges)

    return wrap


@typed
def add(x: int, y: int) -> int:
    return x + y


a = add(1, 2)
