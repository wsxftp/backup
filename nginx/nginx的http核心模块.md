nginx设计最初是为了解决c10k问题作为反向代理服务器，可以反向代理http和smtp/pop3请求，但是很快就被一群没有get到重点的公司带上了web服务器的不归路，比如某宝就开发了tengine,使用Nginx作为web服务器的原因是Nginx作为反向代理服务器需要缓存客户端持久连接状态，可以缓冲大量图片和视频，当收到图片视频数据请求的时候直接从缓存中调取数据响应，缓存技术在Nginx上应用的淋漓尽致，后面Nginx配置时可以发现大量的缓存缓冲配置指令基本上可以缓存的都有具体的指令。Nginx不就在“弯路”上越做越远，老本行反向代理也越来越强大经过一段时间的迭代现在的nginx可以代理大多数的tcp/udp协议，比如mysql，dns。


# 一 i/o模型

了解io模型我们才可以区分出Nginx和Apache的区别，才可以知道如日中天的Apache如何走向低谷。什么是io模型，它是怎么产生的？

它的产生是因为一次web请求，计算机内部需要调用各种资源，然而各种资源有调用顺序和获取速度的差异，由于这些差异导致某些处理已经完成，但是它需要另外一个速度慢的资源的数据。这就产生一个进程等待另一个进程的情况，这时这两个进程的通信的方式就是i/o模型。一个进程等待另一个进程，还有一种情况和编程里的函数调用类似。

## 同步/异步

`它的意思是调用者怎么获取另一个进程的处理状态情况。`

同步的意思是自己什么事情都不做等着另一个进程通知它发送数据

异步的意思是自己每个一段时间就去另一个进程那里获取一下处理状态

## 阻塞/非阻塞

`它的意思是调用者在调用后自己的状态`

阻塞是调用后就不再处理数据，只接收被调用者的信息

非阻塞是调用后还处理数据，不仅接收别调用者的信息

## 五种i/o模型

阻塞型，非阻塞型，复用型，信号驱动，异步

这里先统一一个概念，我们把一次i/o调用分为两个步骤：第一步是被调用获取数据，第二步是被调用进程把数据传输给调用者

阻塞型，第一步的时候阻塞自己，并使用同步的方式接收通知，第二步阻塞自己并接收被调用者发送的数据

非阻塞型，第一步不阻塞自己可以接收数据，并且一次次的向被调用请求处理状态，第二步阻塞自己并接收被调用者发送的数据

复用型，第一步阻塞自己，但是同时调用多个进程获取多分数据，第二步阻塞自己并接收被调用者发送的数据

信号驱动，第一步不阻塞自己，一旦收到被调用者的信号就进入第二步，第二步阻塞自己并接收被调用者发送的数据

异步，第一步不阻塞自己，一旦收到被调用者的信号就直接使用数据，第二步不阻塞自己，数据由被调用者直接写到调用者的内存中


# 二 文件结构

程序，配置文件，日志滚动配置

## 程序文件

使用rpm包安装的

对应的nginx命令可以使用的参数

```
不加任何参数，启动Nginx
-t #检查配置文件的语法
-s #Nginx传递一个参数，常用的reload，stop，restart
```

## 配置文件

主配置文件/etc/nginx/nginx.conf

主要是配置main block和http，main block是配置Nginx进程的基本配置，http配置和http相关的属性

模块化的配置文件/etc/nginx/conf.d/，主要是配置各虚拟主机server

日志滚动配置，这个是防止日志文件过大设置的位置


# 三 主配置文件和模块配置文件内容

## 事件驱动

main block除了对Nginx进程的配置还有对事件的配置，这也是Nginx可以支持c10k的根本。事件机制采用一个进程响应多个请求，但是和线程不同。

在多线程版本中，这3个任务分别在独立的线程中执行。这些线程由操作系统来管理，在多处理器系统上可以并行处理，或者在单处理器系统上交错执行。这使得当某个线程阻塞在某个资源的同时其他线程得以继续执行。与完成类似功能的同步程序相比，这种方式更有效率，但程序员必须写代码来保护共享资源，防止其被多个线程同时访问。多线程程序更加难以推断，因为这类程序不得不通过线程同步机制如锁、可重入函数、线程局部存储或者其他机制来处理线程安全问题，如果实现不当就会导致出现微妙且令人痛不欲生的bug。

