"""Long task: an inventory whose stock rules change over five rounds."""

R1 = '''
class Inventory:
    def __init__(self):
        self._stock = {}

    def add(self, sku, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._stock[sku] = self._stock.get(sku, 0) + qty

    def remove(self, sku, qty):
        if qty <= 0 or self._stock.get(sku, 0) < qty:
            raise ValueError("cannot remove")
        self._stock[sku] -= qty

    def stock(self, sku):
        return self._stock.get(sku, 0)
'''

R2 = '''
class Inventory:
    def __init__(self):
        self._stock = {}
        self._hist = []

    def add(self, sku, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._stock[sku] = self._stock.get(sku, 0) + qty
        self._hist.append((sku, qty))

    def remove(self, sku, qty):
        if qty <= 0 or self._stock.get(sku, 0) < qty:
            raise ValueError("cannot remove")
        self._stock[sku] = self._stock.get(sku, 0) - qty
        self._hist.append((sku, -qty))

    def stock(self, sku):
        return self._stock.get(sku, 0)

    def history(self, sku):
        return [q for s, q in self._hist if s == sku]

    def undo(self):
        if not self._hist:
            raise ValueError("nothing to undo")
        sku, q = self._hist.pop()
        self._stock[sku] -= q
'''

R3 = '''
class Inventory:
    def __init__(self):
        self._stock = {}
        self._hist = []
        self._res = {}
        self._next = 1

    def add(self, sku, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._stock[sku] = self._stock.get(sku, 0) + qty
        self._hist.append((sku, qty))

    def remove(self, sku, qty):
        if qty <= 0 or self.available(sku) < qty:
            raise ValueError("cannot remove")
        self._stock[sku] = self._stock.get(sku, 0) - qty
        self._hist.append((sku, -qty))

    def stock(self, sku):
        return self._stock.get(sku, 0)

    def reserved(self, sku):
        return sum(q for s, q in self._res.values() if s == sku)

    def available(self, sku):
        return self.stock(sku) - self.reserved(sku)

    def history(self, sku):
        return [q for s, q in self._hist if s == sku]

    def undo(self):
        if not self._hist:
            raise ValueError("nothing to undo")
        sku, q = self._hist[-1]
        if q > 0 and self.stock(sku) - q < self.reserved(sku):
            raise ValueError("undo would break a reservation")
        self._hist.pop()
        self._stock[sku] -= q

    def reserve(self, sku, qty):
        if qty <= 0 or self.available(sku) < qty:
            raise ValueError("cannot reserve")
        rid = self._next
        self._next += 1
        self._res[rid] = (sku, qty)
        return rid

    def release(self, rid):
        if rid not in self._res:
            raise KeyError(rid)
        del self._res[rid]

    def fulfil(self, rid):
        if rid not in self._res:
            raise KeyError(rid)
        sku, qty = self._res.pop(rid)
        self._stock[sku] = self._stock.get(sku, 0) - qty
        self._hist.append((sku, -qty))
'''

R4 = R3.replace('''    def remove(self, sku, qty):
        if qty <= 0 or self.available(sku) < qty:
            raise ValueError("cannot remove")''', '''    def remove(self, sku, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")''').replace('''        if q > 0 and self.stock(sku) - q < self.reserved(sku):
            raise ValueError("undo would break a reservation")
''', '')

R5 = R4.replace("class Inventory:", "import json\n\n\nclass Inventory:") + '''
    def snapshot(self):
        return json.dumps({"stock": self._stock, "history": self._hist,
                           "reservations": {str(k): v for k, v in self._res.items()}, "next": self._next})

    @classmethod
    def restore(cls, text):
        d = json.loads(text)
        inv = cls()
        inv._stock = dict(d["stock"])
        inv._hist = [tuple(x) for x in d["history"]]
        inv._res = {int(k): tuple(v) for k, v in d["reservations"].items()}
        inv._next = d["next"]
        return inv
'''


def raises(f, *a, exc=ValueError):
    try:
        f(*a)
    except exc:
        return True
    return False


def t1_add_remove(m):
    i = m.Inventory()
    i.add("a", 5)
    i.add("a", 2)
    i.remove("a", 3)
    assert (i.stock("a"), i.stock("zzz")) == (4, 0)


def t1_bad_quantities(m):
    i = m.Inventory()
    assert raises(i.add, "a", 0) and raises(i.add, "a", -1)
    i.add("a", 1)
    assert raises(i.remove, "a", 0)


def t1_no_negative_stock(m):
    i = m.Inventory()
    i.add("a", 1)
    assert raises(i.remove, "a", 2) and raises(i.remove, "b", 1)
    assert i.stock("a") == 1


def t2_history(m):
    i = m.Inventory()
    i.add("a", 5)
    i.add("b", 1)
    i.remove("a", 2)
    try:
        i.add("a", 0)
    except ValueError:
        pass
    assert i.history("a") == [5, -2] and i.history("b") == [1] and i.history("c") == []


def t2_undo(m):
    i = m.Inventory()
    assert raises(i.undo)
    i.add("a", 5)
    i.remove("a", 2)
    i.undo()
    assert i.stock("a") == 5 and i.history("a") == [5]
    i.undo()
    assert i.stock("a") == 0 and i.history("a") == []


