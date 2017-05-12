
这一篇博客只介绍工作原理，绝不介绍网页添加监控项的操作，因为操作步骤实在是繁琐，并且都是可视化的操作，当我们理解原理之后，繁琐的操作其实就是完成一个很简单的功能，一步步的操作都是这个功能的一些特性。


## 一 zabbix理论

一次监控调用过程（不严谨只是适合记忆）

```
hostgroup and host and templates
application and item
trigger and graph and screen
acction
usergroup and user and media
```

* hostgroup and host and templates

通过组对主机进行分类，监控哪些组内的哪些用户,还有最重要的templates模板，模板的功能就是为同一类的主机提供监控的模板，它的定义方式和主机添加application、item、trigger、graph和screen的方式一样

* application 和 item

监控项和监控内容，监控项iterm和监控项的分组application

* trigger、graph和screen

基于监控项定义的报警器trigger，基于监控项定义的图片graph和基于graph组合成的sreen，这一部分是最重要的部分，三个都要熟练掌握使用

* acction and event

报警和触发事件，根据trigger触发情况定义后续操作，这个歌操作可以是发送邮件执行脚本发送短信

* usergroup and user and media

这里的账号是zabbix建立的虚拟账号，和虚拟账号组,把信息发送给用户后，zabbix虚拟用户用户需要采取一定的方式发送给真实的管理员，这里是定义管理员支持的通知方式


## 二 zabbix基础使用

```bash
#可视化监控页面
monitoring
#主机仓库列表
inventory
#所以信息统计后的概览
reports
#配置管理
configuration
#用户的媒介管理
administration
```

zabbix没有被收录进yum源中，但是官方提供了一个yum源,官方源的地址http://repo.zabbix.com/zabbix/，官方的源速度特别慢这里我使用的是aliyun

```
vim /etc/yum.repos.d/base7.repo

[zabbix3.0]
name=zabbix3.0
baseurl=http://mirrors.aliyun.com/zabbix/zabbix/3.0/rhel/7/x86_64/
gpgcheck=0
```

### 1 创建zabbix-server

* 这里我的主机是centos7，6的话数据库安装mysql,以下操作是给zabbix-server提供数据库和web页面支持

```
yum install -y httpd php php-mysql mariadb-server
systemctl start httpd.service
systemctl start marriadb.service
mysql <<eof
CREATE DATABASE zabbix CHARACTER SET utf8;
GRANT ALL ON zabbix.* TO 'zbxuser'@'localhost' IDENTIFIED BY 'zbxpass';
GRANT ALL ON zabbix.* TO 'zbxuser'@'127.0.0.1' IDENTIFIED BY 'mageedu';
GRANT ALL ON zabbix.* TO 'zbxuser'@'172.16.%.%' IDENTIFIED BY 'mageedu';
eof
```

* 安装zabbix

安装zabbix的客户端，拉取数据的get方法，推数据的sender方法，zabbix的server端这个包中包含zabbix连接数据的方法，提供zabbix网页页面，zabbix网页的数据库使用支持

```bash
yum install zabbix-agent zabbix-get zabbix-sender zabbix-server-mysql zabbix-web zabbix-web-mysql -y
#下面三步是给zabbix提供数据库支持，创建一些数据库表
cd /usr/share/doc/zabbix-server-mysql-3.2.3/
gunzip create.sql.gz
mysql -uzbxuser -hlocalhost -p"zbxpass" -Dzabbix < create.sql
vim /etc/zabbix/zabbix_server.conf

#编辑配置文件更改如下几行数据库主机、数据库名字、数据库用户、数据库密码
DBHost=localhost
DBName=zabbix
DBUser=zbxuser
DBPassword=zbxpass
systemctl restart zabbix-server.service

vim /etc/php.ini
#更改时区
date.timezone = Asia/Shanghai
systemctl restart httpd.service
http://172.16.253.135/zabbix/setup.php
#访问网站，使用setup.php后一定要把这个文件mv到其他不可以访问的目录下面，防止zabbix被重置，万一被重置只能找地方哭去了。
```

默认的用户名和密码admin/zabbix


