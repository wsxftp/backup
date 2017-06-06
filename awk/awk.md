
# 基本用法：

```
awk [options] ‘program’ var=value file…
awk [options] -f programfile var=value file…
awk [options] 'BEGIN{ action;… } pattern{ action;… } END{action;… }' file ...
```

awk程序通常由：BEGIN语句块、能够使用模式匹配的通用语句块、END 语句块，共3部分组成

program 通常是被单引号或双引号中

选项：

```
-F 指明 输入时用到的字段分隔符
-v var=value: 自定义变量
```

# print 格式：print item1, item2, ...

示例：

```
awk '{print "hello,awk"}'
awk –F: '{print}' /etc/passwd
awk –F: ‘{print “wang”}’ /etc/passwd
awk –F: ‘{print $1}’ /etc/passwd
awk –F: ‘{print $0}’ /etc/passwd
awk –F: ‘{print $1”\t”$3}’ /etc/passwd
tail –3 /etc/fstab |awk ‘{print $2,$4}’
```

# 内置变量

FS ：输入字段分隔符， 默认为空白字符

```
awk -v FS=':' '{print $1,$3,$7}’ /etc/passwd
awk –F: '{print $1,$3,$7}’ /etc/passwd
```

OFS ：输出字段分隔符， 默认为空白字符

`awk -v FS=‘:’ -v OFS=‘:’ '{print $1,$3,$7}’ /etc/passwd`

RS ：输入记录分隔符， 指定输入时的换行符，原换行符仍有效

`awk -v RS=' ' ‘{print }’ /etc/passwd`

ORS ：输出记录分隔符， 输出时用指定符号代替换行符

`awk -v RS=' ' -v ORS='###'‘{print }’ /etc/passwd`

NF ：字段 数量
`awk -F： ： ‘{print NF}’ /etc/fstab`引用内置变量不用$

`awk -F: '{print $(NF-1)}' /etc/passwd`

NR ：行号

`awk '{print NR}' /etc/fstab ; awk END'{print NR}' /etc/fstab`

FNR ：各文件分别计数, 行号

`awk '{print FNR}' /etc/fstab /etc/inittab`

FILENAME ：当前文件名

`awk '{print FILENAME}’ /etc/fstab`

ARGC ：命令行参数的个数

```
awk '{print ARGC}’ /etc/fstab /etc/inittab
awk ‘BEGIN {print ARGC}’ /etc/fstab /etc/inittab
```

ARGV ：数组，保存的是命令行所给定的各参数

```
awk ‘BEGIN {print ARGV[0]}’ /etc/fstab
/etc/inittab
awk ‘BEGIN {print ARGV[1]}’ /etc/fstab
/etc/inittab
```

# 自定义变量
(1) -v var=value

变量名区分字符大小写

(2) 在program

# printf

格式化输出：`printf “FORMAT ”, item1, item2, ...`

```
(1) 必须指定FORMAT
(2) 不会自动换行，需要显式给出换行控制符，\n
(3) FORMAT中需要分别为后面每个item指定格式符
```

格式符：与item 一一对应

```
%c: 显示字符的ASCII码 码
%d, %i: 显示十进制整数
%e, %E: 显示科学 计数 法数值
%f ：显示为浮点数
%g, %G ：以科学计数法或浮点形式显示数值
%s ：显示字符串
%u ：无符号整数
%%: 显示% 自身
```

修饰符：

```
#[.#] ：第一个数字控制显示的宽度；第二个# 表示小数点后精度，%3.1f
-: 左对齐（默认） 右对齐） %-15s
+ ：显示数值的号 正负符号 %+d
11
```

printf 示例

```
awk -F: ‘{printf "%s",$1}’ /etc/passwd
awk -F: ‘{printf "%s\n",$1}’ /etc/passwd
awk -F: ‘{printf "Username: %s\n",$1}’ /etc/passwd
awk -F: ‘{printf “Username: %s,UID:%d\n",$1,$3}’
/etc/passwd
awk -F: ‘{printf "Username: %15s,UID:%d\n",$1,$3}’/etc/passwd
awk -F: ‘{printf "Username: %-15s,UID:%d\n",$1,$3}’/etc/passwd
```

