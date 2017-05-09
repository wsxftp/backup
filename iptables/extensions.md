# 显式扩展

在iptalbes中数据包和被跟踪连接的4种不同状态相关联，这四种状态分别是NEW、ESTABLISHED、RELATED及INVALID，除了本机产生的数据包由NAT表的OUTPUT链处理外，所有连接跟踪都是在NAT表的PREROUTING链中进行处理的，也就是说iptables在NAT表的PREROUTING链里从新计算所有数据包的状态。如果发送一个流的初始化数据包，状态就会在NAT表的OUTPUT链里被设置为NEW，当收到回应的数据包时，状态就会在NAT表的PREROUTING链里被设置为ESTABLISHED，如果第一个数据包不是本机生成的，那就回在NAT表PREROUTING链里被设置为NEW状态，所以所有状态的改变和计算都是在NAT表中的表链和OUTPUT链里完成的。

使用-m来指定其状态并赋予匹配规则，语法如下

## -m state --state 状态

   NEW

   ESTABLISHED

   RELATED          

   INVALID

NEW：

NEW状态的数据包说明这个数据包是收到的第一个数据包。比如收到一个SYN数据包，它是连接的第一个数据包，就会匹配NEW状态。第一个包也可能不是SYN包，但它仍会被认为是NEW状态。

ESTABLISHED：

只要发送并接到应答，一个数据连接就从NEW变为ESTABLISHED,而且该状态会继续匹配这个连接后继数据包。

RELATED：

当一个连接和某个已处于ESTABLISHED状态的连接有关系时，就被认为是RELATED，也就是说，一个连接想要是RELATED的，首先要有个ESTABLISHED的连接，这个ESTABLISHED连接再产生一个主连接之外的连接，这个新的连接就是RELATED。

INVALID：

INVALID状态说明数据包不能被识别属于哪个连接或没有任何状态。
