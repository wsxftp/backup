# zabbix客户端安装

[zabbix客户端下载地址]http://www.zabbix.com/downloads/3.0.4/zabbix_agents_3.0.4.win.zip

解压到C:\zabbix目录下

修改配置文件c:\zabbix\conf\zabbix_agentd.win.conf
```bash
# 124.207.65.***为zabbix-server的地址
Server=127.0.0.1,124.207.65.***

# 每个被监控主机Hostname名称需不同
Hostname=ZabbixServer
```

安装zabbix`c:\zabbix\bin\win64\zabbix_agentd.exe -c c:\zabbix\conf\zabbix_agentd.win.conf -i`

以服务的形式启动zabbix`c:\zabbix\bin\win64\zabbix_agentd.exe -c c:\zabbix\conf\zabbix_agentd.win.conf -s`

开始->控制面板->管理工具->服务

![](zabbix-agent.png)

由上图可以得到，zabbix-agent已经运行，并开机自动运行

参数含义：
```
-c 制定配置文件所在位置
-i 是安装客户端
-s 启动客户端  
-x 停止客户端  
-d 卸载客户端
```

***如果遇到zabbix-agent服务启动不了，换一个版本就好了，别试图修复！！！***
