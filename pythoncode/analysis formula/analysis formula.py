#!/usr/sbin/python3
# coding: utf8
import sys
import re
import datetime
import argparse

parser = argparse.ArgumentParser(prog='analysis http log')
parser.add_argument('path', nargs='*', default=['./access.log'])
parser.add_argument(
    '-flow', dest='flow', action='store_true', help='-flow 计算http服务器今天流量总和')
parser.add_argument(
    '-error', dest='error', action='store_true', help='-error 响应码大于300请求的总数量')
parser.add_argument(
    '-bugstatus',
    dest='bugstatus',
    action='store_true',
    help='-bugstatus 无法理解的状态码')
args = parser.parse_args()


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
            yield {
                'ip': '-',
                'time': '-',
                'method': '-',
                'url': '-',
                'version': '-',
                'status': '404',
                'length': '0',
                'referer': '-',
                'ua': '-'
            }
        else:
            d = m.groupdict()
            # print(i, d)
            i += 1
            # d['time'] = datetime.datetime.strptime(d['time'],
            #                                        '%d/%b/%Y:%H:%M:%S %z')
            yield d


def format_flow(data):
    units = (' ', 'K', 'M', 'G', 'T', 'P')
    i = 0
    while data >= 1024:
        data //= 1024
        i += 1
    return '{}{}'.format(data, units[i])


def count_data(data, ret):
    ret['flow'] += int(data['length'])
    if int(data['status']) >= 200:
        ret['200'] += 1
        if int(data['status']) >= 300:
            ret['300'] += 1
            if int(data['status']) >= 400:
                ret['400'] += 1
                if int(data['status']) < 600:
                    ret['500'] += 1
                else:
                    ret['bugstatus'] += 1
    else:
        ret['bugstatus'] += 1
    return ret


def analyzer(path):
    # print(path)
    ret = {
        'flow': 0,
        '200': 0,
        '300': 0,
        '400': 0,
        '500': 0,
        'error': 0,
        'bugstatus': 0
    }
    for data in format_log(open_log(path)):
        ret = count_data(data, ret)
    ret['error'] = ret['300'] + ret['400'] + ret['500']
    # ret['flow'] = format_flow(ret['flow'])
    return ret


def line_print():
    pass


def main():
    # for line in format_log(open_log(sys.argv[1])):
    # print(line)
    result = analyzer(args.path[0])
    if args.flow:
        print(result['flow'])
    if args.error:
        print(result['error'])
    if args.bugstatus:
        print(result['bugstatus'])


if __name__ == '__main__':
    main()
