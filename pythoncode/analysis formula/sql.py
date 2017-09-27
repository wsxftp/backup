# coding: utf8
import pymysql

time = '2'
ip = '3'
source = '中文'

db = pymysql.connect(
    "47.94.135.239", "grafana", "grafana", "grafana", charset='utf8')
db.cursor().execute(
    "INSERT INTO ip_list (time,ip,source) VALUES ('{}','{}','{}')".format(
        time, ip, source))
db.commit()
db.close()
