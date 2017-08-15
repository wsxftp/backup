import stat
import pathlib

a = pathlib.Path('D:\logs').iterdir()
for x in a:
    t = x.stat()
    mode = stat.filemode(t.st_mode)
    a = stat
    print(mode)

help(stat)