#操作符

## 算术操作符：
x+y, x-y, x*y, x/y, x^y, x%y

-x: 转换为负数

+x: 转换 为数值

## 字符串操作符：没有符号的操作符，字符串连接

## 赋值操作符：

```
=, +=, -=, *=, /=, %=, ^=
++, --
```

## 比较操作符：
`>, >=, <, <=, !=, ==`

模式匹配符：

```
~ ：左边是否和 右边匹配包含
!~ ：是否不匹配
awk –F: '$0 ~ /root/{print $1}‘ /etc/passwd
awk '$0 !~ /root/‘ /etc/passwd
```

## 逻辑 操作符：与 与&& ，或||

# for 循环
语法：for(expr1;expr2;expr3) {statement;…}

常见用法：

`for(variable assignment;condition;iteration process){for-body}`

特殊用法：能够遍历数组中的元素；

语法`for(var in array) {for-body}`

示例：

`awk '/^[[:space:]]*linux16/{for(i=1;i<=NF;i++) {print
$i,length($i)}}' /etc/grub2.cfg`

# do-while 循环
语法：do {statement;…}while(condition)

意义：无论真假，至少执行一次循环体

示例：

`awk 'BEGIN{ total=0;i=0;do{total+=i;i++;}while(i<=100);print total}'`

思考：下面两语句有何不同？

```
awk 'BEGIN{i=0;print ++i,i}'
awk 'BEGIN{i=0;print i++,i}'
```

# while 循环
语法：while(condition){statement;…}

条件“真”，进入循环；条件“假”， 退出循环

使用场景：

对一行内的多个字段逐一类似处理时使用

对数组中的各元素逐一处理时使用

示例：

```
awk '/^[[:space:]]*linux16/{i=1;while(i<=NF){print $i,length($i); i++}}' /etc/grub2.cfg
awk '/^[[:space:]]*linux16/{i=1;while(i<=NF) {if(length($i)>=10){print $i,length($i)}; i++}}' /etc/grub2.cfg
```

# 控制语句if-else

语法：

```
if(condition) statement [else statement]
if(condition1){statement1}else if(condition2){statement2}
else{statement3}
```

使用场景：对awk 取得的整行或某个字段做条件判断

示例：

```
awk -F: '{if($3>=1000)print $1,$3}' /etc/passwd
awk -F: '{if($NF=="/bin/bash") print $1}' /etc/passwd
awk '{if(NF>5) print $0}' /etc/fstab
awk -F: '{if($3>=1000) {printf "Common user: %s\n",$1} else
{printf "root or Sysuser: %s\n",$1}}' /etc/passwd
awk -F: '{if($3>=1000) printf "Common user: %s\n",$1;
else printf "root or Sysuser: %s\n",$1}' /etc/passwd
df -h|awk -F% '/^\/dev/{print $1}'|awk '$NF>=80{print $1,$5}‘
awk 'BEGIN{ test=100;if(test>90){print "very good"}
else if(test>60){ print "good"}else{print "no pass"}}'
```

# awk 数组
关联数组：array[index-expression]

index-expression:

(1) 可使用任意字符串；字符串要使用双引号括起来

(2) 如果某数组元素事先不存在，在引用时，awk 会自动创建此元素，并将其值初始化为“空串”

若要判断数组中是否存在某元素，要使用“index in array”格 格

式进行遍历

示例：

```
weekdays[“mon”]="Monday“
awk 'BEGIN{weekdays["mon"]="Monday";
weekdays["tue"]="Tuesday";print weekdays["mon"]}‘
awk ‘!a[$0]++’ dupfile
```

若要遍历数组中的每个元素，要使用for 循环`for(var in array) {for-body}`

注意：var会遍历array的每个索引

示例：

```
awk 'BEGIN{weekdays["mon"]="Monday";weekdays["tue"]="Tuesday";for(i in weekdays) {print weekdays[i]}}‘
netstat -tan | awk '/^tcp\>/{state[$NF]++}END{for(i in state) { print i,state[i]}}'
awk '{ip[$1]++}END{for(i in ip) {print i,ip[i]}}'/var/log/httpd/access_log
```
