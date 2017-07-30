
import argparse

## 注释信息
parser = argparse.ArgumentParser(description='This is a PyMOTW sample program')

## argparse内置6种动作可以在解析到一个参数时进行触发：

store 保存参数值，可能会先将参数值转换成另一个数据类型。若没有显式指定动作，则默认为该动作。

store_const 保存一个被定义为参数规格一部分的值，而不是一个来自参数解析而来的值。这通常用于实现非布尔值的命令行标记。

store_ture/store_false 保存相应的布尔值。这两个动作被用于实现布尔开关。

append 将值保存到一个列表中。若参数重复出现，则保存多个值。

append_const 将一个定义在参数规格中的值保存到一个列表中，要求数值不相同


```python
import argparse

parser = argparse.ArgumentParser(description='This is a PyMOTW sample program')
parser.add_argument('-a', action="store_true", default=False)
parser.add_argument('-b', action="store", dest="b")
parser.add_argument('-c', action="store", dest="c", type=int)

print(parser.parse_args(['-a', '-bval', '-c', '3']))
print(parser.parse_args(['-a', '-b', 'val', '-c', '3']))
print(parser.parse_args(['-a', '-b', 'val', '-c3']))
```

`parser.add_argument('-a', action="store_false", default=True,
        help='Turn A off')`-a存在为False，默认为True,default还可以为True、False、None

## 通过文件获取参数
```python
import argparse
from ConfigParser import ConfigParser
import shlex

parser = argparse./span>ArgumentParser(description='Short sample app')

parser.add_argument('-a', action="store_true", default=False)
parser.add_argument('-b', action="store", dest="b")
parser.add_argument('-c', action="store", dest="c", type=int)

config = ConfigParser()
config.read('argparse_witH_shlex.ini')
config_value = config.get('cli', 'options')
print 'Config: ', config_value

argument_list = shlex.split(config_value)
print 'Arg List:', argument_list

print 'Results:', parser.parse_args(argument_list)
```

## 共享解析器规则
```python
import argparse

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument('--user', action="store")
parser.add_argument('--password', action="store")
```

接下来，以父母解析器集创建另一个解析器：
```python
import argparse
import argparse_parent_base

parser = argparse.ArgumentParser(parents=[argparse_parent_base.parser])

parser.add_argument('--local-arg', action="store_true", default=False)

print parser.parse_args()
```

## 冲突的选项
```python
import argparse

parser = argparse.ArgumentParser(conflict_handler='resolve')

parser.add_argument('-a', action="store")
parser.add_argument('-b', action="store", help="Short alone")
parser.add_argument('--long-b', '-b', action="store", help="Long and short together")

print parser.parse_args(['-h'])
```
当我们想显示连个参数的时候可以把但参数的定义在多参数的后面
```python
import argparse

parser = argparse.ArgumentParser(conflict_handler='resolve')

parser.add_argument('-a', action="store")
parser.add_argument('--long-b', '-b', action="store", help="Long and short together")
parser.add_argument('-b', action="store", help="Short alone")

print parser.parse_args(['-h'])
```

## 参数群组
```python
import argparse

parser = argparse.ArgumentParser(description='Short sample app')

parser.add_argument('--optional', action="store_true", default=False)
parser.add_argument('positional', action="store")

print parser.parse_args()
```
另外一个示例
```python
import argparse

parser = argparser.ArgumentParser(add_help=False)

group = parser.add_argument_group('authentication')

group.add_argument('--user', action="store")
group.add_argument('--password', action="store")
```

```python
import argparse
import argparse_parent_with_group

parser = argparse.ArgumentParser(parents=[argparse_parent_with_group.parser])

parser.add_argument('--local-arg', action="store_true", default=False)

print parser.parse_args()
```

## 互斥选项
```python
import argparse

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument('-a', action='store_true')
group.add_argument('-b', action="store_true")

print parser.parse_args()
```

