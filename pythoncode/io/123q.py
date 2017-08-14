from math import sqrt

def jishu(n,y):
    print (n)
    if y == 1:
        return 0
    else:
        n=n+n
        y=y-1
    return jishu(n,y)

def jishu2(n,y):
    print (n)
    if y == 1:
        return 0
    else:
        n=n*n
        y=y-1
    return jishu2(n,y)

def kasibo(n):
    if n <= 1:
       return n
    else:
       return(kasibo(n-1) + kasibo(n-2))
    
def feibo(n):
    nL = [0,1]
    for i in range(n - 2):
        nL.append(nL[-2] + nL[-1])
    return nL

def sushu(x):
    l = 1 * int(1e+6)
    p = [True] * (l + 1)
    p[0] = p[1] = False
    for i in range(2, int(sqrt(l)+1)):
        if p[i]:
            for j in range(i * i, l+1, i):
                p[j] = False
    prime = [i for i in range(l+1) if p[i]]
    print (prime[x-1])
if __name__ == "__main__":
    n = int(input("?"))
    for i in range(n):
        print(feibo(i+1))
    sushu(10)
    jishu2(2,10)
