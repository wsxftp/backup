# coding: utf-8
import sys
print('the command line arguments are:')
_, x, y, *z = sys.argv
print(x)
print(y)
print(z)
