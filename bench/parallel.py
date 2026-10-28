"""Run independent calls at once (S1: 8 at once was 8.9x faster for free).

    from parallel import run_all
    results = run_all(fn, items, workers=8, first_alone=True)

Results come back in the order of `items`. With `first_alone`, the first
item runs by itself before the rest, so a Claude prompt cache is written
once and the other calls read it, instead of every call racing to write it.
An exception in any call is re-raised after the others finish, with the
item's position, so a failed call is never silently dropped.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable


def run_all(fn: Callable, items: Iterable, workers: int = 8, first_alone: bool = False) -> list:
    items = list(items)
    if not items:
        return []
    results: list = [None] * len(items)
    errors: list = []
    start = 0
    if first_alone:
        results[0] = fn(items[0])
        start = 1

    def one(k):
        try:
            results[k] = fn(items[k])
        except Exception as e:  # collected, then raised with its position
            errors.append((k, e))

    with ThreadPoolExecutor(max(1, workers)) as ex:
        list(ex.map(one, range(start, len(items))))
    if errors:
        k, e = sorted(errors, key=lambda x: x[0])[0]
        raise RuntimeError(f"call {k} of {len(items)} failed ({len(errors)} failed in all): {e}") from e
    return results
