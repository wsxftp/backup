常用模块，简称必须掌握的模块。

### ngx_http_access_module模块：

实现基于ip的访问控制功能

26、`allow address | CIDR | unix: | all;`允许哪些主机可以访问服务器

27、`deny address | CIDR | unix: | all;`拒绝哪些主机访问服务器

可以工作于http, server, location, limit_except配置段

### ngx_http_auth_basic_module模块

实现基于用户的访问控制，使用basic机制进行用户认证；

28、`auth_basic string | off;`认证页面提示内容

29、`auth_basic_user_file file;`认证使用存储密码文件

```
location /admin/ {
		alias /webapps/app1/data/;
		auth_basic "Admin Area";
		auth_basic_user_file /etc/nginx/.ngxpasswd;
}
```

**注意：htpasswd命令由httpd-tools所提供；**

### ngx_http_stub_status_module模块

用于输出nginx的基本状态信息；

```
Active connections: 291
server accepts handled requests
	16630948 16630948 31070465
Reading: 6 Writing: 179 Waiting: 106 	

	Active connections: 活动状态的连接数；
	accepts：已经接受的客户端请求的总数；
	handled：已经处理完成的客户端请求的总数；
	requests：客户端发来的总的请求数；
	Reading：处于读取客户端请求报文首部的连接的连接数；
	Writing：处于向客户端发送响应报文过程中的连接数；
	Waiting：处于等待客户端发出请求的空闲连接数；
```

30、`stub_status;`

配置示例：

```
location  /basic_status {
		stub_status;
}
```

### ngx_http_log_module模块
he ngx_http_log_module module writes request logs in the specified format.

31、`log_format name string ...;`string可以使用nginx核心模块及其它模块内嵌的变量；定义可以查看Nginx内置变量，自定义格式

32、`access_log path [format [buffer=size] [gzip[=level]] [flush=time] [if=condition]];`

```
access_log off;
访问日志文件路径，格式及相关的缓冲的配置；
		buffer=size
		flush=time 		
```

33、`open_log_file_cache max=N [inactive=time] [min_uses=N] [valid=time];`

	open_log_file_cache off;

```
缓存各日志文件相关的元数据信息；
max：缓存的最大文件描述符数量；
min_uses：在inactive指定的时长内访问大于等于此值方可被当作活动项；
inactive：非活动时长；
valid：验正缓存中各缓存项是否为活动项的时间间隔；
```

### ngx_http_gzip_module：
The ngx_http_gzip_module module is a filter that compresses responses using the “gzip” method. This often helps to reduce the size of transmitted data by half or even more.

1、`gzip on | off;`Enables or disables gzipping of responses.

2、`gzip_comp_level level;`Sets a gzip compression level of a response. Acceptable values are in the range from 1 to 9.

3、`gzip_disable regex ...;`Disables gzipping of responses for requests with “User-Agent” header fields matching any of the specified regular expressions.

4、`gzip_min_length length;`启用压缩功能的响应报文大小阈值；

5、`gzip_buffers number size;`支持实现压缩功能时为其配置的缓冲区数量及每个缓存区的大小；

6、`gzip_proxied off | expired | no-cache | no-store | private | no_last_modified | no_etag | auth | any ...;`nginx作为代理服务器接收到从被代理服务器发送的响应报文后，在何种条件下启用压缩功能的；

off：对代理的请求不启用

no-cache, no-store，private：表示从被代理服务器收到的响应报文首部的Cache-Control的值为此三者中任何一个，则启用压缩功能；		

7、`gzip_types mime-type ...;`压缩过滤器，仅对此处设定的MIME类型的内容启用压缩功能；

示例：

```
gzip  on;
gzip_comp_level 6;
gzip_min_length 64;
gzip_proxied any;
gzip_types text/xml text/css  application/javascript;						
```

### ngx_http_ssl_module模块：

1、`ssl on | off;`Enables the HTTPS protocol for the given virtual server.

2、`ssl_certificate file;`当前虚拟主机使用PEM格式的证书文件；

3、`ssl_certificate_key file;`当前虚拟主机上与其证书匹配的私钥文件；

4、`ssl_protocols [SSLv2] [SSLv3] [TLSv1] [TLSv1.1] [TLSv1.2];`支持ssl协议版本，默认为后三个；

5、`ssl_session_cache off | none | [builtin[:size]] [shared:name:size];`builtin[:size]：使用OpenSSL内建的缓存，此缓存为每worker进程私有；

[shared:name:size]：在各worker之间使用一个共享的缓存；

6、`ssl_session_timeout time;`客户端一侧的连接可以复用ssl session cache中缓存 的ssl参数的有效时长；

