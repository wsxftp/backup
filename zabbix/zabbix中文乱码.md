
## 准备字体

字体我们可以使用Windows的字体库，存储路径为C:\Windows\Fonts

把‘楷体 常规’复制出来，复制到桌面会产生一个名为simkai.ttf的文件

zabbix保存字体的路径如下，把simkai.ttf文件保存到这个路径，其它字体我没有测试如果喜欢可以自己测试其它字体(其中微软雅黑不可以使用)
/usr/share/zabbix/fonts

## 配置zabbix3.0.9
vim /usr/share/zabbix/include/defines.inc.php

```bash
# 修改如下内容
define('ZBX_GRAPH_FONT_NAME',       'simkai'); // font file name
define('ZBX_FONT_NAME', 'simkai');
```

保存刷新网页即可，倘若不可以使用，请重启zabbix服务
