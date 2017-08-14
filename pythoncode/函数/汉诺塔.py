def move(n, a, b, c):
    if n == 1:
        print(a + ' --> ' + c)
    else:
        move(n - 1, a, c, b)
        print(a + ' --> ' + c)
        move(n - 1, b, a, c)


move(3, 'A', 'B', 'C')

lst = {x: x * x for x in range(0, 100)}
for x, y in lst.items():
    print(x, y)

i = 3
a = 'abcdabcd'
print(a[0:i])