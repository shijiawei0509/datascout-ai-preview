"""Public metadata preview, release 2026-10-15-65d7221.

The entrypoint is versioned with the public release so hosted script watchers
observe a change when the shared preview modules are updated.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from public_preview import main

main()
