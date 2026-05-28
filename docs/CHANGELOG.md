# Changelog

All notable changes to PLE are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow date-based tags until a 1.0 release.

---

## [Unreleased] — UI overhaul, in-app docs, settings, release pipeline

### Added / Changed (general-use pass)
- **Collapsible sidebar** — a hamburger (☰) toggle in the toolbar shows/hides the left navigation. Navigation stays reachable via the View menu and toolbar when hidden, so collapsing never traps the user.
- **General-purpose home page** — the app is no longer framed as teacher-only:
  - Hero now reads "Your learning workspace" with three clear actions: **Open Jupyter Notebook** (local, primary), **Open JupyterHub** (remote), and **Start lesson** (guided/teacher flow).
  - **Open JupyterHub** is a first-class action for any user — prompts for the hub URL the first time and saves it to Settings.
  - `open_local_notebook` always forces local mode; `open_jupyterhub` always opens the configured/entered hub — predictable regardless of saved settings.
- Toolbar "Jupyter" action and sidebar quick-action now open a local notebook explicitly.

### Fixed
- **Jupyter wouldn't open** — launched a bare `jupyter` command (PATH-dependent; fails when started via `.venv\\Scripts\\python`) and loaded the tab before the server booted (~4 s) → connection-refused. Now launches via `sys.executable -m notebook` and waits for the port to accept connections (with a "Starting…" placeholder and clear error on timeout). Pre-flight Jupyter check made PATH-independent too.
- **Help pages 404** after the `src/` move — `help.html` / `stuck.html` resolved relative to `__file__` (now `src/`). Routed through `ple.core.asset_path`.

### Changed (contrast & palette pass)
- **New professional palettes** (Slate + Blue) for both themes. Every body text ≥ 7:1 contrast on its surface; muted text ≥ 4.5:1 (WCAG AA).
  - Light: canvas `#f8fafc`, surface `#ffffff`, text `#0f172a`, muted `#475569`, primary `#2563eb`.
  - Dark: canvas `#0b1220`, surface `#111a2e`, text `#f1f5f9`, muted `#cbd5e1`, primary `#3b82f6`.
- **Defaults for previously-unstyled widgets** so dialogs and embedded controls inherit the theme: `QDialog`, `QMessageBox`, `QPlainTextEdit`, `QTextEdit`, `QPushButton` (default), `QMenu`, `QMenuBar::item`, `QHeaderView::section`, `QTableWidget`, `QTabBar`. Fixes invisible text in start-lesson, push, and welcome dialogs under dark mode.
- **Pre-flight / submission result table** now sets both background **and foreground** per status (Pass / Warn / Fail). Pale row backgrounds no longer collide with the global theme color.
- **Markdown viewer** — `QTextDocument.setDefaultStyleSheet` is now applied per theme so headings, links, inline code, code blocks, and blockquotes pick up the right palette. Theme switches re-render the active doc immediately.
- Tooltip pill restyled, help-icon and status-badge tones rebalanced for AA contrast.

### Added (latest pass)
- **Inline tooltips** on every confusing field — home page selects, sidebar buttons, status badges, URL bar, settings inputs.
- **`(?)` help icons** next to JupyterHub URL, work folder, default course mode, and the home Course/Delivery selects. Clicking opens the matched guide inside the in-app docs viewer.
- **Theme selector** in Settings — Light / Dark — persisted as `ui/theme`. Applied on launch and immediately on save. Reset to defaults restores Light.
- **Dark stylesheet** matching the light palette (sidebar `#070b13`, surface `#0f1420`, card `#131a29`, gradient hero, themed scrollbars and menus).
- **Styled QToolTip** with PLE accent border in both themes.

### Added
- **In-app Documentation viewer** — sidebar nav opens a Docs page that renders any markdown file from `docs/` (uses `QTextBrowser.setMarkdown`).
- **Sidebar navigation** with Home / Documentation / Settings / About and quick actions for Pre-flight, Start lesson, Open Jupyter.
- **Settings page** with persistence via `QSettings`: JupyterHub URL, default work folder, default course mode. Replaces the `PLE_JUPYTER_URL` env-var-only flow (env var still wins when set).
- **First-run welcome dialog** — guides newcomers to docs or pre-flight on first launch; suppressed afterwards.
- **About page** — version, credits, repository / issues / Classroom links.
- **GitHub Actions release workflow** (`.github/workflows/release.yml`) — builds packaged Windows `.zip` on `v*` tags and attaches it to a GitHub Release.
- `docs/SCREENSHOTS.md` — placeholder for screenshot captures used by guides.
- "Last tested" date stamps on `INSTALL_WINDOWS.md`, `GITHUB_CLASSROOM_SETUP.md`, `TROUBLESHOOTING.md`.

### Changed
- **Stylesheet refresh** — new palette (`#0f1729` sidebar, `#1f6feb` primary, light `#f6f8fb` surface), pill status badges with check/circle glyphs, gradient hero, larger typography scale, scrollbar restyling, splitter handles, focus rings.
- **Home page** — replaces tab-only layout with a hero header, info-card row, lesson setup panel, and status panel.
- **About** — opens the new About page instead of a message box.
- **Menubar** — added a `View` menu (Home / Documentation / Settings) and Help shortcuts to the in-app Install + Classroom guides.

### Previously (documentation overhaul)
- `docs/INSTALL_WINDOWS.md`, `docs/GITHUB_CLASSROOM_SETUP.md`, `docs/FAQ.md`, `docs/GLOSSARY.md`, `docs/TROUBLESHOOTING.md`, `docs/SUPPORT.md`, `docs/CHANGELOG.md`.
- `requirements-core.txt`, `requirements-dip.txt`, `requirements-ai.txt` — tiered installs so non-AI courses skip TensorFlow.
- `README.md` rewritten as a short role-routed landing page.
- `docs/DELIVERY.md` — duplicated troubleshooting section removed; now links to `TROUBLESHOOTING.md`.

### Migration notes
- Existing users can keep using `requirements.txt`. New installs should prefer `requirements-core.txt` and add `-dip.txt` / `-ai.txt` only if their course needs them.
- All previous docs (`TEACHER_GUIDE`, `STUDENT_GUIDE`, `DELIVERY`, `STAKEHOLDER_BRIEF`) remain valid and are still linked from the README.

---

## c6e3390 — 2025-05 — Migrate to PyQt6

- Move from PyQt5 to PyQt6, including WebEngine.
- Modernize Jupyter integration and notebook server launching.

## 6033ae6 — 2020-08

- Initial public version of the app.

---

> *To regenerate the timeline accurately, run `git log --oneline` and add an entry per release tag.*
