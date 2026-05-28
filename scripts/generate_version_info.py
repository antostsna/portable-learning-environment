"""Regenerate scripts/version_info.txt from ple.core.APP_VERSION.

Keeps the Windows executable's embedded version metadata in sync with the
single source of truth in src/ple/core/constants.py.

Run from the repo root::

    python scripts/generate_version_info.py
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from ple.core.constants import APP_NAME, APP_VERSION  # noqa: E402


def _version_tuple(version: str) -> tuple[int, int, int, int]:
    """Turn '2026.05' into (2026, 5, 0, 0)."""
    parts = [int(p) for p in version.replace("-", ".").split(".") if p.isdigit()]
    parts = (parts + [0, 0, 0, 0])[:4]
    return tuple(parts)  # type: ignore[return-value]


TEMPLATE = """# UTF-8
#
# PyInstaller Windows version resource for the packaged executable.
# Embeds Company/Product/Version into the .exe file properties.
# Regenerate with: python scripts/generate_version_info.py
#
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={vers},
    prodvers={vers},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0),
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          "040904B0",
          [
            StringStruct("CompanyName", "{name}"),
            StringStruct("FileDescription", "{name}"),
            StringStruct("FileVersion", "{version}"),
            StringStruct("InternalName", "PortableLearningEnvironment"),
            StringStruct("LegalCopyright", "MIT License. Developed by Haryanto."),
            StringStruct("OriginalFilename", "{name}.exe"),
            StringStruct("ProductName", "{name}"),
            StringStruct("ProductVersion", "{version}"),
          ],
        )
      ]
    ),
    VarFileInfo([VarStruct("Translation", [1033, 1200])]),
  ],
)
"""


def main() -> None:
    out = REPO_ROOT / "scripts" / "version_info.txt"
    content = TEMPLATE.format(
        vers=_version_tuple(APP_VERSION),
        version=APP_VERSION,
        name=APP_NAME,
    )
    out.write_text(content, encoding="utf-8")
    print(f"wrote {out.relative_to(REPO_ROOT)} for version {APP_VERSION}")


if __name__ == "__main__":
    main()
