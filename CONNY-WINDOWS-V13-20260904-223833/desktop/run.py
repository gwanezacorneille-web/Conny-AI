import sys
from pathlib import Path

# V13 launcher: ensure the project root is importable.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.main_window import main

if __name__ == "__main__":
    raise SystemExit(main())
