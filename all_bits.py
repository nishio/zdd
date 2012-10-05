"""
>>> for x in all_bits([0, 0, 0]): print x
[0, 0, 0]
[0, 0, 1]
[0, 1, 0]
[0, 1, 1]
[1, 0, 0]
[1, 0, 1]
[1, 1, 0]
[1, 1, 1]
"""
def all_bits(xs, pos=0):
    if pos == len(xs):
        yield xs
    else:
        xs[pos] = 0
        for _ in all_bits(xs, pos + 1):
            yield xs
        xs[pos] = 1
        for _ in all_bits(xs, pos + 1):
            yield xs


def _test():
    import doctest
    doctest.testmod()


_test()