### 2 添加被监控主机

* 客户端的配置

```bash
yum install zabbix-agent zabbix-sender -y #给被监控主机安装zabbix客户端
vim /etc/zabbix/zabbix_agentd.conf #运行哪些主机监控这台主机，更改agent名字
Server=127.0.0.1,172.16.29.2
Hostname=node2
```

* 服务端配置

然后就可以在server的web页面里添加这台主机了

```bash
主机可以定义的的选项
	application #item的组
	items #item选项
	trigger #报警项
	graph #图
	screen #图组
	web #网页监控选项
```

### 3 添加items

select找到对应的item，查看简单提示，需要高级用法需要查看官方文档

trend storage period #趋势数据

store value:数据怎么存储


### 4 创建trigger

trigger依赖于item，item只负责收集数据，trigger负责给数据定义范围，也就是把数据的值分为多个等级比如10代表正常10代表警告1000代表异常


### 5 添加action

action依赖于trigger，定义的等级当数据到达某个阈值的时候应该怎么办，action就提供了怎么办的定义方式，

* 当出现某个阈值的时候执行某个定义好的脚步

脚步存放的路径/usr/lib/zabbix/alertscripts

* 给某个管理员发送信息

* 以上两个可以结合起来使用，比如出现故障10分钟之内，执行脚步，十分钟之后依然处于故障状态就通知某个管理员


### 6 madie和user


通知管理员那就有一个问题了，怎么通知管理员通知哪些管理员

* user

user的用户是zabbix的用户，每个管理员都会拥有一个自己的账号，并因为这个账号会受到不同的通知信息

* madie

```
madie通知管理员的媒介，媒介的方式
	Email
	script
	sms
```

目前很多公司都使用sms或者购买短信通知客户端，这种方式可以最大程度上保证通信的畅通，也是我们7*24的根源


## 三 zabbix高级用法


### 1 宏和自定义key

* 宏

宏就相当于变量，在administration中general的macros，定义和引用变量都要带$符，例如{$PORT}

* 自定义key

这个是在客户端定义，然后服务器调用


在客户端定义如下

```bash
vim /etc/zabbix/zabbix_agentd.conf #编辑parameter
#   Format: UserParameter=<key>,<shell command>
UserParameter=mem.total,free | awk '/Mem/ {print$2}'
UserParameter=mem.info[*],cat /proc/meminfo| awk '/^$1/ {print $$2}'
systemctl restart zabbix-agent.service
```

服务端引用

```bash
zabbix_get -s 172.16.29.20 -p 10050 -k mem.total #使用命令直接查看试试
zabbix_get -s 172.16.29.20 -p 10050 -k mem.info[MemFree]
zabbix_get -s 172.16.29.20 -p 10050 -k mem.info[MemTotal]
```

网页引用自定义变量需要手动输入key，例如mem.info[MemTotal]

客户端第二个parameter的功能就强大很多了,我们还可以把key和macros结合起来使用


### 2 创建和管理graph、screen

我们监控的数据可能会有很多，只要超出阈值报错，真正需要实时查看涨跌的数据就不是那么多了，并且需要把两项类似的数据对比查看，这时我们可以使用graph把需要的数据绘制在一幅图里面。

screen是在一个页面里一次展示多少张图，以怎样的体位展示出来，方便给老总汇报和展示公司数据情况


### 3 主机发现和web监控

* action

主机发现，这是一个很高能的功能，也是特别实用的功能，一个公司的服务器类型不过10种，现在流程微服务基本上一个服务器只有一个提供服务器的端口，只要我们给每个服务定义好监控模板，我们定义一个发现规则，当发现某个端口是处于监听状态就给该主机套用该模板。

公司规模一般的话，公司服务器的个数基本固定，并且一定时间内变化的可能性不大，即使服务器变化也在10台左右，服务间耦合度也比较高，这种情况也不是很适合使用服务器发现，服务发现的使用成本会大于收益。但是公司使用虚拟化后，公司服务器是动态变化并且但服务器只提供一项服务，这时使用发现就比较合适。没有确定的规范最好方法就是感觉手动添加监控的次数达到每三天一次以上就上自动发现。

