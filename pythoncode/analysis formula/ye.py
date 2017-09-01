import re


def open_log(path):
    with open(path) as f:
        yield from f


def analyzer(path):
    ip_list = []
    o = re.compile(r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<other>.*)')
    for line in open_log(path):
        d = o.search(line).groupdict()
        if d['ip'] not in ip_list:
            ip_list.append(d['ip'])
            yield d['ip']


if __name__ == '__main__':
    for i in analyzer('access.log'):
        print(i)
