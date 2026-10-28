def regex_match(pattern: str, s: str) -> bool:
    # Parse into an NFA (Thompson construction), then simulate it over s.
    # Simulation keeps a set of states, so time is O(len(pattern) * len(s)).

    class _Node:
        __slots__ = ("kind", "a", "b", "out", "out2", "pred")
        # kind: 'eps' (epsilon, uses out/out2), 'char' (uses pred, out), 'match'

    def _char_pred(kind, data):
        if kind == "any":
            return lambda c: True
        if kind == "lit":
            return lambda c, ch=data: c == ch
        # class: data = (negated, items) where items is list of (lo, hi)
        negated, ranges = data
        def pred(c, negated=negated, ranges=ranges):
            hit = False
            for lo, hi in ranges:
                if lo <= c <= hi:
                    hit = True
                    break
            return hit != negated
        return pred

    # Parser produces a fragment-building AST first, then compiles.
    # AST nodes: ('empty',), ('char', pred), ('cat', l, r), ('alt', l, r),
    #            ('star', n), ('plus', n), ('opt', n)
    n = len(pattern)
    pos = 0

    def peek():
        return pattern[pos] if pos < n else None

    def parse_alt():
        nonlocal pos
        left = parse_cat()
        while peek() == "|":
            pos += 1
            right = parse_cat()
            left = ("alt", left, right)
        return left

    def parse_cat():
        nonlocal pos
        items = []
        while True:
            c = peek()
            if c is None or c == "|" or c == ")":
                break
            if c in "*+?":
                raise ValueError("quantifier with nothing before it")
            atom = parse_atom()
            # postfix quantifiers, possibly stacked
            while peek() in ("*", "+", "?"):
                q = peek()
                pos += 1
                if q == "*":
                    atom = ("star", atom)
                elif q == "+":
                    atom = ("plus", atom)
                else:
                    atom = ("opt", atom)
            items.append(atom)
        if not items:
            return ("empty",)
        node = items[0]
        for it in items[1:]:
            node = ("cat", node, it)
        return node

    def parse_atom():
        nonlocal pos
        c = pattern[pos]
        if c == "(":
            pos += 1
            inner = parse_alt()
            if peek() != ")":
                raise ValueError("unbalanced parentheses")
            pos += 1
            return inner
        if c == ")":
            raise ValueError("unbalanced parentheses")
        if c == ".":
            pos += 1
            return ("char", _char_pred("any", None))
        if c == "[":
            return parse_class()
        if c == "\\":
            if pos + 1 >= n:
                raise ValueError("trailing backslash")
            lit = pattern[pos + 1]
            pos += 2
            return ("char", _char_pred("lit", lit))
        pos += 1
        return ("char", _char_pred("lit", c))

    def parse_class():
        nonlocal pos
        pos += 1  # skip '['
        negated = False
        if peek() == "^":
            negated = True
            pos += 1
        ranges = []
        first = True
        while True:
            if pos >= n:
                raise ValueError("unclosed character class")
            c = pattern[pos]
            if c == "]" and not first:
                pos += 1
                break
            first = False
            if c == "\\":
                if pos + 1 >= n:
                    raise ValueError("trailing backslash")
                lo = pattern[pos + 1]
                pos += 2
            else:
                lo = c
                pos += 1
            # range?
            if (pos + 1 < n and pattern[pos] == "-"
                    and pattern[pos + 1] != "]"):
                pos += 1  # skip '-'
                if pattern[pos] == "\\":
                    if pos + 1 >= n:
                        raise ValueError("trailing backslash")
                    hi = pattern[pos + 1]
                    pos += 2
                else:
                    hi = pattern[pos]
                    pos += 1
                if hi < lo:
                    raise ValueError("bad range")
                ranges.append((lo, hi))
            else:
                ranges.append((lo, lo))
        return ("char", _char_pred("class", (negated, ranges)))

    ast = parse_alt()
    if pos != n:
        # leftover: must be an unmatched ')'
        raise ValueError("unbalanced parentheses")

    # Compile AST to NFA.
    def compile_ast(node, nxt):
        """Return the start state for node that continues to state nxt."""
        kind = node[0]
        if kind == "empty":
            return nxt
        if kind == "char":
            st = _Node()
            st.kind = "char"
            st.pred = node[1]
            st.out = nxt
            st.out2 = None
            return st
        if kind == "cat":
            return compile_ast(node[1], compile_ast(node[2], nxt))
        if kind == "alt":
            st = _Node()
            st.kind = "eps"
            st.out = compile_ast(node[1], nxt)
            st.out2 = compile_ast(node[2], nxt)
            return st
        if kind == "star":
            st = _Node()
            st.kind = "eps"
            st.out2 = nxt
            body = compile_ast(node[1], st)
            st.out = body
            return st
        if kind == "plus":
            st = _Node()
            st.kind = "eps"
            st.out2 = nxt
            body = compile_ast(node[1], st)
            st.out = body
            return body
        if kind == "opt":
            st = _Node()
            st.kind = "eps"
            st.out = compile_ast(node[1], nxt)
            st.out2 = nxt
            return st
        raise ValueError("unknown node")

    accept = _Node()
    accept.kind = "match"
    accept.out = None
    accept.out2 = None
    start = compile_ast(ast, accept)

    def closure(states):
        stack = list(states)
        seen = set(states)
        while stack:
            st = stack.pop()
            if st.kind == "eps":
                for nx in (st.out, st.out2):
                    if nx is not None and id(nx) not in seen:
                        seen.add(id(nx))
                        stack.append(nx)
        return seen

    # Map id -> node for lookup during stepping.
    current = {id(start): start}
    current = {k: v for k, v in _expand(current, closure).items()}
    for ch in s:
        nxt = {}
        for st in current.values():
            if st.kind == "char" and st.pred(ch):
                nxt[id(st.out)] = st.out
        if not nxt:
            return False
        current = _expand(nxt, closure)
    return any(st.kind == "match" for st in current.values())


def _expand(nodes, closure):
    ids = closure(list(nodes.values()))
    result = {}
    stack = list(nodes.values())
    # Collect every node reachable by epsilon closure from the given nodes.
    all_nodes = {}
    frontier = list(nodes.values())
    while frontier:
        st = frontier.pop()
        if id(st) in all_nodes:
            continue
        all_nodes[id(st)] = st
        if st.kind == "eps":
            for nx in (st.out, st.out2):
                if nx is not None:
                    frontier.append(nx)
    return all_nodes