配置位置configuration的discovery

* web监控

只有服务器端口指标的话，有时服务器正常运行但是不能提供网页，这种情况就比较奇葩了，但是这种情况对公司的影响极其严重，发现难度很大，等到发现之后客户已经流失了。zabbix就提供一些web监控的一些方法。

在host那里有web按钮，进入添加web监控指标就好了，不要监控太多，只监控最重要的几个入口页面就可以


### 4 active和snmp

* active

当服务器数量比较大的时候，zabbix服务器需要大量的服务器发送请求监控数据，服务器很有可能忙不过来，这时就需要客户端主动发送数据到服务器端以减少zabbix服务器端的压力。

既然是客户端发送数据那么就会引来一个问题，客户端故障怎么判断，很容易了只要在监控的时间间隔内数据没有发送过来就判定这次数据失效，这就要求服务器端和客户端的时间需要同步

客户端配置

```bash
	ServerActive=127.0.0.1，172.16.29.2 #填上服务器端的ip
```

服务器端

在选择item监控方式的时候选择agent（active)就可以了，主动模式的key和被动模式的key有点不同

* snmp

很多比较老的设备或者不装操作系统的设备，我们没有agent，这里只好借用snmp协议进行通信，snmp有三个版本v1，v2，v3，v2，v3版本虽然功能强大很多但是我们监控的是比较老旧的设备并且很多年固件没有升级的设备，这种设备基本上只支持v1，监控硬件需要监控的指标也不需要特别复杂。snmp的性能不是很好比agent差一些，能用agent就不用snmp。

客户端配置，开启snmp服务，这个方法需要根据不同的设备的情况确定

服务器端，item监控方式选择哪个版本的snmp就可以了


### 5 proxy和整体性能优化

* proxy

当监控项继续增大，一个zabbix主机即使使用active不能完成需求的时候，这时我们必须增加监控主机，两台zabbix主机监控的话数据聚合又是一个老大难得问题。这里zabbix开发有proxy机制，就是使用一台主机协助zabbix收集数据，一段时间后把主机收集的数据一次性发给zabbix服务器端。

proxy的安装

```bash
yum install -y mariadb-server
mysql <<eof
CREATE DATABASE zabbix CHARACTER SET utf8;
GRANT ALL ON zabbix.* TO 'zbxuser'@'localhost' IDENTIFIED BY 'zbxpass';
GRANT ALL ON zabbix.* TO 'zbxuser'@'127.0.0.1' IDENTIFIED BY 'mageedu';
GRANT ALL ON zabbix.* TO 'zbxuser'@'172.16.%.%' IDENTIFIED BY 'mageedu';
eof
yum install zabbix-agent zabbix-get zabbix-sender zabbix-proxy-mysql -y
cd /usr/share/doc/zabbix-proxy-mysql-3.2.3/ #下面三步是给zabbix提供数据库支持，创建一些数据库表
gunzip create.sql.gz
mysql -uzbxuser -hlocalhost -p"zbxpass" -Dzabbix < create.sql
vim /etc/zabbix/zabbix_proxy.conf #编辑配置文件更改如下几行数据库主机、数据库名字、数据库用户、数据库密码
DBHost=
DBName=
DBUser=
DBPassword=
Hostname= #注意不要和服务器端重名
systemctl restart zabbix-proxy.service
```

服务器端的配置就是在administrator的proxies中添加一个主机，使用proxy监控数据的时候，只要在创建主机的时候选择使用哪个proxy

* 性能优化

能用钱解决监控主机不足的话一定不要用，保持和别人不一样的代价是很大的。


数据不要保持太多
减少使用聚合函数比如avg(),max(),min(),sum()
减少使用snmp/agent-less/agent,尽量使用agent(active)
收集的数据尽量收集无符号数字，减少test，string


# 总结

zabbix有三个重点，也是我们最常使用的，但是有一个前提基础的item必须熟练使用，根据业务需要尽量找到对应的模块。

* monitoring各页面功能

* configrutra

	templaters

	host

	graph and screen

* administrator

	media一般使用第三方的短信工具
