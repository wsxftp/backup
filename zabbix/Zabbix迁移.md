# Zabbix迁移

数据库备份

```bash
mysqldump -B zabbix --single-transaction -R --triggers -E --flush-logs --master-data=2 > zabbix.sql
```

zabbix服务器初始化脚本

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

zabbix运行环境准备脚本

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
GRANT ALL ON zabbix.* TO 'zbxuser'@'localhost' IDENTIFIED BY 'zbpass';
GRANT ALL ON zabbix.* TO 'zbxuser'@'127.0.0.1' IDENTIFIED BY 'zbpass';
EOF
```

zabbix安装启动

```bash
yum install zabbix-agent zabbix-get zabbix-sender zabbix-server-mysql zabbix-web zabbix-web-mysql -y
# 数据库导入
mysql < zabbix.sql
systemctl restart zabbix-server.service
```

访问主机ip，按照setup步骤生成`/etc/zabbix/web/zabbix.conf.php`文件，或者直接复制原本的配置文件到这个位置

***如果Zabbix设置监控Tomcat，需要自己配置***
