def regex_match(pattern: str, s: str) -> bool:
    # state: [type, data, o1, o2]; types: 0 char, 1 split, 2 eps, 3 match
    states = []

    def new(t, data=None, o1=-1, o2=-1):
        states.append([t, data, o1, o2])
        return len(states) - 1

    def patch(outs, target):
        for idx, slot in outs:
            states[idx][slot] = target

    def empty_frag():
        e = new(2)
        return (e, [(e, 2)])

    def concat(seq):
        if not seq:
            return empty_frag()
        cur = seq[0]
        for nxt in seq[1:]:
            patch(cur[1], nxt[0])
            cur = (cur[0], nxt[1])
        return cur

    def finish(frame):
        alts, seq = frame
        alts.append(concat(seq))
        cur = alts[0]
        for nxt in alts[1:]:
            sp = new(1, None, cur[0], nxt[0])
            cur = (sp, cur[1] + nxt[1])
        return cur

    def parse_class(i):
        # i is index after '['
        n = len(pattern)
        negate = False
        if i < n and pattern[i] == '^':
            negate = True
            i += 1
        chars = set()
        ranges = []
        first = True
        while True:
            if i >= n:
                raise ValueError("unclosed class")
            c = pattern[i]
            if c == ']' and not first:
                i += 1
                break
            first = False
            if c == '\\':
                if i + 1 >= n:
                    raise ValueError("trailing backslash")
                c = pattern[i + 1]
                i += 2
            else:
                i += 1
            # range?
            if i + 1 < n and pattern[i] == '-' and pattern[i + 1] != ']':
                j = i + 1
                e = pattern[j]
                if e == '\\':
                    if j + 1 >= n:
                        raise ValueError("trailing backslash")
                    e = pattern[j + 1]
                    j += 2
                else:
                    j += 1
                if e < c:
                    raise ValueError("bad range")
                ranges.append((c, e))
                i = j
            else:
                chars.add(c)
        return ('set', (negate, frozenset(chars), tuple(ranges))), i

    n = len(pattern)
    stack = [[[], []]]
    i = 0
    while i < n:
        c = pattern[i]
        frame = stack[-1]
        if c == '(':
            stack.append([[], []])
            i += 1
        elif c == ')':
            if len(stack) == 1:
                raise ValueError("unbalanced")
            fr = stack.pop()
            stack[-1][1].append(finish(fr))
            i += 1
        elif c == '|':
            frame[0].append(concat(frame[1]))
            frame[1] = []
            i += 1
        elif c in '*+?':
            seq = frame[1]
            if not seq:
                raise ValueError("nothing to repeat")
            f = seq[-1]
            if c == '*':
                sp = new(1, None, f[0], -1)
                patch(f[1], sp)
                seq[-1] = (sp, [(sp, 3)])
            elif c == '+':
                sp = new(1, None, f[0], -1)
                patch(f[1], sp)
                seq[-1] = (f[0], [(sp, 3)])
            else:
                sp = new(1, None, f[0], -1)
                seq[-1] = (sp, f[1] + [(sp, 3)])
            i += 1
        elif c == '.':
            st = new(0, ('any', None))
            frame[1].append((st, [(st, 2)]))
            i += 1
        elif c == '[':
            m, i = parse_class(i + 1)
            st = new(0, m)
            frame[1].append((st, [(st, 2)]))
        elif c == '\\':
            if i + 1 >= n:
                raise ValueError("trailing backslash")
            st = new(0, ('c', pattern[i + 1]))
            frame[1].append((st, [(st, 2)]))
            i += 2
        else:
            st = new(0, ('c', c))
            frame[1].append((st, [(st, 2)]))
            i += 1
    if len(stack) != 1:
        raise ValueError("unbalanced")
    start, outs = finish(stack[0])
    match_state = new(3)
    patch(outs, match_state)

    m_count = len(states)
    mark = [-1] * m_count

    def closure(starts, gen, result):
        stk = list(starts)
        while stk:
            x = stk.pop()
            if x < 0 or mark[x] == gen:
                continue
            mark[x] = gen
            t = states[x][0]
            if t == 1:
                stk.append(states[x][3])
                stk.append(states[x][2])
            elif t == 2:
                stk.append(states[x][2])
            else:
                result.append(x)

    def matches(data, ch):
        k = data[0]
        if k == 'c':
            return data[1] == ch
        if k == 'any':
            return True
        neg, chars, ranges = data[1]
        r = ch in chars
        if not r:
            for lo, hi in ranges:
                if lo <= ch <= hi:
                    r = True
                    break
        return r != neg

    cur = []
    gen = 0
    closure([start], gen, cur)
    for ch in s:
        gen += 1
        nxt = []
        targets = []
        for x in cur:
            st = states[x]
            if st[0] == 0 and matches(st[1], ch):
                targets.append(st[2])
        closure(targets, gen, nxt)
        cur = nxt
        if not cur:
            return False
    for x in cur:
        if states[x][0] == 3:
            return True
    return False
