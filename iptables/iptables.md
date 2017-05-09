## 表和链的关系

* filter:过滤

  INPUT、FORWARD、OUTPUT

* nat:这个表是咨询当遇到包创建一个新的连接

  PREROUTING、OUTPUT、POSTROUTING

* mangle:这个表是用来专门包变更

  kernel 2.4.17及之前kernel只支持PREROUTING、OUTPUT

  从kernel 2.4.18开始在原来的基础上继续增加了INPUT、FORWARD、POSTROUTING的支持

* raw:这个表主要用于配置免除连接跟踪，需结合NOTRACK目标使用

  PREROUTING、OUTPUT

* security:这个表是用来强制访问控制(MAC)网络规则,比如SECMAR和CONNSECMARK目标。

  INPUT、OUTPUT、FORWARD



## 选项

### 增
* -A, --append chain rule-specification

  在链的最后追加一条规则到特定的链

  示例：`[root@centos7 ~]# iptables -A INPUT -s 172.18.99.3 -p tcp --dport 80 -j REJECT`

* -I, --insert chain [rulenum] rule-specification

  指定行号前插入一行一条规则到特定的链，不写`[rulenum]`时默认值是1

  示例一，在第二行之前插入一条规则`[root@centos7 ~]# iptables -I INPUT 2 -s 172.18.99.5 -p tcp --dport 80 -j REJECT`

  示例二，使用默认值，在第一行之前添加一条规则：`[root@centos7 ~]# iptables -I INPUT -s 172.18.99.6 -p tcp --dport 80 -j REJECT`

### 查

* -C, --check chain rule-specification

  查找一条规则是否存在，存在没有返回，不存在则返回`iptables: Bad rule (does a matching rule exist in that chain?).`

  示例：`[root@centos7 ~]# iptables -C INPUT -s 172.18.99.3 -p tcp --dport 80 -j REJECT`

* -L, --list [chain]

  列出某个链的规则，`[chain]`的默认值是filter

* -S, --list-rules [chain]

  列出某个链的规则，`[chain]`的默认值是filter

### 删

* -D, --delete chain rule-specification

  删除一条规则。先通过-C查找链是否存在，后使用-D删除

  示例：`[root@centos7 ~]# iptables -D INPUT -s 172.18.99.3 -p tcp --dport 80 -j REJECT`

* -D, --delete chain rulenum

  按照行号删除某一行，查找行号的方法`[root@centos7 ~]# iptables -L --line-number`

### 改










aaa
