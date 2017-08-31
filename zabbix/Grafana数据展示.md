# Grafana数据展示

zabbix虽然有screen展示数据，但是图形类型很有限，并且不可以灵活的排列图形，所以我们借用Grafana进行数据展示。

安装请参考本博客地址的另一篇文章《自定义监控套件》

## 安装拓展组件

在命令行中输入以下命令添加组件

```bash
# 调用zabbix的组件
grafana-cli plugins install alexanderzobnin-zabbix-app
# 时钟组件，用于显示时间
grafana-cli plugins install grafana-clock-panel
# 饼图，用于对内存使用情况绘图
grafana-cli plugins install grafana-piechart-panel
```

更多组件的安装请参考https://grafana.com/plugins

## Grafana自定义Dashboard

第一步，进入的Dashboards界面

![](Grafana3.png)

第二步，创建自定义的监控页面

![](Grafana4.png)

![](Grafana5.png)

第三步，添加行

![](Grafana6.png)

第四步，添加图形

![](Grafana7.png)

![](Grafana8.png)

## Grafana调用zabbix

这里以走势图为例

第一步，添加一个走势图

![](Grafana9.png)

第二步，点击名称的位置，修改走势图属性

![](Grafana10.png)

第三步，修改走势图名称

![](Grafana11.png)

第四步，修改数据类型

![](Grafana12.png)

第五步，选着Zabbix的iterm

![](Grafana13.png)

第六步，修改图形属性

![](Grafana14.png)

第七步，选择需要显示统计数据

![](Grafana15.png)