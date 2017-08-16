import stat
import pathlib
import datetime

a = pathlib.Path('D:\logs').iterdir()
for x in a:
    t = x.stat()
    mode = stat.filemode(t.st_mode)
    a = stat
    print(t)


dt = datetime.datetime.fromtimestamp(t.st_mtime)
print('{:>2} {:>2} {:>2}:{:>2}'.format(dt.month, dt.day, dt.hour, dt.minute))

ret = {
    "mode": 1,
    "name": "bbb"
}

ret["mode"] = str(ret["mode"])

print('{mode} {name}'.format(**ret))
