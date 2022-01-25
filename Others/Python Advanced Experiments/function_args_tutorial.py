import time

def foo(a, b, *, c, d):
    print(a,b,c,d)
    for arg in args:
        print(arg)
    for key in kwargs:
        print(key, kwargs[key])

foo(1, 2, c=3, d=4)