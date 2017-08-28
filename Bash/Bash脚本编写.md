# Bash脚本编写

## if

字符串比较，由于bash是弱类型语言（不同类型变量可以比较），所以判断的内容就灵活的多

```bash
if [ "foo" = "foo" ]; then
    echo true
fi

if [ 3 = 3 ]; then
    echo true
fi
```

执行结果，命令执行结果会返回状态，执行成功为真失败为假，这里我就可以使用if

```bash
echo 1 >file1
echo 2 >file2
if ! diff -q file1 file2; then
    echo file1 file2 diff
else
    echo file1 file2 same
fi
```

文件测试

```bash
if [ -e myfile ]; then
    echo myfile exists
else
    touch myfile
    echo myfile created
fi
```

正则匹配

```bash
i=2
if [[ $i =~ 2 ]];then
    echo $i
else
    echo no
fi
```

***正则匹配特殊情况***正则表达式部分不要使用''把正则表达式引起来

## for

```bash
for i in $@;do
    echo $i
done
```

```bash
for((i=0;i<10;i++));do
    echo $i
done
```

Bash数组的使用方法

```bash
declare -a Unix=('Debian' 'Red hat' 'Red hat' 'Suse' 'Fedora')
for i in ${Unix[@]};do
    echo $i
done
```

Bash传参的使用方法

```bash
for i in $@;do
    echo $i
done
```

## while

```bash
i=3
while [ $i -gt 0 ];do
    echo $i
    let i--
done
```