"""Minimal Streamlit Community Cloud entrypoint for public metadata only."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from public_preview import main

main()
