"""Long task: a booking calendar whose rules change over five rounds."""

R1 = '''
class Calendar:
    def __init__(self):
        self._b = []

    def book(self, start, end):
        if end <= start:
            raise ValueError("empty booking")
        if any(s < end and start < e for s, e in self._b):
            return False
        self._b.append((start, end))
        return True
'''

R2 = R1 + '''
    def cancel(self, start, end):
        if (start, end) in self._b:
            self._b.remove((start, end))
            return True
        return False

    def bookings(self):
        return sorted(self._b)
'''

R3 = '''
class Calendar:
    def __init__(self, horizon=10080):
        self.horizon = horizon
        self._series = []  # (start, end, every)

    def _occ(self, start, end, every):
        out = []
        while start < self.horizon:
            out.append((start, end))
            if not every:
                break
            start, end = start + every, end + every
        return out

    def _all(self):
        return [o for s in self._series for o in self._occ(*s)]

    def book(self, start, end, every=None):
        if end <= start:
            raise ValueError("empty booking")
        if every is not None and every < end - start:
            raise ValueError("occurrences would overlap")
        new = self._occ(start, end, every)
        taken = self._all()
        if any(s < e2 and s2 < e for s, e in new for s2, e2 in taken):
            return False
        self._series.append((start, end, every))
        return True

    def cancel(self, start, end):
        for x in self._series:
            if x[0] == start and x[1] == end:
                self._series.remove(x)
                return True
        return False

    def bookings(self):
        return sorted(self._all())
'''

R4 = R3 + '''
    def free(self, duration):
        t = 0
        for s, e in sorted(self._all()):
            if s - t >= duration:
                break
            t = max(t, e)
        return t if t + duration <= self.horizon else None
'''

R5 = R4.replace('''        self._series = []  # (start, end, every)''', '''        self._series = []  # (start, end, every, tentative)''').replace(
    '''    def _all(self):
        return [o for s in self._series for o in self._occ(*s)]''', '''    def _all(self, tentative=False):
        return [o for s in self._series if s[3] == tentative for o in self._occ(*s[:3])]''').replace(
    '''    def book(self, start, end, every=None):
        if end <= start:
            raise ValueError("empty booking")
        if every is not None and every < end - start:
            raise ValueError("occurrences would overlap")
        new = self._occ(start, end, every)
        taken = self._all()
        if any(s < e2 and s2 < e for s, e in new for s2, e2 in taken):
            return False
        self._series.append((start, end, every))
        return True''', '''    def book(self, start, end, every=None, tentative=False):
        if end <= start:
            raise ValueError("empty booking")
        if every is not None and every < end - start:
            raise ValueError("occurrences would overlap")
        new = self._occ(start, end, every)

        def hits(series):
            return any(s < e2 and s2 < e for s, e in new for s2, e2 in self._occ(*series[:3]))

        if any(hits(x) for x in self._series if not x[3]):
            return False
        if not tentative:
            self._series = [x for x in self._series if not (x[3] and hits(x))]
        self._series.append((start, end, every, tentative))
        return True''').replace(
    '''    def free(self, duration):''', '''    def tentative(self):
        return sorted(self._all(tentative=True))

    def free(self, duration):''')


def raises(f, *a, **k):
    try:
        f(*a, **k)
    except ValueError:
        return True
    return False


def t1_book_and_clash(m):
    c = m.Calendar()
    assert c.book(60, 120) and c.book(120, 180) and c.book(0, 60)
    assert not c.book(119, 121) and not c.book(30, 200) and not c.book(61, 62)


def t1_empty_refused(m):
    c = m.Calendar()
    assert raises(c.book, 10, 10) and raises(c.book, 10, 5)


def t2_cancel_and_list(m):
    c = m.Calendar()
    c.book(300, 360)
    c.book(0, 30)
    c.book(100, 200)
    assert c.bookings() == [(0, 30), (100, 200), (300, 360)]
    assert c.cancel(100, 200) and not c.cancel(100, 200) and not c.cancel(0, 31)
    assert c.book(150, 160)
    assert c.bookings() == [(0, 30), (150, 160), (300, 360)]


