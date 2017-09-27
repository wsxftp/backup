#!/usr/bin/python3
# coding: gb2312
import re
import argparse
import datetime
import threading
import os
import pymysql
import urllib.request
import json

parser = argparse.ArgumentParser(
    prog='Access IP', description='每有ip访问服务器就会记录到日志中且不记录重复ip,每隔10分钟后记录一次重复ip')
parser.add_argument(
    '-time',
    dest='Wait_time',
    type=int,
    default=600,
    help='-time 设置隔多长时间记录一次重复ip')
parser.add_argument(
    '-file_path',
    dest='file_path',
    default='/usr/local/nginx/logs/access.log',
    # default='./access.log',
    help='-file_path http日志位置，默认处理/usr/local/nginx/logs/access.log')
parser.add_argument(
    '-log_path',
    dest='log_path',
    default='/var/log/zabbix/ip.log',
    # default='./ip.log',
    help='-log_path 停用了，处理结果保存路径，默认保存到/var/log/zabbix/ip.log')
args = parser.parse_args()


def open_log(path):
    offset = 0
    event = threading.Event()
    while not event.is_set():
        with open(path) as f:
            if offset > os.stat(path).st_size:
                offset = 0
            f.seek(offset)
            yield from f
            offset = f.tell()
        event.wait(1)


def analyzer(path):
    Last_time = datetime.datetime.now()
    ip_list = []
    o = re.compile(r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<other>.*)')
    for line in open_log(path):
        # t = datetime.datetime.now() - Last_time
        # print(t)
        if datetime.datetime.now() - Last_time > datetime.timedelta(
                seconds=args.Wait_time):
            # print('1')
            ip_list = []
            clear_data()
            Last_time = datetime.datetime.now()
            # f = open(args.log_path, 'w')
            # f.close()
        # print(Last_time)
        m = o.search(line.rstrip('\n'))
        # print(m)
        if m:
            d = m.groupdict()
            # print(d)
            if d['ip'] not in ip_list:
                ip_list.append(d['ip'])
                # print(ip_list)
                yield d['ip']


def clear_data():
    db = pymysql.connect("47.94.135.239", "grafana", "grafana", "grafana")
    db.cursor().execute('DELETE FROM ip_list')
    db.commit()
    db.close()


def ip_address(ip):
    apiurl = 'http://ip.taobao.com/service/getIpInfo.php?ip={}'.format(ip)
    data = urllib.request.urlopen(apiurl).read()
    data = json.loads(str(data, encoding="utf-8"))['data']
    if not data['region']:
        return '{}'.format(data['country'])
    return '{} {} {}'.format(data['region'], data['city'], data['isp'])


def insert_data(time, ip):
    address = ip_address(ip)
    db = pymysql.connect("47.94.135.239", "grafana", "grafana", "grafana")
    db.cursor().execute(
        "INSERT INTO ip_list (time,ip,source) VALUES ('{}','{}','{}')".
        format(time, ip, address))
    db.commit()
    db.close()


if __name__ == '__main__':
    for i in analyzer(args.file_path):
        # print(i)
        Now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 下面两行是写Now_time和i到文件中，如果记录数据到文件中需要同时取消59,60行的注释
        # with open(args.log_path, 'a') as logf:
        #     logf.write('[{}] {}\n'.format(Now_time, i))
        # 下面一行是写数据到数据库中，这一行需要57
        # 行的配合
        insert_data(Now_time, i)
