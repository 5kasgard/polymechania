"""Workers AI free-allowance guard (queue q24).

Every /ai call made by the bench is logged to bench/neurons.jsonl (time,
model, neurons, what for). Before a call, `room()` says how many neurons
are left, counted over the last 24 hours.

Why a rolling 24 hours, not the UTC day: Cloudflare's pricing page says
limits reset at 00:00 UTC, but on 2026-10-29 at 00:20 UTC the door was
refused ("4006: you have used up your daily free allocation") with only
2,876 neurons used since 00:00 UTC by Cloudflare's own analytics; the 24
hours before it held 12,207. A rolling window is the stricter reading
and fits what happened, so the guard uses it until the evidence says
otherwise (see bench/neurons.md).

    python bench/neurons.py          # room left now, and the last 24 h by hour
    DOOR_DIR=... python bench/neurons.py probe   # one tiny call: does Cloudflare allow use now?
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOG = Path(__file__).resolve().parent / "neurons.jsonl"
LIMIT = 10_000
RESERVE = 300  # never plan to spend the last few hundred: Cloudflare's count and ours can differ


class OutOfNeurons(RuntimeError):
    pass


def now() -> datetime:
    return datetime.now(timezone.utc)


def stamp(t: datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def rows() -> list[dict]:
    if not LOG.exists():
        return []
    return [json.loads(line) for line in LOG.read_text().splitlines() if line.strip()]


def used(hours: int = 24, at: datetime | None = None) -> float:
    at = at or now()
    since = stamp(at - timedelta(hours=hours))
    return sum(r["neurons"] for r in rows() if r["time"] >= since)


def room(at: datetime | None = None) -> float:
    return LIMIT - RESERVE - used(at=at)


def check(estimate: float = 50) -> None:
    left = room()
    if left < estimate:
        raise OutOfNeurons(f"only {left:.0f} neurons of room in the last 24 h (need about {estimate:.0f})")


def log(model: str, neurons: float, purpose: str, source: str = "door usage") -> None:
    with LOG.open("a") as f:
        f.write(json.dumps({"time": stamp(now()), "model": model, "neurons": round(float(neurons or 0), 3),
                            "purpose": purpose, "source": source}) + "\n")


def refused_for_allowance(text: str) -> bool:
    return "4006" in text or "daily free allocation" in text


def probe() -> dict:
    """One tiny call that bypasses the guard, to see whether Cloudflare allows use now.

    Logged to bench/neurons-probes.jsonl with the 24-hour total at that moment,
    so the refusals and successes can be set against both readings of the limit.
    """
    import os
    import urllib.error
    import urllib.request
    import sys
    sys.path.insert(0, str(LOG.parent / "boot"))
    import run as t2
    dd = Path(os.environ["DOOR_DIR"])
    req = urllib.request.Request(t2.DOOR + "/ai", method="POST", data=json.dumps({
        "model": "@cf/meta/llama-3.1-8b-instruct-fp8-fast", "max_tokens": 3,
        "messages": [{"role": "user", "content": "Say ok."}]}).encode(), headers={
        "content-type": "application/json", "user-agent": "polymechania-bench/1",
        "CF-Access-Client-Id": (dd / "cf_id").read_text().strip(),
        "CF-Access-Client-Secret": (dd / "cf_secret").read_text().strip(),
        "x-door-token": (dd / "door_token").read_text().strip()})
    row = {"time": stamp(now()), "used_24h": round(used()),
           "used_utc_day": round(sum(r["neurons"] for r in rows() if r["time"][:10] == stamp(now())[:10]))}
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            out = json.loads(r.read())
        log("@cf/meta/llama-3.1-8b-instruct-fp8-fast", out.get("usage", {}).get("neurons", 0), "allowance probe")
        row["allowed"] = True
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")
        row["allowed"] = False
        row["refusal"] = body[:120]
    with (LOG.parent / "neurons-probes.jsonl").open("a") as f:
        f.write(json.dumps(row) + "\n")
    return row


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["probe"]:
        print(probe())
        raise SystemExit
    by_hour: dict[str, float] = {}
    since = stamp(now() - timedelta(hours=24))
    for r in rows():
        if r["time"] >= since:
            by_hour[r["time"][:13]] = by_hour.get(r["time"][:13], 0) + r["neurons"]
    for h, n in sorted(by_hour.items()):
        print(f"{h}:00Z  {n:8.0f}")
    print(f"used in the last 24 h: {used():.0f}; room (limit {LIMIT:,}, reserve {RESERVE}): {room():.0f}")
