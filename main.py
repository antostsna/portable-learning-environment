"""Entry point for Portable Learning Environment.

All source code lives in ``src/``. This file simply puts that directory on
``sys.path`` and hands off to the controller. Run with::

    python main.py

PyInstaller builds also use this file as the spec entry — see
``.github/workflows/release.yml``.
"""

import sys
from pathlib import Path

# Make ``src/`` importable so ``import controler`` / ``import ple`` resolve.
_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from controler import Controller  # noqa: E402 — must follow sys.path setup


def run():
    window = Controller()
    sys.exit(window.exec())


if __name__ == "__main__":
    run()
