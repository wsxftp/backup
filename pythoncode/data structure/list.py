# coding: utf-8

# 初始化
l1 = list()
l2 = []
l3 = [1, 2, 3]

# 查，下标/索引操作,如果索引超出范围将引发IndexError
print(l3[0])
print(l3[-1])
print(l3[-4])

# 修改，超出范围抛出IndexError
l3[2] = 5
# 追加
l1.append(12)
# 在某个元素之前增加一个元素，如果超出索引在最后或最前增加一个元素
l1.insert(0, 1)
# 追加一个列表
l1.extend([1, 2, 3])
l1.extend(l3)

# 删除最后一个元素，超出索引范围抛出IndexError
l1.pop()
# 删除第三个元素
l1.pop(3)
# 从前往后删除一个与值相同一个元素，remove如果值不存在则抛出ValueError
l1.remove(2)
# 删除第1个元素
del l1[0]
# 清除列表
l1.clear()

# 查找一个元素
l3.index(3)
# 统计元素个数
l3.count(3)
# 类别长度
len(l3)

# 原地排序
l3.sort()
# 倒排
l3.sort(reverse=True)
# 原地反转
l3.reverse()

# copy复制内存内容,l4 = l3这种是定义一个指针指向l3指针指向的内存
l4 = l3.copy()
