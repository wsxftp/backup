import sys
import re
import datetime


def open_log(path):
    with open(path) as f:
        yield from f


def format_log(path):
    o = re.compile(
        r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .* .* \[(?P<time>.*)\] "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w|/\.\d]*)" (?P<status>\d{3}) (?P<length>\d+) "(?P<referer>[^\s]*)" "(?P<ua>.*)"'
        # r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .* .* \[(?P<time>.*)\] "(?P<method>.*) (?P<url>.*) (?P<version>.*)" (?P<status>\d*) (?P<length>\d*) "(?P<referer>.*)" "(?P<ua>.*)"'
    )
    i = 1
    for line in path:
        m = o.search(line)
        # print(m)
        if not m:
            yield {'ip': '-', 'time': '-', 'method': '-', 'url': '-', 'version': '-', 'status': '404', 'length': '0', 'referer': '-', 'ua': '-'}
        else:
            d = m.groupdict()
            # print(i, d)
            i += 1
            d['time'] = datetime.datetime.strptime(
                d['time'], '%d/%b/%Y:%H:%M:%S %z'
            )
            yield d


def format_flow(data):
    units = (' ', 'K', 'M', 'G', 'T', 'P')
    i = 0
    while data >= 1024:
        data //= 1024
        i += 1
    return '{}{}'.format(data, units[i])


def analyzer(path):
    print(path)
    ret = {'flow': 0, 'error': 0}
    for data in format_log(open_log(path)):
        ret['flow'] += int(data['length'])
        if int(data['status']) >= 300:
            ret['error'] += 1
    ret['flow'] = format_flow(ret['flow'])
    return ret


def line_print():
    pass


def main():
    # for line in format_log(open_log(sys.argv[1])):
        # print(line)
    result = analyzer(sys.argv[1])
    print("today's flow:{}, today's error:{}".format(result['flow'], result[
        'error']))


if __name__ == '__main__':
    main()
