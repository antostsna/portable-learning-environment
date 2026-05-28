"""CSS injected into ``QTextDocument`` when the docs viewer renders Markdown.

The widget-level stylesheet on ``QTextBrowser`` does NOT cascade into the
document body — Qt renders the converted HTML using the document's
``defaultStyleSheet`` instead. This module is the single place that controls
prose typography in the in-app documentation reader.

Design goals:
    * Larger body type than the rest of the UI (15 px) — reading at length
      benefits from a bigger size than chrome controls.
    * Generous line-height (1.7) for paragraphs.
    * Strong heading hierarchy with visible separators.
    * Code blocks that look like real code blocks (dark surface, monospace,
      breathing room).
    * Blockquotes styled as tinted callouts.
    * Tables with a clearly distinguished header.

Qt's HTML/CSS subset is limited; this stylesheet uses only the properties
documented at https://doc.qt.io/qt-6/richtext-html-subset.html.
"""

from ple.core.constants import THEME_DARK


_LIGHT = """
body {
    color: #1e293b;
    font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif;
    font-size: 15px;
    line-height: 1.7;
}

/* ---------- Headings ---------- */
h1 {
    color: #0f172a;
    font-size: 30px;
    font-weight: 800;
    margin-top: 4px;
    margin-bottom: 18px;
    padding-bottom: 10px;
    border-bottom: 2px solid #cbd5e1;
}
h2 {
    color: #0f172a;
    font-size: 22px;
    font-weight: 700;
    margin-top: 32px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid #e2e8f0;
}
h3 {
    color: #0f172a;
    font-size: 18px;
    font-weight: 700;
    margin-top: 26px;
    margin-bottom: 8px;
}
h4 {
    color: #334155;
    font-size: 14px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 6px;
}
h5, h6 {
    color: #475569;
    font-size: 13px;
    font-weight: 700;
    margin-top: 16px;
    margin-bottom: 6px;
}

/* ---------- Prose ---------- */
p {
    color: #1e293b;
    margin-top: 0;
    margin-bottom: 14px;
}
strong {
    color: #0f172a;
    font-weight: 700;
}
em {
    color: #475569;
    font-style: italic;
}
a {
    color: #1d4ed8;
    text-decoration: none;
    font-weight: 600;
}

/* ---------- Lists ---------- */
ul, ol {
    margin-top: 6px;
    margin-bottom: 16px;
    padding-left: 28px;
}
li {
    color: #1e293b;
    margin-bottom: 6px;
}

/* ---------- Code ---------- */
code {
    background-color: #f1f5f9;
    color: #b45309;
    padding: 2px 6px;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    font-family: "Cascadia Mono", "Consolas", "Courier New", monospace;
    font-size: 13px;
}
pre {
    background-color: #0f172a;
    color: #e2e8f0;
    padding: 14px 18px;
    border: 1px solid #1e293b;
    border-radius: 8px;
    font-family: "Cascadia Mono", "Consolas", "Courier New", monospace;
    font-size: 13px;
    margin-top: 12px;
    margin-bottom: 16px;
}
pre code {
    background-color: transparent;
    color: #e2e8f0;
    padding: 0;
    border: 0;
    font-size: 13px;
}

/* ---------- Callouts ---------- */
blockquote {
    color: #1e293b;
    background-color: #eff6ff;
    border-left: 4px solid #2563eb;
    padding: 12px 18px;
    margin-top: 12px;
    margin-bottom: 16px;
}

/* ---------- Tables ---------- */
table {
    border-collapse: collapse;
    margin-top: 14px;
    margin-bottom: 18px;
}
th {
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 10px 14px;
    border: 1px solid #cbd5e1;
    text-align: left;
    font-weight: 700;
}
td {
    color: #1e293b;
    padding: 10px 14px;
    border: 1px solid #e2e8f0;
    background-color: #ffffff;
}

/* ---------- Misc ---------- */
hr {
    border: 0;
    border-top: 1px solid #cbd5e1;
    margin-top: 22px;
    margin-bottom: 22px;
}
img {
    margin-top: 8px;
    margin-bottom: 8px;
}
"""


_DARK = """
body {
    color: #e2e8f0;
    font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif;
    font-size: 15px;
    line-height: 1.7;
}

/* ---------- Headings ---------- */
h1 {
    color: #ffffff;
    font-size: 30px;
    font-weight: 800;
    margin-top: 4px;
    margin-bottom: 18px;
    padding-bottom: 10px;
    border-bottom: 2px solid #334155;
}
h2 {
    color: #ffffff;
    font-size: 22px;
    font-weight: 700;
    margin-top: 32px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid #1e293b;
}
h3 {
    color: #f1f5f9;
    font-size: 18px;
    font-weight: 700;
    margin-top: 26px;
    margin-bottom: 8px;
}
h4 {
    color: #cbd5e1;
    font-size: 14px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 6px;
}
h5, h6 {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 700;
    margin-top: 16px;
    margin-bottom: 6px;
}

/* ---------- Prose ---------- */
p {
    color: #e2e8f0;
    margin-top: 0;
    margin-bottom: 14px;
}
strong {
    color: #ffffff;
    font-weight: 700;
}
em {
    color: #cbd5e1;
    font-style: italic;
}
a {
    color: #93c5fd;
    text-decoration: none;
    font-weight: 600;
}

/* ---------- Lists ---------- */
ul, ol {
    margin-top: 6px;
    margin-bottom: 16px;
    padding-left: 28px;
}
li {
    color: #e2e8f0;
    margin-bottom: 6px;
}

/* ---------- Code ---------- */
code {
    background-color: #162338;
    color: #fbbf24;
    padding: 2px 6px;
    border: 1px solid #1e293b;
    border-radius: 4px;
    font-family: "Cascadia Mono", "Consolas", "Courier New", monospace;
    font-size: 13px;
}
pre {
    background-color: #060a14;
    color: #e2e8f0;
    padding: 14px 18px;
    border: 1px solid #1e293b;
    border-radius: 8px;
    font-family: "Cascadia Mono", "Consolas", "Courier New", monospace;
    font-size: 13px;
    margin-top: 12px;
    margin-bottom: 16px;
}
pre code {
    background-color: transparent;
    color: #e2e8f0;
    padding: 0;
    border: 0;
    font-size: 13px;
}

/* ---------- Callouts ---------- */
blockquote {
    color: #e2e8f0;
    background-color: #162338;
    border-left: 4px solid #3b82f6;
    padding: 12px 18px;
    margin-top: 12px;
    margin-bottom: 16px;
}

/* ---------- Tables ---------- */
table {
    border-collapse: collapse;
    margin-top: 14px;
    margin-bottom: 18px;
}
th {
    background-color: #162338;
    color: #ffffff;
    padding: 10px 14px;
    border: 1px solid #334155;
    text-align: left;
    font-weight: 700;
}
td {
    color: #e2e8f0;
    padding: 10px 14px;
    border: 1px solid #1e293b;
    background-color: #111a2e;
}

/* ---------- Misc ---------- */
hr {
    border: 0;
    border-top: 1px solid #334155;
    margin-top: 22px;
    margin-bottom: 22px;
}
img {
    margin-top: 8px;
    margin-bottom: 8px;
}
"""


def markdown_css(theme: str) -> str:
    """Return the Markdown stylesheet for the named theme.

    Falls back to the light stylesheet on any unknown value.
    """
    if isinstance(theme, str) and theme.lower() == THEME_DARK.lower():
        return _DARK
    return _LIGHT


__all__ = ["markdown_css"]
