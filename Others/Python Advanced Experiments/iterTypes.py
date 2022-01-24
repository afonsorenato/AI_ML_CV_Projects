from itertools import product, permutations

def IterProduct():
    a = [1,2]
    b = [3]
    prod = product(a,b, repeat = 2)
    print(list(prod))

def IterPermutations():
    a = [1,2,3]
    perm = permutations(a)
    print(list(perm))


add10 = lambda x: x + 10
print(add10(5))

mult = lambda x, y: x * y
print(mult(2, 7))


def testLambda():

    points2D = {(1,2), (15,1), (5,-1), (10,4)}
    points2D_sorted = sorted(points2D)
    print(points2D)
    print(points2D_sorted)


testLambda()
IterProduct()
IterPermutations()