#!/usr/bin/python3
# coding:utf-8
import requests
# import json

url = "http://api.sendcloud.net/apiv2/mail/send"
# 您需要登录SendCloud创建API_USER，使用API_USER和API_KEY才可以进行邮件的发送。
params = {
    "apiUser": "mortimer_test_jL6V39",
    "apiKey": "ooiXo3AOTAErP040",
    "from": "service@sendcloud.im",
    "fromName": "zabbix",
    "to": "328624847@qq.com",
    "subject": '服务器故障',
    "html": "服务器故障请查看zabbix，判断问题并处理问题",
}

r = requests.post(url, files={}, data=params)
# print(r.text)
