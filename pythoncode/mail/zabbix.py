#!/usr/bin/python3
# coding: gb2312
import smtplib
import sys
from email.mime.text import MIMEText
# from email.header import Header

_, subject, *msgbody = sys.argv
sender = 'mortimer2017@163.com'
receiver = ['328624847@qq.com']
# subject = 'ServerError at {}'.format(nowtime)
smtpserver = 'smtp.163.com'
username = sender
password = 'wyc12345'

for i in receiver:
    msg = MIMEText(' '.join(msgbody), 'plain',
                   'gb2312')
    msg['Subject'] = str(subject)
    msg['From'] = sender
    msg['To'] = i
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, i, msg.as_string())
    smtp.quit()
