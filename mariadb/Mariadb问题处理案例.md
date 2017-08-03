
## 问题特征
mysql每天晚上一点到早上九点有大量的查询操作，在这段时间内MySQLd进程占满一颗CPU，最初发现这个问题是zabbix监控到的

## 第一次处理问题

直接使用mysql连接数据时，不能使用`show processlist\G`命令，初步判断是由于命令权限不足

重新授权`grant all on *.* to ''@'localhost'`，这时可以执行`show processlist\G`

第二天观察，晚上依然有大量的查询操作


## 第二次处理问题

使用`show processlist\G`命令，在晚上抓取数据

```
filename=mysql-`date|awk '{print $5}'`.log
mysql -e 'show processlist\G' > /tmp/mysqlcheck/$filename
```

抓取到大量的是sleep状态的数据，其中有一些Query的数据，数据如下
```
*************************** 14. row ***************************
     Id: 144932
   User: root
   Host: 10.28.***.***:52918
     db: niis_log
Command: Query
   Time: 0
  State: checking permissions
   Info: show tables like '2016_12_14'
--
*************************** 16. row ***************************
     Id: 144934
   User: root
   Host: 10.28.***.***:52920
     db: niis_log
Command: Query
   Time: 0
  State: checking permissions
   Info: show tables like '2016_12_15'
--
*************************** 20. row ***************************
```

出现`checking permissions`，一般有两个原因：

* 一个是用户数量太多，这个原因在我这里不适合，因为我的user表中只有5个用户

* 另一个原因是闰秒，我立即同步了时间

第二天，依然没有效果

## 第三次处理

这时我怀疑数据库被入侵了，开启日志抓取查询操作
```bash
# 设置日志保存方式，以文件方式保存
set global log_output=file;
# 设置保存文件名及位置，这里使用是默认位置在数据的数据目录下
set global general_log_file="general-log.log";
# 开始记录日志
set global general_log=on;
```

一部分日志的内容
```
170803  8:59:49	163839 Init DB	niis_log
		163839 Query	show tables like '2017_07_02'
		163835 Init DB	niis_log
		163835 Query	SELECT count(*) from 2017_07_02 where MD5 = '81BAF28E29749B*****************'
		163844 Init DB	niis_log
		163844 Query	show tables like '2017_07_02'
		163831 Init DB	niis_log
		163831 Query	SELECT count(*) from 2017_07_02 where MD5 = '09552B860E98D******************'
		163846 Init DB	niis_log
		163846 Query	show tables like '2017_07_02'
```

显然是有进程在处理数据

## 第四次处理

判断是什么进程在处理数据（这时需要加班了，因为只有夜里才处理数据）

`show processlist\G`命令抓取数据库正在执行的sql语句

```
*************************** 16. row ***************************
     Id: 144934
   User: root
   Host: 10.28.***.***:52920
     db: niis_log
Command: Query
   Time: 0
  State: checking permissions
   Info: show tables like '2016_12_15'
```

这里可以发现是通过`10.28.***.***:52920`地址发送来的请求，我竟然发现这是我们自己的服务器地址（开发给我挖了个坑），到相应的服务器找到使用该端口的进程`ps -ef|grep 52920`

接下来就是等待开发处理了