def t3_reserve(m):
    i = m.Inventory()
    i.add("a", 5)
    r1 = i.reserve("a", 3)
    r2 = i.reserve("a", 2)
    assert (r1, r2) == (1, 2)
    assert (i.stock("a"), i.available("a")) == (5, 0)
    assert raises(i.reserve, "a", 1)
    i.release(r1)
    assert i.available("a") == 3
    i.fulfil(r2)
    assert (i.stock("a"), i.available("a")) == (3, 3)
    assert raises(i.release, r2, exc=KeyError) and raises(i.fulfil, 99, exc=KeyError)


def t3_remove_respects_reservations(m):
    i = m.Inventory()
    i.add("a", 5)
    i.reserve("a", 4)
    assert raises(i.remove, "a", 2)
    i.remove("a", 1)
    assert i.available("a") == 0


def t3_fulfil_in_history(m):
    i = m.Inventory()
    i.add("a", 5)
    r = i.reserve("a", 2)
    i.fulfil(r)
    assert i.history("a") == [5, -2]


def t3_undo_keeps_reservations(m):
    i = m.Inventory()
    i.add("a", 5)
    i.reserve("a", 4)
    assert raises(i.undo)
    assert i.stock("a") == 5 and i.history("a") == [5]


def t4_backorders(m):
    i = m.Inventory()
    i.add("a", 1)
    i.remove("a", 3)
    assert (i.stock("a"), i.available("a")) == (-2, -2)
    i.remove("new", 1)
    assert i.stock("new") == -1
    assert raises(i.remove, "a", 0)


def t4_reserve_still_needs_stock(m):
    i = m.Inventory()
    i.add("a", 2)
    i.reserve("a", 2)
    i.remove("a", 1)  # allowed now: available goes to -1
    assert i.available("a") == -1
    assert raises(i.reserve, "a", 1)


def t5_round_trip(m):
    i = m.Inventory()
    i.add("a", 5)
    i.add("b", 2)
    r = i.reserve("a", 2)
    i.remove("b", 3)
    j = m.Inventory.restore(i.snapshot())
    assert isinstance(i.snapshot(), str)
    assert [j.stock(s) for s in "abc"] == [5, -1, 0] and j.available("a") == 3
    assert j.history("b") == [2, -3]
    j.fulfil(r)
    assert j.stock("a") == 3
    assert j.reserve("a", 1) == 2  # ids continue


def t5_restored_undo(m):
    i = m.Inventory()
    i.add("a", 4)
    i.remove("a", 1)
    j = m.Inventory.restore(i.snapshot())
    j.undo()
    assert j.stock("a") == 4 and i.stock("a") == 3  # independent copies


S1 = ('Write a Python module with `class Inventory` having `add(sku: str, qty: int)`, `remove(sku: str, qty: int)` and '
      '`stock(sku: str) -> int` (0 for an unknown sku). Raise ValueError if qty is not positive, and if a remove would '
      'take stock below zero (nothing changes then).')
S2 = ('Add `history(sku) -> list[int]`: the signed quantity of each successful add (+) and remove (-) for that sku, '
      'in order; and `undo()`: revert the most recent successful add or remove of any sku, also removing it from '
      'history; raise ValueError if there is nothing to undo.')
S3 = ('Add reservations. `reserve(sku, qty) -> int` holds qty units and returns a reservation id (1, 2, 3, ... in '
      'order across all skus); raise ValueError if qty is not positive or more than `available(sku)`. '
      '`available(sku)` is stock minus all reserved units of that sku. `remove` may only take available units. '
      '`release(id)` cancels a reservation; `fulfil(id)` removes its units from stock and records it in history as '
      'a remove; both raise KeyError for an unknown or finished id. `undo` must raise ValueError (changing nothing) '
      'if undoing would leave stock below what is reserved.')
S4 = ('Change: backorders are allowed. `remove` no longer checks stock or availability (it still raises ValueError '
      'for a quantity that is not positive), so stock and available may go negative; `undo` no longer checks '
      'reservations. `reserve` still needs enough available units.')
S5 = ('Add `snapshot() -> str` (a JSON string of the whole state: stock, history, reservations and the next id) and '
      'a classmethod `Inventory.restore(text) -> Inventory` that rebuilds an independent inventory with exactly that '
      'state, so every method behaves the same afterwards (reservation ids continue from where they were).')

ROUNDS = [
    {"spec": S1, "ref": R1, "tests": {"t1_add_remove": t1_add_remove, "t1_bad_quantities": t1_bad_quantities,
                                     "t1_no_negative_stock": t1_no_negative_stock}},
    {"spec": S2, "ref": R2, "tests": {"t2_history": t2_history, "t2_undo": t2_undo}},
    {"spec": S3, "ref": R3, "tests": {"t3_reserve": t3_reserve, "t3_remove_respects_reservations": t3_remove_respects_reservations,
                                     "t3_fulfil_in_history": t3_fulfil_in_history,
                                     "t3_undo_keeps_reservations": t3_undo_keeps_reservations}},
    {"spec": S4, "ref": R4, "tests": {"t4_backorders": t4_backorders, "t4_reserve_still_needs_stock": t4_reserve_still_needs_stock},
     "retires": ["t1_no_negative_stock", "t3_remove_respects_reservations", "t3_undo_keeps_reservations"]},
    {"spec": S5, "ref": R5, "tests": {"t5_round_trip": t5_round_trip, "t5_restored_undo": t5_restored_undo}},
]
