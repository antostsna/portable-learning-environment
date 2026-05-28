# Deployment Checklist

Use this before cutting a release or rolling PLE out to a lab. Covers both
delivery models — see [DELIVERY.md](DELIVERY.md) for the rollout strategy and
[INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) for end-user install.

> *Last reviewed: 2026-05.*

---

## 1. Pre-release verification (developer machine)

Run from the repo root with the project venv.

- [ ] Dependencies install clean: `.\.venv\Scripts\python -m pip install -r requirements.txt`
- [ ] App launches: `python main.py`
- [ ] **Open Jupyter Notebook** starts a local server and loads the tree (wait ~5 s).
- [ ] **Open JupyterHub** prompts for a URL and opens it.
- [ ] **Documentation** page renders a doc on first open (not blank).
- [ ] **Settings** save/restore; theme switch (Light/Dark) applies live.
- [ ] **Sidebar** show/hide toggle (☰) works.
- [ ] **Pre-flight check** runs and reports Python/Git/Jupyter status.
- [ ] **Help stuck students** page opens (no ERR_FILE_NOT_FOUND).
- [ ] Byte-compile passes: `python -m py_compile main.py src/MainWindow.py src/controler.py`

## 2. Version bump

- [ ] Update `APP_VERSION` in `src/ple/core/constants.py`.
- [ ] Regenerate the Windows version resource: `python scripts/generate_version_info.py`
- [ ] Update the version line at the top of [CHANGELOG.md](CHANGELOG.md).
- [ ] Update the `v2026.05` strings in the sidebar/About if the year changed.

## 3. Repository state (critical — these have bitten us)

- [ ] `docs/` **is committed** (it is NOT gitignored; the in-app reader and the
      packaged build both need it).
- [ ] The whole `src/ple/` package is committed (not just the legacy files).
- [ ] `assets/ico.png` **and** `assets/ico.ico` are committed.
- [ ] `scripts/` (icon + version generators, build script) is committed.
- [ ] `git status` is clean; `git ls-files src/ple | wc -l` is non-zero.

## 4. Build the packaged app

Local:

```powershell
.\scripts\build_windows.ps1
```

Or via CI by pushing a tag:

```powershell
git tag v2026.05.0
git push origin v2026.05.0
```

- [ ] PyInstaller completes without "module not found" errors.
- [ ] `dist\Portable Learning Environment\` contains the `.exe`, `assets\`,
      `docs\`, and `ple\views\theme\*.qss`.

## 5. Test the packaged build (clean machine if possible)

- [ ] Double-click the `.exe` — window opens with the correct taskbar icon.
- [ ] Right-click the `.exe` → Properties → Details shows version `2026.05`.
- [ ] Documentation renders (confirms `docs/` bundled).
- [ ] Open Jupyter Notebook works (confirms Python + notebook bundled).
- [ ] Theme files load (no fallback-to-unstyled).

## 6. Publish

- [ ] CI attached `PortableLearningEnvironment-<tag>-windows.zip` to the GitHub Release.
- [ ] Release notes mention notable changes (pull from CHANGELOG).
- [ ] Update [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) "Path A" link if the asset name changed.

## 7. Rollout

- [ ] Pilot on one lab section first (see DELIVERY.md "Suggested University Rollout").
- [ ] Confirm network access to github.com, pypi.org (source installs), and your JupyterHub.
- [ ] Hand teachers [TEACHER_GUIDE.md](TEACHER_GUIDE.md) and [GITHUB_CLASSROOM_SETUP.md](GITHUB_CLASSROOM_SETUP.md).
- [ ] Hand students [STUDENT_GUIDE.md](STUDENT_GUIDE.md).

---

## Known constraints

- Packaged build is large (PyQt6 + WebEngine + scientific stack). That is expected.
- TensorFlow only ships in `requirements-ai.txt`; a core-only build won't run AI notebooks.
- The app is tested on Windows 10/11. macOS/Linux should work from source but are unverified.