在事件驱动版本的程序中，3个任务交错执行，但仍然在一个单独的线程控制中。当处理I/O或者其他昂贵的操作时，注册一个回调到事件循环中，然后当I/O操作完成时继续执行。回调描述了该如何处理某个事件。事件循环轮询所有的事件，当事件到来时将它们分配给等待处理事件的回调函数。这种方式让程序尽可能的得以执行而不需要用到额外的线程。事件驱动型程序比多线程程序更容易推断出行为，因为程序员不需要关心线程安全问题。


## main配置段常见的配置指令：

main配置段按照指令性质分类如下：

* 正常运行必备的配置

*	优化性能相关的配置

*	用于调试及定位问题相关的配置

*	事件驱动相关的配置

### 正常运行必备的配置

1、`user`指定运行worker进程的用户和组

```
Syntax:	user user [group]
Default:	user nobody nobody
```

2、`pid /PATH/TO/PID_FILE;`指定存储nginx主进程进程号码的文件路径

3、`include file | mask;`指明包含进来的其它配置文件片断

4、`load_module file;`指明要装载的动态模块

### 性能优化相关的配置

1、`worker_processes number | auto;`worker进程的数量；通常应该为当前主机的cpu的物理核心数

2、`worker_cpu_affinity cpumask ...;`

worker_cpu_affinity auto [cpumask]

CPU MASK：

00000001：0号CPU

00000010：1号CPU

... ...

3、`worker_priority number;`指定worker进程的nice值，设定worker进程优先级；[-20,20]

4、`worker_rlimit_nofile number;`worker进程所能够打开的文件数量上限

### 调试、定位问题：

1、`daemon on|off;`是否以守护进程方式运行Nignx

2、`master_process on|off;`是否以master/worker模型运行nginx；默认为on

3、`error_log file [level];`错误日志级别

### 事件驱动相关的配置:

事件相关配置都放在events配置段中

```
events {
...
}
```

1、`worker_connections number;`每个worker进程所能够打开的最大并发连接数数量

2、`use method;`指明并发连接请求的处理方法；#常用方法epoll

3、`accept_mutex on | off;`处理新的连接请求的方法；on意味着由各worker轮流处理新请求，Off意味着每个新请求的到达都会通知所有的worker进程


## 与套接字相关的配置

1、`server { ... }`配置一个虚拟主机；

```
	server {
		listen address[:PORT]|PORT;
		server_name SERVER_NAME;
		root /PATH/TO/DOCUMENT_ROOT;
	}
```

2、`listen PORT|address[:port]|unix:/PATH/TO/SOCKET_FILE;`

```
  listen address[:port] [default_server] [ssl] [http2 | spdy]  [backlog=number] [rcvbuf=size] [sndbuf=size]
	default_server：设定为默认虚拟主机；
	ssl：限制仅能够通过ssl连接提供服务；
	backlog=number：后援队列长度；
	rcvbuf=size：接收缓冲区大小；
	sndbuf=size：发送缓冲区大小；
```

3、`server_name name ...;`

指明虚拟主机的主机名称；后可跟多个由空白字符分隔的字符串；

支持*通配任意长度的任意字符；server_name *.magedu.com  www.magedu.*

支持~起始的字符做正则表达式模式匹配；server_name ~^www\d+\.magedu\.com$

```
	匹配机制：
		(1) 首先是字符串精确匹配;
		(2) 左侧*通配符；
		(3) 右侧*通配符；
		(4) 正则表达式；
```

4、`tcp_nodelay on | off;`在keepalived模式下的连接是否启用TCP_NODELAY选项；

5、`sendfile on | off;`是否启用sendfile功能；

## 定义路径相关的配置：

6、`root path;`设置web资源路径映射；用于指明用户请求的url所对应的本地文件系统上的文档所在目录路径；可用的位置：http, server, location, if in location；

7、`location [ = | ~ | ~* | ^~ ] uri { ... }`

