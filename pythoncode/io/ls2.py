import stat
import argparse
import pathlib

parser = argparse.ArgumentParser(prog='ls', description='use python make ls')
parser.add_argument('-l', dest='long_format', help='-l 以长格式显示文件信息', action='store_true')
parser.add_argument('path', nargs='*', default='.')
args = parser.parse_args()


def scan(path):
    yield from (x for x in pathlib.Path(path).iterdir())


def format(iterm: pathlib.Path) -> str:
    if not args.long_format:
        return iterm
    else:
        ret = {
            "mode": stat.filemode(iterm.stat().st_mode),
            "size": iterm.stat().st_size,
            "name": iterm
        }
    return '{mode} {size} {name}'.format(**ret)


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
