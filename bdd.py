import pdb

NONE = -1

class Node(object):
    def __init__(self, v, lo=NONE, hi=NONE):
        assert isinstance(v, int)
        assert isinstance(lo, int)
        assert isinstance(hi, int)
        self.v = v
        self.lo = lo
        self.hi = hi
        self.aux = 0

    def __repr__(self):
        return repr((self.v, self.lo, self.hi, self.aux))


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

# reduction
def reduction(root):
    global p, q, r, s, avail
    avail = new_node(0)
    # R1
    print 'R1'
    v_max = 3
    head = [NONE] * (v_max + 1)

    if root < 2: return # if root==true or root==false
    array[0].aux = array[1].aux = array[root].aux = NONE

    s = root
    while s != 0:
        print s
        p = s
        np = array[p]
        s = ~np.aux
        np.aux = head[np.v]
        head[np.v] = ~p
        if array[np.lo].aux >= 0:
            array[np.lo].aux = ~s
            s = np.lo
        if array[np.hi].aux >= 0:
            array[np.hi].aux = ~s
            s = np.hi


    print_array()
    print head

    # R2
    print 'R2'
    array[0].aux = array[1].aux = 0
    v = v_max - 1

    # R3
    while True:
        print 'R3'
        p = ~head[v]
        s = 0
        while p != 0:
            p2 = ~array[p].aux

            q = array[p].hi
            if array[q].lo < 0:
                array[p].hi = ~array[q].lo

            q = array[p].lo
            if array[q].lo < 0:
                array[p].lo = ~array[q].lo
                q = array[p].lo

            if q == array[p].hi:
                array[p].lo = ~q
                array[p].hi = avail
                array[p].aux = 0
                avail = p
            elif array[q].aux >= 0:
                array[p].aux = s
                s = ~q
                array[q].aux = ~p
            else:
                array[p].aux = array[~(array[q].aux)].aux
                array[~(array[q].aux)].aux = p

            p = p2

        print 'after R3'
        print avail
        print_array()

        # R4
        print 'R4'
        r = ~s
        s = 0
        while r >= 0:
            print r
            q = ~array[r].aux
            array[r].aux = 0
            if s == 0:
                s = q
            else:
                array[p].aux = q
            p = q
            while array[p].aux > 0:
                p = array[p].aux

            r = ~array[p].aux
        print_array()

        # R5
        print 'R5'
        p = s
        if p != 0:
            # not jumped to R9
            q = p
            R678()

        print_array()
        # R9
        print 'R9'
        while p != 0:
            # GOTO R6
            R678()
            print 'R9'

        if v > array[root].v:
            v -= 1
            # GOTO R3
            continue
        break

    if array[root].lo < 0:
        root = ~array[root].lo

    print_array()

def R678():
    global p, q, r, s, avail
    # R6
    print 'R6'
    s = array[p].lo
    assert p == q

    # R7
    while True:
        print 'R7'
        r = array[q].hi
        if array[r].aux >= 0:
            array[r].aux = ~q
        else:
            array[q].lo = array[r].aux
            array[q].hi = avail
            avail = q

        q = array[q].aux
        if q != 0 and array[q].lo == s:
            # GOTO R7
            continue
        break

    # R8
    while True:
        print 'R8'
        if array[p].lo >= 0:
            array[array[p].hi].aux = 0
        p = array[p].aux
        if p != q:
            # GOTO R8
            continue
        break


import dis

reduction(root)
