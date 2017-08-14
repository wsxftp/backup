# coding: utf-8

# 猜数字游戏
truenum = 8
x = 3
while True:
    if x == 0:
        print("you lose")
        break
    num = input("please input a number:")
    if num == truenum:
        print("you win")
        break
    elif int(num) < truenum:
        print("less than,You have {} more chance".format(x))
        x -= 1
    elif int(num) > truenum:
        print("more than,You have {} more chance".format(x))
        x -= 1