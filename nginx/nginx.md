# log

## debugging log

全局启用debug日志，而某个server不使用debug

```
error_log /path/to/log debug;

http {
    server {
        error_log /path/to/log;
        ...
```

全局启用debug日志，而某个server使用其他文件记录debug日志

```
error_log /path/to/log debug;

http {
    server {
        error_log /path/to/log debug;
        ...
```

只针对记录某些客户端的debug日志

```
error_log /path/to/log;

events {
    debug_connection 192.168.1.1;
    debug_connection 192.168.10.0/24;
}
```

环形内存记录debug日志

`error_log memory:32m debug;` 日志量很大的时候可以使用


## 记录日志到syslog

`server=address`

server地址可以使用域名也可以是ip地址

`facility=string`

Sets facility of syslog messages, as defined in RFC 3164. Facility can be one of “kern”, “user”, “mail”, “daemon”, “auth”, “intern”, “lpr”, “news”, “uucp”, “clock”, “authpriv”, “ftp”, “ntp”, “audit”, “alert”, “cron”, “local0”..“local7”. Default is “local7”.

`severity=string`

Sets severity of syslog messages for access_log, as defined in RFC 3164. Possible values are the same as for the second parameter (level) of the error_log directive. Default is “info”.
Severity of error messages is determined by nginx, thus the parameter is ignored in the error_log directive.

`tag=string`

标签，Sets the tag of syslog messages. Default is “nginx”.

`nohostname`

通过sock通信时，不需要使用主机ip或者域名。Disables adding the “hostname” field into the syslog message header (1.9.7).



示例

```
Example syslog configuration:

error_log syslog:server=192.168.1.1 debug;

access_log syslog:server=unix:/var/log/nginx.sock,nohostname;
access_log syslog:server=[2001:db8::1]:12345,facility=local7,tag=nginx,severity=info combined;
```

# 配置文件的度量单位

文件大小单位

```
1024    Byte
8k    1024Byte
1m    1024K
1G/1g   1024m
```



时间单位

```
ms	milliseconds
s	seconds
m	minutes
h	hours
d	days
w	weeks
M	months, 30 days
y	years, 365 days
```


## nginx命令使用

```
nginx -h
nginx version: nginx/1.10.2
Usage: nginx [-?hvVtTq] [-s signal] [-c filename] [-p prefix] [-g directives]

Options:
  -?,-h         : 帮助
  -v            : 显示Nginx版本
  -V            : 显示Nginx版本和编译选项
  -t            : 测试配置文件
  -T            : 测试配置文件，转储并退出
  -q            : 在配置测试期间禁止非错误消息
  -s signal     : 向Nginx主进程发送一个信号: stop, quit, reopen, reload
  -p prefix     : set prefix path (default: /usr/share/nginx/)
  -c filename   : set configuration file (default: /etc/nginx/nginx.conf)
  -g directives : set global directives out of configuration file
```

`nginx -s signal`

可以使用的signal

```
stop — fast shutdown，直接停止服务
quit — graceful shutdown，处理完请求后停止服务
reload — reloading the configuration file，从新加载配置文件。建立新进程接受请求。旧worker进程不接受新请求，并在处理完成接受后退出。
reopen — reopening the log files。从新打开日志，用于日志滚动。日志滚动式为了防止日志文件过大。一个日志滚动脚本示例如下
```

Nginx日志滚动脚本

```bash
#!/bin/bash
logs_path='/data/logs'

mkdir -pv ${logs_path}$(date -d "yesterday" +"%Y")/$(date -d "yesterday" +"%m")/
mv ${logs_path}/access.log ${logs_path}$(date -d "yesterday" +"%Y")/$(date -d "yesterday" +"%m")/access_$(date -d "yesterday" +"%Y%m%d").log
nginx -s reopen
```







* 负载均衡  

upstream

调度算法

proxy_pass

* Rewrite


    Nginx的rewrite和apache的RewriteRule差别不大

break

if


perl正则

Nginx内置变量

允许指定域名访问本站


* cache

ncache

fastcache

*
