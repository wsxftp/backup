
```bash
#!/bin/bash

# 增加zabbix3yum源
cat > /etc/yum.repos.d/zabbix.repo <<EOF
[zabbix3.0]
name=zabbix3.0
baseurl=http://mirrors.aliyun.com/zabbix/zabbix/3.0/rhel/7/x86_64/
gpgcheck=0
EOF

# 安装git
yum install git -y
# 安装iftop,用于网络监控
yum install iftop -y
```

zabbix安装

```bash
#!/bin/bash

#安装httpd提供zabbix服务
yum install -y httpd php php-mysql mariadb-server

# 启动httpd和数据库,设置开机启动
systemctl start httpd.service
systemctl start mariadb.service
systemctl enable httpd.service
systemctl enable mariadb.service

# 导入数据库
mysql <<EOF
CREATE DATABASE zabbix CHARACTER SET utf8;
GRANT ALL ON zabbix.* TO 'zbxuser'@'localhost' IDENTIFIED BY 'guocai888';
GRANT ALL ON zabbix.* TO 'zbxuser'@'127.0.0.1' IDENTIFIED BY 'guocai888';
EOF
```

安装zabbix

```bash
yum install zabbix-agent zabbix-get zabbix-sender zabbix-server-mysql zabbix-web zabbix-web-mysql -y
#下面三步是给zabbix提供数据库支持，创建一些数据库表
cd /usr/share/doc/zabbix-server-mysql-3.0.9/
gunzip create.sql.gz
mysql -uzbxuser -hlocalhost -p"guocai888" -Dzabbix < create.sql
```

设置zabbix配置

```bash
vim /etc/zabbix/zabbix_server.conf

#编辑配置文件更改如下几行数据库主机、数据库名字、数据库用户、数据库密码
DBHost=localhost
DBName=zabbix
DBUser=zbxuser
DBPassword=zbxpass
```

启动服务，开机启动

```
systemctl start zabbix-server.service
systemctl enable zabbix-server.service
```

关闭linux系统图形界面

```
systemctl set-default multi-user.target
```


更改时区

```bash
vim /etc/php.ini

date.timezone = Asia/Shanghai
systemctl restart httpd.service
```

使用浏览器访问http://172.16.16.16/zabbix/setup.php

默认的用户名和密码admin/zabbix

更改浏览器访问路径为http://172.16.16.16的方法

```
vim /etc/httpd/conf/httpd.conf

DocumentRoot "/usr/share/zabbix"

systemctl restart httpd
```
