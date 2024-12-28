import math

# fsum will return the sum of any sequence/iterables
def mathModule(nos):
    print(math.fsum(nos))
    print(math.prod(nos))
    p=1
    for val in nos:
        p=p*val
    print(p)
    print(math.trunc(-1.009))
    print(math.sqrt(5.5))
    print(math.isqrt(5))
    print(math.remainder(5.9,3))
    print(math.isclose(2,2.5))
    

mathModule([40,4,5.645])

