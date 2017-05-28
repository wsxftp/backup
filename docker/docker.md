# 容器技术

## namespace

各种namespace

## cgroup

cpu


# docker

docker domean
docker client
docker image
registory

两个重要的组件

link
AUFS

## docker默认是NAT桥

只能使用一种桥接方式，全局只有一个桥

## docker四种网络模型

第一种，私有型，虚拟机只具有回环接口

第二种，桥接型，和宿主主机在同一个网络中

第三种，联合型，和另一个主机共享命名空间，主要用于更改已经启动的虚拟主机

第四种，NAT型，


## docker状态查看命令

`docker inpect -f {{.State.Pid}} web`

cadvisor容器 分析容器运行时的状态，具有web界面展示
