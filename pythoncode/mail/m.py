#coding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
      
sender = 'mortimer2017@163.com'
receiver = "328624847@qq.com"
subject = '放假通知'
smtpserver = 'smtp.163.com'
username = 'mortimer2017@163.com'
password = 'wyc12345'
      
msg = MIMEText('大家关好窗户','plain','utf-8')#中文需参数‘utf-8'，单字节字符不需要
msg['Subject'] = Header(subject, 'utf-8')
msg['From'] = 'mortimer2017@163.com'
msg['To'] = "328624847@qq.com"
smtp = smtplib.SMTP()
smtp.connect(smtpserver)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()