def a(rg):
    data = 0 
    for i in range(0, rg):
        if data >= 5:
            data += 1
            yield data
        else:
            data += 1
            yield 1


for x in a(10):
    print(x)
