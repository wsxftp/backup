# ecncoding: utf8
# test
import stat
import argparse
import pathlib
import pwd
import grp
import datetime

parser = argparse.ArgumentParser(prog='ls', description='use python make ls')
parser.add_argument('-l', dest='long_format', help='-l 以长格式显示文件信息', action='store_true')
parser.add_argument('-h', dest='human_read', help='-h 以易读的格式返回文件大小信息', action='store_true')
parser.add_argument('path', nargs='*', default='.')
args = parser.parse_args()


def scan(path):
    yield from (x for x in pathlib.Path(path).iterdir())


def time_format(mtime):
    dt = datetime.datetime.fromtimestamp(mtime)
    return '{:>2} {:>2} {:>2}:{:>2}'.format(dt.month, dt.day, dt.hour, dt.minute)


def human_format(mtime):
    


def format(iterm: pathlib.Path) -> str:
    st = iterm.stat()
    if not args.long_format:
        return iterm
    else:
        ret = {
            "mode": stat.filemode(st.st_mode),
            "nlink": st.st_link,
            "user": pwd.getpwuid(st.st_uid).pw_name,
            'group': grp.getgrgid(st.st_gid).gr_name,
            "size": st.st_size,
            "mtime": time_format(st.st_mtime),
            "name": iterm
        }
        if not args.human_read:
            ret["size"] = 
        return '{mode} {nlink} {user} {group} {size:>8} {mtime} {name}'.format(**ret)


def main():
    if isinstance(args.path, list):
        for path in args.path:
            print('{}:'.format(path))
            for item in scan(path):
                print(format(item))
            print()
    else:
        for item in scan(args.path):
            print(format(item))


if __name__ == '__main__':
    main()