`location @name { ... }`在一个server中location配置段可存在多个，用于实现从uri到文件系统的路径映射；ngnix会根据用户请求的URI来检查定义的所有location，并找出一个最佳匹配，而后应用其配置；

```
=：对URI做精确匹配；例如, http://www.magedu.com/, http://www.magedu.com/index.html
		location = / {
			...
		}
~：对URI做正则表达式模式匹配，区分字符大小写；
~*：对URI做正则表达式模式匹配，不区分字符大小写；
^~：对URI的左半部分做匹配检查，不区分字符大小写；
不带符号：匹配起始于此uri的所有的url；
匹配优先级：=, ^~, ～/～*，不带符号；
```

配置示例

```
	root /vhosts/www/htdocs/
		http://www.magedu.com/index.html --> /vhosts/www/htdocs/index.html
	server {
		root  /vhosts/www/htdocs/
		location /admin/ {
			root /webapps/app1/data/
		}
	}
```

8、`alias path;`定义路径别名，文档映射的另一种机制；仅能用于location上下文；

注意：location中使用root指令和alias指令的意义不同；

(a) root，给定的路径对应于location中的/uri/左侧的/；

(b) alias，给定的路径对应于location中的/uri/右侧的/；		

9、`index file ...;`默认资源；http, server, location；

10、`error_page code ... [=[response]] uri;`Defines the URI that will be shown for the specified errors. 	

11、`try_files file ... uri;`

## 定义客户端请求的相关配置

12、`keepalive_timeout timeout [header_timeout];`设定保持连接的超时时长，0表示禁止长连接；默认为75s；

13、`keepalive_requests number;`在一次长连接上所允许请求的资源的最大数量，默认为100; 	

14、`keepalive_disable none | browser ...;`对哪种浏览器禁用长连接；

15、`send_timeout time;`向客户端发送响应报文的超时时长，此处，是指两次写操作之间的间隔时长；

16、`client_body_buffer_size size;`用于接收客户端请求报文的body部分的缓冲区大小；默认为16k；超出此大小时，其将被暂存到磁盘上的由client_body_temp_path指令所定义的位置；

17、`client_body_temp_path path [level1 [level2 [level3]]];`设定用于存储客户端请求报文的body部分的临时存储路径及子目录结构和数量；

```
		16进制的数字；
		client_body_temp_path path  /var/tmp/client_body  1 2 2
```

## 对客户端进行限制的相关配置：

18、`limit_rate rate;`限制响应给客户端的传输速率，单位是bytes/second，0表示无限制；

19、`limit_except method ... { ... }`限制对指定的请求方法之外的其它方法的使用客户端；

```
	limit_except GET {
		allow 192.168.1.0/24;
		deny  all;
	}							
```

## 文件操作优化的配置

20、`aio on | off | threads[=pool];`是否启用aio功能；

21、`directio size | off;`在Linux主机启用O_DIRECT标记，此处意味文件大于等于给定的大小时使用，例如directio 4m;

22、`open_file_cache off;`

```
	open_file_cache max=N [inactive=time];
		nginx可以缓存以下三种信息：
			(1) 文件的描述符、文件大小和最近一次的修改时间；
			(2) 打开的目录结构；
			(3) 没有找到的或者没有权限访问的文件的相关信息；
		max=N：可缓存的缓存项上限；达到上限后会使用LRU算法实现缓存管理；
		inactive=time：缓存项的非活动时长，在此处指定的时长内未被命中的或命中的次数少于open_file_cache_min_uses指令所指定的次数的缓存项即为非活动项；
```

23、`open_file_cache_valid time;`缓存项有效性的检查频率；默认为60s;

24、`open_file_cache_min_uses number;`在open_file_cache指令的inactive参数指定的时长内，至少应该被命中多少次方可被归类为活动项；

25、`open_file_cache_errors on | off;`是否缓存查找时发生错误的文件一类的信息；


# 总结

配置指令特别复杂，重点是记住原理，并且都是重点，Nginx是伴随我们一生的工具，慢慢了解就好。并且这里只介绍了最基本http核心模块的使用，还有大量模块没有介绍，并且比这里的内容还要重要。我不介绍了：）