配置示例：
```
server {
		listen 443 ssl;
		server_name www.magedu.com;
		root /vhosts/ssl/htdocs;
		ssl on;
		ssl_certificate /etc/nginx/ssl/nginx.crt;
		ssl_certificate_key /etc/nginx/ssl/nginx.key;
		ssl_session_cache shared:sslcache:20m;
}							
```

### ngx_http_rewrite_module模块：

The ngx_http_rewrite_module module is used to change request URI using PCRE regular expressions, return redirects, and conditionally select configurations.

将用户请求的URI基于regex所描述的模式进行检查，而后完成替换；

1、`rewrite regex replacement [flag];`将用户请求的URI基于regex所描述的模式进行检查，匹配到时将其替换为replacement指定的新的URI；

注意：如果在同一级配置块中存在多个rewrite规则，那么会自下而下逐个检查；被某条件规则替换完成后，会重新一轮的替换检查，因此，隐含有循环机制；[flag]所表示的标志位用于控制此循环机制；

如果replacement是以http://或https://开头，则替换结果会直接以重向返回给客户端；
		301：永久重定向；

```
[flag]：
		last：重写完成后停止对当前URI在当前location中后续的其它重写操作，而后对新的URI启动新一轮重写检查；提前重启新一轮循环；
		break：重写完成后停止对当前URI在当前location中后续的其它重写操作，而后直接跳转至重写规则配置块之后的其它配置；结束循环；
		redirect：重写完成后以临时重定向方式直接返回重写后生成的新URI给客户端，由客户端重新发起请求；不能以http://或https://开头；
		permanent:重写完成后以永久重定向方式直接返回重写后生成的新URI给客户端，由客户端重新发起请求；
```


2、`return`

```
return code [text];
return code URL;
return URL;

Stops processing and returns the specified code to a client.
```

3、`rewrite_log on | off;`是否开启重写日志；

4、`if (condition) { ... }`引入一个新的配置上下文 ；条件满足时，执行配置块中的配置指令；server, location；

```
condition：
比较操作符：
		==
		!=
		~：模式匹配，区分字符大小写；
		~*：模式匹配，不区分字符大小写；
		!~：模式不匹配，区分字符大小写；
		!~*：模式不匹配，不区分字符大小写；
文件及目录存在性判断：
		-e, !-e
		-f, !-f
		-d, !-d
		-x, !-x
```

5、`set $variable value;`用户自定义变量 ；

6、`Syntax:	error_page code ... [=[response]] uri;`可以配置在http, server, location, if in location

示例

```
error_page 403      http://example.com/forbidden.html;
error_page 404 =301 http://example.com/notfound.html;
error_page 500 502 503 504 /50x.html;
location = /50x.html {
    /data/error_page
}
```

### ngx_http_fastcgi_module模块：

The ngx_http_fastcgi_module module allows passing requests to a FastCGI server.

1、`fastcgi_pass address;`address为fastcgi server的地址；	location, if in location；

2、`fastcgi_index name;`fastcgi默认的主页资源;

3、`fastcgi_param parameter value [if_not_empty];`Sets a parameter that should be passed to the FastCGI server. The value can contain text, variables, and their combination.

配置示例1：
前提：配置好fpm server和mariadb-server服务；

```
location ~* \.php$ {
		root           /usr/share/nginx/html;
		fastcgi_pass   127.0.0.1:9000;
		fastcgi_index  index.php;
		fastcgi_param  SCRIPT_FILENAME  /usr/share/nginx/html$fastcgi_script_name;
		include        fastcgi_params;
}
```


配置示例2：通过/pm_status和/ping来获取fpm server状态信息；

```
location ~* ^/(pm_status|ping)$ {
		include        fastcgi_params;
		fastcgi_pass 127.0.0.1:9000;
		fastcgi_param  SCRIPT_FILENAME  $fastcgi_script_name;
}			
```

4、`fastcgi_cache_path path [levels=levels] [use_temp_path=on|off] keys_zone=name:size [inactive=time] [max_size=size] [manager_files=number] [manager_sleep=time] [manager_threshold=time] [loader_files=number] [loader_sleep=time] [loader_threshold=time] [purger=on|off] [purger_files=number] [purger_sleep=time] [purger_threshold=time];`定义fastcgi的缓存；缓存位置为磁盘上的文件系统，由path所指定路径来定义；

```
levels=levels：缓存目录的层级数量，以及每一级的目录数量；levels=ONE:TWO:THREE
		leves=1:2:2
keys_zone=name:size
		k/v映射的内存空间的名称及大小
inactive=time
		非活动时长
max_size=size
		磁盘上用于缓存数据的缓存空间上限
```

5、`fastcgi_cache zone | off;`调用指定的缓存空间来缓存数据；http, server, location

6、`fastcgi_cache_key string;`定义用作缓存项的key的字符串；

