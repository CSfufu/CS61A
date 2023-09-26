def tree(label,branches = []):
    for branch in branches:
        assert is_tree(branch),"branch must be tree"
    return [label] + list(branches)

def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_tree(tree):
    if type(tree) != list or len(tree) < 1 :
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    return not branches(tree)

def count_leaves(tree):
    if is_leaf(tree):
        return 1
    else:
        return sum([count_leaves(b) for b in branches(tree)])

def make_withdraw(balance):
    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return "there is no enough money"
        balance -= amount
        return balance
    return withdraw

def a_then_b(a,b):
    yield from a
    yield from b

r = a_then_b([3,4,5],[4,6,4])

def countdown(n):
    if n > 0:
        yield n
        yield from countdown(n-1)

empty = 'empty'
def is_link(s):
    return s == empty or (len(s) == 2 and is_link(s[1]))
def link(first, rest):
    assert is_link(rest), 'rest must be a linklist'
    return [first, rest]
def first(s):
    assert is_link(s),'s must be a linklist'
    assert s != empty, 's can not be empty'
    return s[0]
def rest(s):
    assert  is_link(s), 's must be a linklist'
    assert s != empty, 's can not be empty'
    return s[1]
def link_len(s):
    len = 0
    while s != empty:
        s, len = rest(s), len + 1
    return len
def getiem_link(s, i):
    while i > 0:
        s, i = rest(s), i - 1
    return first(s)
def extend_list(s, t):
    assert is_link(s) and is_link(t),'s and t must be link lists'
    if s == empty:
        return t
    else:
        return link(first(s), extend_list(rest(s), t))
def apply_link(f, s):
    if s == empty:
        return s
    else:
        return link(f(first(s)),apply_link(f,rest(s)))
def keep_link(f, s):
    if s == empty:
        return s
    else:
        if f(first(s)):
            return link(first(s), keep_link(f, rest(s)))
        else:
            return keep_link(f, rest(s))
def seperator_link(s, seperator):
    if s == empty:
        return ''
    elif rest(s) == empty:
        return str(first(s))
    else:
        return str(first(s)) + seperator + seperator_link(rest(s), seperator)

