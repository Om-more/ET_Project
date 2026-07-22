from __future__ import annotations

import sys
from pathlib import Path

# Allow `from mapao.src...` imports to resolve to the repository's top-level `src/` package.
ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT))

__path__.insert(0, str(SRC_PATH))
