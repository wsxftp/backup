# coding: utf-8

for i in range(101):
    if i % 3 == 0:
        if i % 5 == 0:
            print('BigKing')
        else:
            print('Big')
    elif i % 5 == 0:
        print('King')
    else:
        print('SmallKing')
