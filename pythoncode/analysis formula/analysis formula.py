# -*- coding: utf-8 -*-
import timeit

print([x**2 for x in range(10)])

# timeit.timeit被测量时间的语句要求在''内部
print(timeit.timeit('y=[x**2 for x in range(0, 10) if x % 2 == 0]'))


def addd():
    pass


def fun():
    pass
