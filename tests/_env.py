"""Puts the repository on the path, and Gnomon too when it can be found.

The planner, the forms and the worlds need nothing beyond the standard
library. The organisation (`polymechania.org`) keeps its books in a Gnomon
record, so its tests run only where Gnomon is built: set GNOMON_PYTHON to
Gnomon's `python/` folder, or keep a built clone beside this one
(`../gnomon`)."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_candidates = [os.environ.get("GNOMON_PYTHON"), str(ROOT.parent / "gnomon" / "python")]
for c in _candidates:
    if c and (Path(c) / "gnomon" / "__init__.py").exists():
        sys.path.insert(1, c)
        break

try:
    import gnomon  # noqa: F401
    gnomon.Memory  # the native core must be built for this to work
    HAVE_GNOMON = True
except Exception:  # not found, or found but not built
    HAVE_GNOMON = False

needs_gnomon = unittest.skipUnless(HAVE_GNOMON, "needs Gnomon (set GNOMON_PYTHON to its built python/ folder)")