def t3_weekly(m):
    c = m.Calendar(horizon=100)
    assert c.book(10, 15, every=30)
    assert c.bookings() == [(10, 15), (40, 45), (70, 75)]
    assert not c.book(42, 43) and c.book(15, 40)
    assert not c.book(0, 2, every=25)  # its occurrence 25-27 falls inside 15-40
    assert c.book(90, 99) and c.book(100, 105)  # 100 is past the horizon: kept, but no occurrence listed
    assert c.bookings()[-1] == (90, 99)


def t3_cancel_series(m):
    c = m.Calendar(horizon=200)
    c.book(0, 10, every=50)
    assert not c.cancel(50, 60)
    assert c.cancel(0, 10) and c.bookings() == []


def t3_every_shorter_than_booking(m):
    c = m.Calendar()
    assert raises(c.book, 0, 10, every=5)


def t4_free(m):
    c = m.Calendar(horizon=100)
    assert c.free(5) == 0
    c.book(0, 10)
    c.book(20, 30)
    assert (c.free(10), c.free(11), c.free(70), c.free(71)) == (10, 30, 30, None)


def t4_free_with_series(m):
    c = m.Calendar(horizon=50)
    c.book(0, 5, every=10)
    assert (c.free(5), c.free(6)) == (5, None)


def t5_tentative(m):
    c = m.Calendar(horizon=100)
    assert c.book(10, 20, tentative=True) and c.book(15, 25, tentative=True)
    assert c.tentative() == [(10, 20), (15, 25)] and c.bookings() == []
    assert c.book(18, 30)
    assert c.tentative() == [] and c.bookings() == [(18, 30)]
    assert c.book(0, 5, tentative=True) and not c.book(25, 27, tentative=True)


def t5_free_ignores_tentative(m):
    c = m.Calendar(horizon=100)
    c.book(0, 50, tentative=True)
    c.book(60, 70)
    assert c.free(55) == 0 and c.free(61) is None


S1 = ('Write a Python module with `class Calendar` and `book(start: int, end: int) -> bool` (times in minutes; a '
      'booking covers the half-open interval [start, end)). Return False and change nothing if it overlaps an existing '
      'booking, else store it and return True. Raise ValueError if end <= start.')
S2 = ('Add `cancel(start, end) -> bool` (remove the booking with exactly that start and end; False if there is none) '
      'and `bookings() -> list[tuple[int, int]]` (all bookings, sorted by start).')
S3 = ('Add repeating bookings and a horizon. `Calendar(horizon: int = 10080)`; `book(start, end, every=None)`: with '
      '`every`, the booking repeats every `every` minutes (start, start+every, ...) for all occurrences that start '
      'before the horizon. A booking (single or repeating) succeeds only if none of its occurrences overlaps any '
      'existing occurrence. Raise ValueError if `every` is shorter than the booking. `bookings()` lists every '
      'occurrence starting before the horizon, sorted. `cancel(start, end)` cancels a whole series when given its '
      'first occurrence (only the first). A single booking starting at or after the horizon is accepted but has no '
      'listed occurrence.')
S4 = ('Add `free(duration: int) -> int | None`: the earliest start time t >= 0 such that [t, t+duration) overlaps no '
      'occurrence and t + duration <= horizon; None if there is none.')
S5 = ('Add tentative bookings: `book(..., tentative=True)`. A tentative booking may overlap other tentative '
      'bookings but not firm ones (then it is refused). A firm booking ignores tentative ones when checking for '
      'overlaps, and on success removes every tentative booking (whole series) that any of its occurrences '
      'overlaps. `bookings()` and `free()` consider firm bookings only; add `tentative()` listing tentative '
      'occurrences like `bookings()` does.')

ROUNDS = [
    {"spec": S1, "ref": R1, "tests": {"t1_book_and_clash": t1_book_and_clash, "t1_empty_refused": t1_empty_refused}},
    {"spec": S2, "ref": R2, "tests": {"t2_cancel_and_list": t2_cancel_and_list}},
    {"spec": S3, "ref": R3, "tests": {"t3_weekly": t3_weekly, "t3_cancel_series": t3_cancel_series,
                                     "t3_every_shorter_than_booking": t3_every_shorter_than_booking}},
    {"spec": S4, "ref": R4, "tests": {"t4_free": t4_free, "t4_free_with_series": t4_free_with_series}},
    {"spec": S5, "ref": R5, "tests": {"t5_tentative": t5_tentative, "t5_free_ignores_tentative": t5_free_ignores_tentative}},
]
