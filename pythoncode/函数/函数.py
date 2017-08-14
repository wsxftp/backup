# coding: utf-8
import datetime
import functools
import time


def logger(s):
    def _logger(fn):
        @functools.wraps(fn)
        def wrap(*args, **kwargs):
            start = datetime.datetime.now()
            ret = fn(*args, **kwargs)
            end = datetime.datetime.now()
            if (end - start).total_seconds() > s:  # 当s值为2时，输出执行时间
                print('call {} took {}'.format(fn.__name__, end - start))
            return ret

        return wrap

    return _logger


# 设置s的值为2
@logger(2)
def sleep(x):
    time.sleep(x)


sleep(3)
