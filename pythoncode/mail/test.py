import time

t = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
t1 = 'ServerError at {}'.format(t)
print(type(t))
print(t1)