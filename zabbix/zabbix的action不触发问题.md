在使用zabbix的action的时候，我遇到了一个问题：定义的trigger可以触发，然而定义的action却始终不触发
我使用的zabbix的版本是3.0.7-1.el7.x86_64，客户端也是如此。
然后就开始排错
### 1用户授权
把用户所在的组授予监控该主机组可读权限
### 2media管理
查看media的定义是否有问题
### 3user管理
这里主要是用户可以使用的media
### 4action的定义管理
这也是我犯错误的地方，在定义Operations的时候，Conditions我没有定义，以为默认值就可以触发，然并卵，然后添加的选项如下：
	Conditions Label	Name							Action
			   A	    Event acknowledged = Not Ack	Remove
这个定义取决于个人定义，可以在monitoring的events中查看ack列，如下
	Time				Description	Status		Severity	Duration	Ack		Actions
	2016-12-31 07:37:57	80			OK			High		17m 25s		No	
	2016-12-31 07:36:27	80			PROBLEM		High		1m 30s		No		2

