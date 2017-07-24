
客户端的配置

```bash
#!/bin/bash

# 增加zabbix3yum源
cat > /etc/yum.repos.d/zabbix.repo <<EOF
[zabbix3.0]
name=zabbix3.0
baseurl=http://mirrors.aliyun.com/zabbix/zabbix/3.0/rhel/7/x86_64/
gpgcheck=0
EOF

#给被监控主机安装zabbix客户端
yum install zabbix-agent -y
```

允许哪些主机监控这台主机，更改agent名字

```bash
vim /etc/zabbix/zabbix_agentd.conf

#124.207.65.146为zabbix-server的地址
Server=127.0.0.1,124.207.65.***

#每个被监控主机Hostname名称需不同
Hostname=ZabbixServer

# 允许执行action传递的命令
EnableRemoteCommands=1
```

启动服务器，开机启动

```bash
systemctl enable zabbix-agent.service
systemctl start zabbix-agent.service
```

```bash
visudo

# allows 'zabbix' user to restart nginx without password.
zabbix ALL=NOPASSWD: /usr/local/nginx/sbin/nginx -s reload

# allows 'zabbix' user to check mysql without password.
zabbix ALL=NOPASSWD: /bin/mysqlslave.sh
```
