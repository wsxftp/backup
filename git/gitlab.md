
## gitlab的安装

```
wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-8.8.5-ce.1.el7.x86_64.rpm
yum install ./gitlab-ce-8.8.5-ce.1.el7.x86_64.rpm -y
gitlab-ctl reconfigure
gitlab-ctl start
```

打开/etc/gitlab/gitlab.rb文件，在external_url和ip之间加等号“=”，最好把域名改成ip(如果域名能访问的话可以不用改)

编辑/etc/gitlab/gitlab.rb
```bash
# 配置使用自己的域名，如果没有可以填写本机ip地址
external_url='http://oldking.uicp.io'
```

修改之后使用`gitlab-ctl reconfigure`重载一下配置文件

***如果不填写自己的域名，会导致web页面返回的地址为git@localhost.localdoman:oldking/guocai.git*** 填写之后的结果如图

![](gitlab3.png)

第一次登录，配置一下root的密码
![](gitlab2.png)


## 汉化

```
gitlab-ctl stop
wget https://github.com/larryli/gitlabhq/archive/8-8-zh.zip
unzip gitlabhq-8-8-zh.zip
\cp  /root/gitlabhq-8-8-zh/*  /opt/gitlab/embedded/service/gitlab-rails/  -rf
gitlab-ctl start
```
注意要多刷新几次浏览器或者ctrl+f5

![](gitlab.png)

![](gitlab1.png)
