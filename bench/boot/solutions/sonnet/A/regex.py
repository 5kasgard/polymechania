```python
def regex_match(pattern: str, s: str) -> bool:
    CHR, ANY, CLS, SPLIT, EPS, MATCH = 0, 1, 2, 3, 4, 5
    kind = []
    data = []
    o1 = []
    o2 = []

    def new(k, d=None):
        kind.append(k)
        data.append(d)
        o1.append(-1)
        o2.append(-1)
        return len(kind) - 1

    def patch(outs, target):
        for st, slot in outs:
            if slot == 0:
                o1[st] = target
            else:
                o2[st] = target

    def atom(k, d=None):
        st = new(k, d)
        return (st, [(st, 0)])

    def empty():
        return atom(EPS)

    def cat(f1, f2):
        patch(f1[1], f2[0])
        return (f1[0], f2[1])

    def star(f):
        sp = new(SPLIT)
        o1[sp] = f[0]
        patch(f[1], sp)
        return (sp, [(sp, 1)])

    def plus(f):
        sp = new(SPLIT)
        o1[sp] = f[0]
        patch(f[1], sp)
        return (f[0], [(sp, 1)])

    def quest(f):
        sp = new(SPLIT)
        o1[sp] = f[0]
        return (sp, f[1] + [(sp, 1)])

    def alt(f1, f2):
        sp = new(SPLIT)
        o1[sp] = f1[0]
        o2[sp] = f2[0]
        return (sp, f1[1] + f2[1])

    p = pattern
    n = len(p)

    def parse_class(i):
        neg = False
        if i < n and p[i] == '^':
            neg = True
            i += 1
        singles = set()
        ranges = []
        first = True
        while True:
            if i >= n:
                raise ValueError("unclosed class")
            c = p[i]
            if c == ']' and not first:
                i += 1
                break
            first = False
            if c == '\\':
                i += 1
                if i >= n:
                    raise ValueError("trailing backslash")
                c = p[i]
            i += 1
            if i + 1 < n and p[i] == '-' and p[i + 1] != ']':
                i += 1
                e = p[i]
                if e == '\\':
                    i += 1
                    if i >= n:
                        raise ValueError("trailing backslash")
                    e = p[i]
                i += 1
                if e < c:
                    raise ValueError("bad range")
                ranges.append((c, e))
            else:
                singles.add(c)
        return (neg, singles, ranges), i

    # frames: [alts, cat, last]
    stack = [[[], None, None]]

    def commit(fr):
        if fr[2] is not None:
            fr[1] = fr[2] if fr[1] is None else cat(fr[1], fr[2])
            fr[2] = None

    def finish(fr):
        commit(fr)
        cur = fr[1] if fr[1] is not None else empty()
        fr[0].append(cur)
        res = fr[0][0]
        for f in fr[0][1:]:
            res = alt(res, f)
        return res

    def add_atom(fr, f):
        commit(fr)
        fr[2] = f

    i = 0
    while i < n:
        c = p[i]
        fr = stack[-1]
        if c == '(':
            stack.append([[], None, None])
            i += 1
        elif c == ')':
            if len(stack) == 1:
                raise ValueError("unbalanced parentheses")
            f = finish(stack.pop())
            add_atom(stack[-1], f)
            i += 1
        elif c == '|':
            commit(fr)
            fr[0].append(fr[1] if fr[1] is not None else empty())
            fr[1] = None
            i += 1
        elif c in '*+?':
            if fr[2] is None:
                raise ValueError("nothing to repeat")
            if c == '*':
                fr[2] = star(fr[2])
            elif c == '+':
                fr[2] = plus(fr[2])
            else:
                fr[2] = quest(fr[2])
            i +=