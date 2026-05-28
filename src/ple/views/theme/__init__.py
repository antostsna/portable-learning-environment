"""Theme loaders. Two surfaces are themed:

* The Qt widget stylesheet (``light.qss`` / ``dark.qss``) — controls all
  chrome and surfaces in the app.
* The documentation viewer's HTML stylesheet (``markdown_css.py``) — controls
  prose typography inside the rendered Markdown.

Both are exposed here so the rest of the app imports one module.
"""

from ple.core import theme_path

from .markdown_css import markdown_css

_VALID_THEMES = {"light", "dark"}


def load_stylesheet(name: str) -> str:
    """Return the contents of ple/views/theme/<name>.qss.

    Raises FileNotFoundError if the theme file is missing.
    """
    key = name.lower()
    if key not in _VALID_THEMES:
        key = "light"
    return theme_path(f"{key}.qss").read_text(encoding="utf-8")


__all__ = ["load_stylesheet", "markdown_css"]
