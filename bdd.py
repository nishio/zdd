NONE = -1

class Node(object):
    def __init__(self, v, lo=NONE, hi=NONE):
        assert isinstance(v, int)
        assert isinstance(lo, int)
        assert isinstance(hi, int)
        self.v = v
        self.lo = lo
        self.hi = hi

    def __repr__(self):
        return repr((self.v, self.lo, self.hi))


# generate BDD for median function
array = []
def new_node(*args):
    n = Node(*args)
    id = len(array)
    array.append(n)
    return id


def get(node_id, hilo):
    if hilo == 0:
        return array[node_id].lo
    if hilo == 1:
        return array[node_id].hi
    raise AssertionError('not here')

def set(node_id, hilo, v):
    if hilo == 0:
        array[node_id].lo = v
        return v
    if hilo == 1:
        array[node_id].hi = v
        return v
    raise AssertionError('not here')

false = new_node(NONE, 0, 0)
true = new_node(NONE, 1, 1)

root = new_node(0)

def get_child(node, hilo, v):
    print 'get_child of %s, via %s' % (node, hilo)
    c = get(node, hilo)
    if c == NONE: # not added yet
        c = new_node(v)
        print 'not found, created %s' % c
        set(node, hilo, c)
    return c

for x in [0, 1]:
    c = get_child(root, x, 1)
    for y in [0, 1]:
        c2 = get_child(c, y, 2)
        for z in [0, 1]:
            if x + y + z > 1:
                result = true
            else:
                result = false
            set(c2, z, result)

def print_array():
    print ", ".join("%d:%s" % (i, v) for i, v in enumerate(array))

print_array()
