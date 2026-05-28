"""Filesystem paths.

Project layout::

    <repo>/
        assets/                      ASSET_DIR
        docs/                        DOCS_DIR
        src/
            ple/                     <- this package
                core/paths.py        <- this file
                views/theme/         THEME_DIR
        main.py

``THEME_DIR`` is derived from the package location, while ``ASSET_DIR`` and
``DOCS_DIR`` sit at the repo root so they're easy to ship next to the
executable in a PyInstaller bundle.
"""

from pathlib import Path

# ple/core/paths.py -> ple/core -> ple
_PLE_ROOT = Path(__file__).resolve().parent.parent

# ple -> src -> repo root
_REPO_ROOT = _PLE_ROOT.parent.parent

ASSET_DIR = _REPO_ROOT / "assets"
DOCS_DIR = _REPO_ROOT / "docs"
THEME_DIR = _PLE_ROOT / "views" / "theme"


def asset_path(name: str) -> str:
    """Return absolute path to an asset file as a string (for Qt APIs that
    don't accept ``pathlib.Path``)."""
    return str(ASSET_DIR / name)


def docs_path(name: str) -> Path:
    """Return absolute path to a docs/ markdown file."""
    return DOCS_DIR / name


def theme_path(name: str) -> Path:
    """Return absolute path to a stylesheet (.qss) file."""
    return THEME_DIR / name