## 嵌套解析器
```python
import argparse

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help='commands')

# A list command
list_parser = subparsers.add_parser('list', help='List contents')
list_parser.add_argument('dirname', action='store', help='Directory to list')

# A create command
create_parser = subparsers.add_parser('create', help='Create a directory')
create_parser.add_argument('dirname', action='store', help='New directory to create')
create_parser.add_argument('--read-only', default=False, action='store_true',
        help='Set permissions to prevent writing to the directory')

# A delete command
delete_parser = subparsers.add_parser('delete', help='Remove a directory')
delete_parser.add_argument('dirname', action='store', help='The directory to remove')
delete_parser.add_argument('--recursive', '-r', default=False, action='store_true',
        help='Remove the contents of the directory, too')

print parser.parse_args()
```

## 可变形参列表
```
值  含义
N   参数的绝对个数（例如：3）
?   0或1个参数
*   0或所有参数
+   所有，并且至少一个参数
```
```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--three', nargs=3)
parser.add_argument('--optional', nargs='?')
parser.add_argument('--all', nargs='*', dest='all')
parser.add_argument('--one-or-more', nargs='+')

print parser.parse_args()
```
$ python argparse_nargs.py -h

## 参数类型
argparse将所有参数值都看作是字符串，除非你告诉它将字符串转换成另一种数据类型。add_argument()的type参数以一个转换函数作为值，被ArgumentParser用来将参数值从一个字符串转换成另一种数据类型。
```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-i', type=int)
parser.add_argument('-f', type=float)
parser.add_argument('--file', type=file)

try:
    print parser.parse_args()
except IOError, msg:
    parser.error(str(msg))
```

## 文件参数
虽然文件对象可以单个字符串参数值来实例化，但并不允许你指定访问模式。FileType让你能够更加灵活地指定某个参数应该是个文件，包括其访问模式和缓冲区大小。
```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-i', metavar='in-file', type=argparse.FileType('rt'))
parser.add_argument('-o', metavar='out-file', type=argparse.FileType('wt'))

try:
    results = parser.parse_args()
    print 'Input file:', results.i
    print 'Output file:', results.o
except IOError, msg:
    parser.error(str(msg))
```

## 自定义动作

除了前面描述的内置动作之外，你也可以提供一个实现了Action API的对象来自定义动作。作为action传递给add_argument()的对象应接受描述所定义形参的实参，并返回一个可调用对象，作为parser的实参来处理形参，namespace存放解析的结果、参数值，以及触发动作的option_string。

argparse提供了一个Action类作为要定义的新动作的基类。构造方法是处理参数定义的，所以你只要在子类中覆盖call()。
```python
import argparse

class CustomAction(argparse.Action):
    def __init__(self,
            option_strings,
            dest,
            nargs=None,
            const=None,
            default=None,
            type=None,
            choices=None,
            required=False,
            help=None,
            metavar=None):
        argparse.Action.__init__(self,
                option_strings=option_strings,
                dest=dest,
                nargs=nargs,
                const=const,
                default=default,
                type=type,
                choices=choices,
                required=required,
                help=help,
                metavar=metavar)
        print
        print 'Initializing CustomAction'
        for name,value in sorted(locals().items()):
            if name == 'self' or value is None:
                continue
            print '  %s = %r' % (name, value)
        return

    def __call__(self, parser, namespace, values, option_string=None):
        print
        print 'Processing CustomAction for "%s"' % self.dest
        print '  parser = %s' % id(parser)
        print '  values = %r' % values
        print '  option_string = %r' % option_string

        # Do some arbitrary processing of the input values
        if isinstance(values, list):
            values = [ v.upper() for v in values ]
        else:
            values = values.upper()
        # Save the results in the namespace using the destination
        # variable given to our constructor.
        setattr(namespace, self.dest, values)

parser = argparse.ArgumentParser()

parser.add_argument('-a', action=CustomAction)
parser.add_argument('-m', nargs='*', action=CustomAction)
parser.add_argument('positional', action=CustomAction)

results = parser.parse_args(['-a', 'value', '-m' 'multi-value', 'positional-value'])
print
print results
```
values的类型取决于nargs的值。如果该参数允许多个值，则values会是一个列表，即使其仅包含一个列表项。

option_string的值也取决于原有的参数规范。对于位置相关的、必需的参数，option_string始终为None。
