"""Long task: a rate limiter that changes shape over five rounds."""

R1 = '''
class RateLimiter:
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.counts = {}

    def allow(self, now):
        w = int(now // self.window)
        if self.counts.get(w, 0) >= self.limit:
            return False
        self.counts[w] = self.counts.get(w, 0) + 1
        return True
'''

R2 = '''
class RateLimiter:
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.counts = {}

    def allow(self, key, now):
        w = (key, int(now // self.window))
        if self.counts.get(w, 0) >= self.limit:
            return False
        self.counts[w] = self.counts.get(w, 0) + 1
        return True
'''

R3 = '''
class RateLimiter:
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.calls = {}

    def _recent(self, key, now):
        xs = [t for t in self.calls.get(key, []) if t > now - self.window]
        self.calls[key] = xs
        return xs

    def allow(self, key, now):
        xs = self._recent(key, now)
        if len(xs) >= self.limit:
            return False
        xs.append(now)
        return True
'''

R4 = R3 + '''
    def retry_after(self, key, now):
        xs = self._recent(key, now)
        if len(xs) < self.limit:
            return 0.0
        return xs[len(xs) - self.limit] + self.window - now
'''

R5 = R4 + '''
    def __len__(self):
        for key in list(self.calls):
            self._recent(key, self.last)
        self.calls = {k: v for k, v in self.calls.items() if v}
        return len(self.calls)

    def _track(self, now):
        self.last = max(getattr(self, "last", now), now)
'''
R5 = R5.replace("    def allow(self, key, now):\n        xs = self._recent(key, now)",
                "    def allow(self, key, now):\n        self._track(now)\n        xs = self._recent(key, now)")
R5 = R5.replace("    def retry_after(self, key, now):\n        xs = self._recent(key, now)",
                "    def retry_after(self, key, now):\n        self._track(now)\n        xs = self._recent(key, now)")


def t1_fixed_window(m):
    r = m.RateLimiter(2, 10)
    assert [r.allow(t) for t in (0, 1, 2, 9.9, 10, 11, 12)] == [True, True, False, False, True, True, False]


def t1_refused_calls_do_not_count(m):
    r = m.RateLimiter(1, 5)
    assert [r.allow(t) for t in (0, 1, 2, 3, 5)] == [True, False, False, False, True]


def t2_keys_are_independent(m):
    r = m.RateLimiter(1, 10)
    assert [r.allow("a", 0), r.allow("b", 0), r.allow("a", 1), r.allow("b", 1)] == [True, True, False, False]


def t2_fixed_window_per_key(m):
    r = m.RateLimiter(2, 10)
    assert [r.allow("k", t) for t in (0, 9, 10, 11)] == [True, True, True, True]  # 10 opens a new window
    assert r.allow("j", 9.5)


def t3_sliding_window(m):
    r = m.RateLimiter(2, 10)
    # allowed calls in (now - 10, now]: at 10 the call at 0 has left the window, the one at 9 has not
    assert [r.allow("k", t) for t in (0, 9, 9.5, 10, 10.5, 19, 19.5)] == [True, True, False, True, False, True, False]


def t3_boundary_is_open(m):
    r = m.RateLimiter(1, 5)
    assert [r.allow("k", 0), r.allow("k", 4.999), r.allow("k", 5)] == [True, False, True]


def t4_retry_after(m):
    r = m.RateLimiter(2, 10)
    assert r.retry_after("k", 0) == 0
    r.allow("k", 1)
    r.allow("k", 3)
    assert abs(r.retry_after("k", 4) - 7) < 1e-9  # the call at 1 leaves at 11
    assert r.allow("k", 10.9) is False
    assert r.retry_after("k", 11) == 0
    assert r.allow("k", 11)
    assert abs(r.retry_after("k", 12) - 1) < 1e-9  # now the call at 3 must leave, at 13


def t4_retry_after_new_key(m):
    r = m.RateLimiter(3, 1)
    assert r.retry_after("never-seen", 100) == 0


def t5_len_counts_live_keys(m):
    r = m.RateLimiter(1, 10)
    r.allow("a", 0)
    r.allow("b", 5)
    assert len(r) == 2
    r.allow("c", 12)  # "a" (last call at 0) is idle now; "b" (5) is still within (2, 12]
    assert len(r) == 2
    r.allow("c", 30)
    assert len(r) == 1


def t5_refused_keys_not_tracked_twice(m):
    r = m.RateLimiter(1, 10)
    r.allow("a", 0)
    r.allow("a", 1)
    assert len(r) == 1


S1 = ('Write a Python module defining `class RateLimiter(limit: int, window: float)` with a method '
      '`allow(now: float) -> bool`. Time is split into fixed windows [0, window), [window, 2*window), and so on; '
      'in each window at most `limit` calls are allowed. `allow` returns True and counts the call if it is allowed, '
      'else returns False and does not count it. Calls arrive with non-decreasing `now`.')
S2 = ('Change: limits are now per key. The method becomes `allow(key: str, now: float) -> bool`; each key has its '
      'own count in each fixed window, independent of every other key. The old one-argument form is no longer needed.')
S3 = ('Change: use a sliding window instead of fixed windows. A call for a key at time `now` is allowed if fewer than '
      '`limit` allowed calls for that key happened in the half-open interval (now - window, now]. Refused calls still '
      'do not count.')
S4 = ('Add `retry_after(key: str, now: float) -> float`: 0 if a call for that key at `now` would be allowed, else how '
      'many seconds from `now` until the earliest moment a call would be allowed (given no other calls). It does not '
      'count as a call.')
S5 = ('Add `__len__`: the number of keys that have at least one allowed call inside the current window, where the '
      'current window is (latest - window, latest] for the latest `now` seen by any call to `allow` or '
      '`retry_after`. Keys with no calls in it must be forgotten so memory does not grow without bound.')

ROUNDS = [
    {"spec": S1, "ref": R1, "tests": {"t1_fixed_window": t1_fixed_window,
                                     "t1_refused_calls_do_not_count": t1_refused_calls_do_not_count}},
    {"spec": S2, "ref": R2, "tests": {"t2_keys_are_independent": t2_keys_are_independent,
                                     "t2_fixed_window_per_key": t2_fixed_window_per_key},
     "retires": ["t1_fixed_window", "t1_refused_calls_do_not_count"]},
    {"spec": S3, "ref": R3, "tests": {"t3_sliding_window": t3_sliding_window, "t3_boundary_is_open": t3_boundary_is_open},
     "retires": ["t2_fixed_window_per_key"]},
    {"spec": S4, "ref": R4, "tests": {"t4_retry_after": t4_retry_after, "t4_retry_after_new_key": t4_retry_after_new_key}},
    {"spec": S5, "ref": R5, "tests": {"t5_len_counts_live_keys": t5_len_counts_live_keys,
                                     "t5_refused_keys_not_tracked_twice": t5_refused_keys_not_tracked_twice}},
]
