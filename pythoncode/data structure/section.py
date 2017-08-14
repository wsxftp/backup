# coding: utf-8

l1 = []
# 显示第0到8个元素
l1[0:8]
l1[10:-1]


# copy函数可以使用section实现
def copy(lst):
    return lst[:]


# 带步长的切片
l1[2:9:2]
l1[10:3:-1]

# 反正列表
l1[::-1]
