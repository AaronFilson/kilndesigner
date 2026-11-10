"""Engine v2's tests: the reference kilns' data and the helpers beside it import by name."""

import sys
from pathlib import Path

HERE = str(Path(__file__).resolve().parent)
if HERE not in sys.path:
    sys.path.insert(0, HERE)
