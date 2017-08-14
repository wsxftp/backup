# coding: utf-8
import smtplib
import time
from email.mime.text import MIMEText
# from email.header import Header

nowtime = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
<<<<<<< HEAD
sender = 'guocai666@21cn.com'
receiver = ['mortimer2017@163.com']
subject = 'ServerError at {}'.format(nowtime)
smtpserver = 'smtp.21cn.com'
=======
sender = 'mortimer2017@163.com'
receiver = ['328624847@qq.com']
subject = 'ServerError at {}'.format(nowtime)
smtpserver = 'smtp.163.com'
>>>>>>> 8de92378fbce13aae177c6da6dcbf82f79066814
username = sender
password = 'l7hqfr'

for i in receiver:
<<<<<<< HEAD
    msg = MIMEText('ServerError at {} please fix it'.format(nowtime), 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
=======
    msg = MIMEText('ServerError at {} please fix it'.format(nowtime), 'plain',
                   'utf-8')
    msg['Subject'] = subject
>>>>>>> 8de92378fbce13aae177c6da6dcbf82f79066814
    msg['From'] = sender
    msg['To'] = i
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, i, msg.as_string())
    smtp.quit()