7、`fastcgi_cache_methods GET | HEAD | POST ...;`为哪些请求方法使用缓存；

8、`fastcgi_cache_min_uses number;`缓存空间中的缓存项在inactive定义的非活动时间内至少要被访问到此处所指定的次数方可被认作活动项；

9、`fastcgi_cache_valid [code ...] time;`不同的响应码各自的缓存时长；

示例：

```
http {
		...
		fastcgi_cache_path /var/cache/nginx/fastcgi_cache levels=1:2:1 keys_zone=fcgi:20m inactive=120s;
		...
		server {
				...
				location ~* \.php$ {
						...
						fastcgi_cache fcgi;
						fastcgi_cache_key $request_uri;
						fastcgi_cache_valid 200 302 10m;
						fastcgi_cache_valid 301 1h;
						fastcgi_cache_valid any 1m;
						...
				}
				...
		}
		...
}
```

10、`fastcgi_keep_conn on | off;`By default, a FastCGI server will close a connection right after sending the response. However, when this directive is set to the value on, nginx will instruct a FastCGI server to keep connections open.


### ngx_http_referer_module模块：
	The ngx_http_referer_module module is used to block access to a site for requests with invalid values in the “Referer” header field.

1、`valid_referers none | blocked | server_names | string ...;`定义referer首部的合法可用值；

```
none：请求报文首部没有referer首部；
blocked：请求报文的referer首部没有值；
server_names：参数，其可以有值作为主机名或主机名模式；
arbitrary_string：直接字符串，但可使用*作通配符；
regular expression：被指定的正则表达式模式匹配到的字符串；要使用~打头，例如 ~.*\.magedu\.com；
```

配置示例：

```
valid_referers none block server_names *.magedu.com *.mageedu.com magedu.* mageedu.* ~\.magedu\.;
if($invalid_referer) {
		return 403;
}
```

### ngx_http_headers_module模块
The ngx_http_headers_module module allows adding the “Expires” and “Cache-Control” header fields, and arbitrary fields, to a response header.

向由代理服务器响应给客户端的响应报文添加自定义首部，或修改指定首部的值；

1、`add_header name value [always];`添加自定义首部；

```
add_header X-Via  $server_addr;
add_header X-Accel $server_name;
```

2、`expires [modified] time;` `expires epoch | max | off;`用于定义Expire或Cache-Control首部的值；


### ngx_http_upstream_module模块
The ngx_http_upstream_module module is used to define groups of servers that can be referenced by the proxy_pass, fastcgi_pass, uwsgi_pass, scgi_pass, and memcached_pass directives.

1、`upstream name { ... }`定义后端服务器组，会引入一个新的上下文；Context: http

```
upstream httpdsrvs {
		server ...
		server...
		...
}
```


2、`server address [parameters];`在upstream上下文中server成员，以及相关的参数；Context:	upstream

address的表示格式：

```bash
unix:/PATH/TO/SOME_SOCK_FILE
IP[:PORT]
HOSTNAME[:PORT]

parameters：
		#权重，默认为1；
		weight=number
		#失败尝试最大次数；超出此处指定的次数时，server将被标记为不可用；
		max_fails=number
		#设置将服务器标记为不可用状态的超时时长；
		fail_timeout=time
		#当前的服务器的最大并发连接数；
		max_conns
		#将服务器标记为“备用”，即所有服务器均不可用时此服务器才启用；
		backup
		#标记为“不可用”；
		down
```

3、`least_conn;`最少连接调度算法，当server拥有不同的权重时其为wlc;

4、`ip_hash;`源地址hash调度方法；

5、`hash key [consistent];`基于指定的key的hash表来实现对请求的调度，此处的key可以直接文本、变量或二者的组合；

作用：将请求分类，同一类请求将发往同一个upstream server；

If the consistent parameter is specified the ketama consistent hashing method will be used instead.

示例：

```
hash $request_uri consistent;
hash $remote_addr;
```

6、`keepalive connections;`为每个worker进程保留的空闲的长连接数量；


### ngx_stream_core_module模块

模拟反代基于tcp或udp的服务连接，即工作于传输层的反代或调度器；

1、`stream { ... }`定义stream相关的服务；Context:main

```
stream {
		upstream sshsrvs {
				server 192.168.22.2:22;
				server 192.168.22.3:22;
				least_conn;
		}
		server {
				listen 10.1.0.6:22022;
				proxy_pass sshsrvs;
		}
}
```

2、`listen`

listen address:port [ssl] [udp] [proxy_protocol] [backlog=number] [bind] [ipv6only=on|off] [reuseport] [so_keepalive=on|off|[keepidle]:[keepintvl]:[keepcnt]];



# 很重要，必须掌握
