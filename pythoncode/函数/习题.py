from functools import wraps


def typecheck(*type_args, **type_kwargs):
    def dec(fn):
        @wraps(fn)
        def wrap(*args, **kwargs):
            for i, t in enumerate(type_args):
                print(i)
                if not isinstance(args[i], t):
                    print('{} type not is {},plaes reinput'.format(args[i], t))
                    return None
            for i, t in type_kwargs.items():
                if not isinstance(kwargs[i], t):
                    print(
                        '{} type not is {},plaes reinput'.format(i, t))
                    return None
            return fn(*args, **kwargs)

        return wrap

    return dec


@typecheck(int, int)
def add(x, y):
    return x + y


add('1', '1')
