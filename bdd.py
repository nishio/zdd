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


class Macro(object):
    """
    Syntax suger to write array[x].aux as AUX[x]
    """
    def __init__(self, name):
        self.name = name

    def __setitem__(self, i, v):
        setattr(array[i], self.name, v)

    def __getitem__(self, i):
        return getattr(array[i], self.name)

AUX = Macro('aux')
V = Macro('v')
HI = Macro('hi')
LO = Macro('lo')


def new_node(*args):
    n = Node(*args)
    id = len(array)
    array.append(n)
    return id


def get(node_id, hilo):
    if hilo == 0:
        return LO[node_id]
    if hilo == 1:
        return HI[node_id]
    raise AssertionError('not here')


def set(node_id, hilo, v):
    if hilo == 0:
        LO[node_id] = v
        return v
    if hilo == 1:
        HI[node_id] = v
        return v
    raise AssertionError('not here')


def get_child(node, hilo, v):
    print 'get_child of %s, via %s' % (node, hilo)
    c = get(node, hilo)
    if c == NONE: # not added yet
        c = new_node(v)
        print 'not found, created %s' % c
        set(node, hilo, c)
    return c


def print_array():
    print ", ".join("%d:%s" % (i, v) for i, v in enumerate(array))


# reduction
def reduction(root):
    global p, q, r, s, avail
    avail = new_node(0)
    # R1
    # generate linked list of nodes which have same value
    # 'head' points the head of lists
    # links are represented by AUX. next(x) == ~AUX[x]
    print 'R1'
    head = [NONE] * v_max

    if root < 2: return # if root==true or root==false
    AUX[0] = AUX[1] = AUX[root] = NONE

    print_array()
    s = root
    while s != 0:
        print s
        p = s
        s = ~AUX[p]
        AUX[p] = head[V[p]]
        head[V[p]] = ~p
        if AUX[LO[p]] >= 0:
            AUX[LO[p]] = ~s
            s = LO[p]
        if AUX[HI[p]] >= 0:
            AUX[HI[p]] = ~s
            s = HI[p]


    print_array()
    print head

    # R2
    print 'R2'
    AUX[0] = AUX[1] = 0
    v = v_max - 1

    # R3
    while True:
        print 'R3'
        p = ~head[v]
        s = 0
        while p != 0:
            p2 = ~AUX[p]

            q = HI[p]
            if LO[q] < 0:
                print "R3-1"
                HI[p] = ~LO[q]

            q = LO[p]
            if LO[q] < 0:
                print "R3-2"
                LO[p] = ~LO[q]
                q = LO[p]

            if q == HI[p]:
                print "R3-3"
                LO[p] = ~q
                HI[p] = avail
                AUX[p] = 0
                avail = p
            elif AUX[q] >= 0:
                print "R3-4"
                AUX[p] = s
                s = ~q
                AUX[q] = ~p
            else:
                print "R3-5"
                AUX[p] = AUX[~(AUX[q])]
                AUX[~(AUX[q])] = p

            p = p2

        print 'after R3'
        print 'avail:', avail
        print 's:', s
        print_array()

        # R4
        print 'R4'
        r = ~s
        s = 0
        while r >= 0:
            print r
            q = ~AUX[r]
            AUX[r] = 0
            if s == 0:
                s = q
            else:
                AUX[p] = q
            p = q
            while AUX[p] > 0:
                p = AUX[p]

            r = ~AUX[p]

        print 'after R4'
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

        if v > V[root]:
            v -= 1
            # GOTO R3
            continue
        break

    if LO[root] < 0:
        root = ~LO[root]

    print_array()


def R678():
    global p, q, r, s, avail
    # R6
    print 'R6'
    s = LO[p]
    assert p == q

    # R7
    while True:
        print 'R7'
        r = HI[q]
        if AUX[r] >= 0:
            AUX[r] = ~q
        else:
            LO[q] = AUX[r]
            HI[q] = avail
            avail = q

        q = AUX[q]
        if q != 0 and LO[q] == s:
            # GOTO R7
            continue
        break

    # R8
    while True:
        print 'R8'
        if LO[p] >= 0:
            AUX[HI[p]] = 0
        p = AUX[p]
        if p != q:
            # GOTO R8
            continue
        break


# test TAOCP-ja P72 7.1.4 fig21

# generate BDD for median function
array = []
false = new_node(NONE, 0, 0) # == 0
true = new_node(NONE, 1, 1) # == 1
root = new_node(0) # == 2

def median(x, y, z):
    if x + y + z > 1:
        return true
    return false

v_max = 3
from all_bits import all_bits

def generate_bdt(f):
    for xs in all_bits([0] * v_max):
        c = root
        for i in range(v_max - 1):
            c = get_child(c, xs[i], i + 1)
        result = f(*xs)
        set(c, xs[-1], result)

generate_bdt(median)

assert repr(array) == '[(-1, 0, 0, 0), (-1, 1, 1, 0), (0, 3, 6, 0), (1, 4, 5, 0), (2, 0, 0, 0), (2, 0, 1, 0), (1, 7, 8, 0), (2, 0, 1, 0), (2, 1, 1, 0)]'
reduction(root)
assert repr(array) == '[(-1, 0, 0, 0), (-1, 1, 1, 0), (0, 3, 6, 0), (1, 0, 5, 0), (2, -1, 9, 0), (2, 0, 1, 0), (1, 5, 1, 0), (2, -6, 8, 0), (2, -2, 4, 0), (0, -1, -1, 0)]'
print 'ok.'

# TODO
# P77, kernel of C6
array = array[:2] # true and false
root = new_node(0) # == 2

def kernel(*xs):
    """
    if X is kernel, no 2 continuous 1s in X and no 3 continuous 0s in X.
    """
    for i in range(len(xs)):
        if xs[i - 1] == xs[i] == 1:
            return false

    for i in range(len(xs)):
        if xs[i - 2] == xs[i - 1] == xs[i] == 0:
            return false

    return true

v_max = 6
generate_bdt(kernel)
reduction(root)
print len(array)

def filtered_show():
    """
    show array after reduction
    filtered out unused node, sorted with their values
    """
    buf = []
    next = [root]
    while next:
        cur = next
        next = []
        for x in cur:
            if x == true or x == false: continue
            array[x].id = x
            buf.append(x)
            if HI[x] not in next:
                next.append(HI[x])
            if LO[x] not in next:
                next.append(LO[x])

    for v in range(v_max):
        print "Value:", v
        for x in buf:
            if V[x] == v:
                print ("%d:(LO: %d, HI: %d)" % (array[x].id, LO[x], HI[x])),
        print

    return buf


assert repr(filtered_show()) == '[2, 34, 3, 35, 19, 4, 43, 36, 20, 12, 21, 40, 13, 23, 14]'
