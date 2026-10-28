# Thompson-style NFA simulation: linear in len(pattern) * len(s), no backtracking.


class _Node:
    __slots__ = ("kind", "arg", "out", "out2")

    def __init__(self, kind, arg=None, out=None, out2=None):
        self.kind = kind  # 'char', 'any', 'class', 'split', 'eps', 'match'
        self.arg = arg
        self.out = out
        self.out2 = out2


class _Frag:
    __slots__ = ("start", "outs")

    def __init__(self, start, outs):
        self.start = start
        self.outs = outs  # list of (node, attr) dangling pointers


def _patch(outs, target):
    for node, attr in outs:
        setattr(node, attr, target)


def _parse_class(pattern, i):
    # pattern[i] == '['; returns (predicate_tuple, next_index)
    n = len(pattern)
    j = i + 1
    negate = False
    if j < n and pattern[j] == "^":
        negate = True
        j += 1
    items = []  # list of (lo, hi) inclusive ranges
    first = True
    while True:
        if j >= n:
            raise ValueError("unclosed character class")
        c = pattern[j]
        if c == "]" and not first:
            j += 1
            break
        first = False
        if c == "\\":
            j += 1
            if j >= n:
                raise ValueError("trailing backslash")
            lo = pattern[j]
            j += 1
        else:
            lo = c
            j += 1
        # range?
        if j + 1 < n and pattern[j] == "-" and pattern[j + 1] != "]":
            j += 1
            c2 = pattern[j]
            if c2 == "\\":
                j += 1
                if j >= n:
                    raise ValueError("trailing backslash")
                hi = pattern[j]
                j += 1
            else:
                hi = c2
                j += 1
            if hi < lo:
                raise ValueError("range out of order")
            items.append((lo, hi))
        else:
            items.append((lo, lo))
    return ("class", negate, tuple(items)), j


def _parse(pattern):
    """Recursive-descent parser building an NFA fragment. Returns (frag)."""
    n = len(pattern)
    pos = [0]

    def peek():
        return pattern[pos[0]] if pos[0] < n else None

    def parse_alt(depth):
        frags = [parse_concat(depth)]
        while peek() == "|":
            pos[0] += 1
            frags.append(parse_concat(depth))
        if len(frags) == 1:
            return frags[0]
        # build split chain
        cur = frags[-1]
        for f in reversed(frags[:-1]):
            sp = _Node("split", out=f.start, out2=cur.start)
            cur = _Frag(sp, f.outs + cur.outs)
        return cur

    def parse_concat(depth):
        # returns fragment; empty concat -> epsilon
        frag = None
        while True:
            c = peek()
            if c is None or c == "|" or (c == ")" and depth > 0):
                break
            if c == ")":
                raise ValueError("unbalanced parenthesis")
            if c in "*+?":
                if frag is None:
                    raise ValueError("quantifier with nothing before it")
                # quantifier applies to previous atom (handled below), so here
                # it must follow an atom; atoms handle their own quantifiers.
                raise ValueError("quantifier with nothing before it")
            atom = parse_atom(depth)
            atom = parse_quant(atom)
            frag = atom if frag is None else _cat(frag, atom)
        if frag is None:
            e = _Node("eps")
            return _Frag(e, [(e, "out")])
        return frag

    def parse_quant(atom):
        while True:
            c = peek()
            if c == "*":
                pos[0] += 1
                sp = _Node("split", out=atom.start)
                _patch(atom.outs, sp)
                atom = _Frag(sp, [(sp, "out2")])
            elif c == "+":
                pos[0] += 1
                sp = _Node("split", out=atom.start)
                _patch(atom.outs, sp)
                atom = _Frag(atom.start, [(sp, "out2")])
            elif c == "?":
                pos[0] += 1
                sp = _Node("split", out=atom.start)
                atom = _Frag(sp, atom.outs + [(sp, "out2")])
            else:
                return atom

    def parse_atom(depth):
        c = pattern[pos[0]]
        if c == "(":
            pos[0] += 1
            inner = parse_alt(depth + 1)
            if peek() != ")":
                raise ValueError("unbalanced parenthesis")
            pos[0] += 1
            return inner
        if c == "[":
            spec, nxt = _parse_class(pattern, pos[0])
            pos[0] = nxt
            node = _Node("class", arg=spec)
            return _Frag(node, [(node, "out")])
        if c == ".":
            pos[0] += 1
            node = _Node("any")
            return _Frag(node, [(node, "out")])
        if c == "\\":
            pos[0] += 1
            if pos[0] >= n:
                raise ValueError("trailing backslash")
            ch = pattern[pos[0]]
            pos[0] += 1
            node = _Node("char", arg=ch)
            return _Frag(node, [(node, "out")])
        pos[0] += 1
        node = _Node("char", arg=c)
        return _Frag(node, [(node, "out")])

    def _cat(a, b):
        _patch(a.outs, b.start)
        return _Frag(a.start, b.outs)

    frag = parse_alt(0)
    if pos[0] != n:
        raise ValueError("unbalanced parenthesis")
    m = _Node("match")
    _patch(frag.outs, m)
    return frag.start


def _class_matches(spec, ch):
    _, negate, items = spec
    hit = False
    for lo, hi in items:
        if lo <= ch <= hi:
            hit = True
            break
    return hit != negate


def _closure(states, node, seen):
    stack = [node]
    while stack:
        nd = stack.pop()
        if nd is None or id(nd) in seen:
            continue
        seen.add(id(nd))
        if nd.kind == "split":
            stack.append(nd.out2)
            stack.append(nd.out)
        elif nd.kind == "eps":
            stack.append(nd.out)
        else:
            states.append(nd)


def regex_match(pattern: str, s: str) -> bool:
    start = _parse(pattern)
    cur = []
    _closure(cur, start, set())
    for ch in s:
        nxt = []
        seen = set()
        for nd in cur:
            k = nd.kind
            if k == "char":
                if nd.arg == ch:
                    _closure(nxt, nd.out, seen)
            elif k == "any":
                _closure(nxt, nd.out, seen)
            elif k == "class":
                if _class_matches(nd.arg, ch):
                    _closure(nxt, nd.out, seen)
        cur = nxt
        if not cur:
            return False
    for nd in cur:
        if nd.kind == "match":
            return True
    return False
