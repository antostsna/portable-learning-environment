# Troubleshooting

> *Last tested: 2026-05 on Windows 11.*

Common problems and fixes, grouped by where they appear. Search this page with Ctrl+F.

If your problem isn't here, check [FAQ.md](FAQ.md) or [SUPPORT.md](SUPPORT.md) for how to file an issue.

---

## Installation

### `'py' is not recognized as an internal or external command`

Python isn't on the PATH. Reinstall Python from <https://www.python.org/downloads/windows/> and **tick "Add python.exe to PATH"** during install.

### `'git' is not recognized`

Git isn't installed. Get it from <https://git-scm.com/download/win>.

### `error: Microsoft Visual C++ 14.0 is required`

Some scientific wheels need the Microsoft build tools. Install [Build Tools for Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and re-run pip install.

### `ERROR: Could not install packages due to an OSError: [WinError 3] The system cannot find the path specified`

This is the Windows long-path limit. Move the project to a short path such as `C:\ple\portable-learning-environment` and re-run install. Optionally enable Windows Long Path support via Group Policy.

### TensorFlow install hangs or fails

- Confirm you're on 64-bit Python: `python -c "import struct; print(struct.calcsize('P') * 8)"` should print `64`.
- Retry on a better connection — TensorFlow is ~600 MB.
- If your course doesn't need AI, skip `requirements-ai.txt` entirely.

### PyQt6 fails to install

Upgrade pip first: `.\.venv\Scripts\python -m pip install --upgrade pip`. Then retry.

---

## Running the app

### App opens but window is blank or all-white

The Qt WebEngine renderer failed to initialize. Try:
- Update your graphics driver.
- Set `QT_OPENGL=software` in environment variables and relaunch.

### `Jupyter command not found`

Jupyter is missing from the venv. Reinstall core requirements:

```powershell
.\.venv\Scripts\python -m pip install -r requirements-core.txt
```

### App launches but pre-flight check fails on Git

Configure your git identity (required to commit/push):

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Local Jupyter asks for a token

Close any old Jupyter servers running on ports 8899+, then restart the app. PLE finds a free port starting at `8899` and disables tokens for its own session.

### Taskbar shows the wrong icon

Restart Windows Explorer (Task Manager → Restart **Windows Explorer**). The app sets a unique AppUserModelID on first launch.

---

## GitHub Classroom and Git

### Student gets `404 Not Found` when cloning

The repo is private and the PAT isn't authorized. Re-issue a fine-grained PAT scoped to the specific assignment repo with **Contents: Read and write**. See [GITHUB_CLASSROOM_SETUP.md](GITHUB_CLASSROOM_SETUP.md#step-9--brief-your-students-on-personal-access-tokens-pats).

### Push fails with `403 Forbidden`

- The PAT expired — generate a new one.
- The PAT is for the wrong repo — re-create with the correct repo in scope.
- The student signed in with a different GitHub account than the one on the roster.

### `fatal: not a git repository`

The selected folder isn't a cloned assignment. Start over from **Start lesson → paste invitation URL**, and let PLE choose the folder.

### Submission quality check shows warnings

Warnings are not always wrong. Read each one:

- **Empty code cells** — delete or fill them.
- **No outputs** — run the notebook top-to-bottom before submitting.
- **No evidence artefacts** — for image processing or AI courses, save an output image, CSV, or metric.
- **No changed files** — nothing to commit; verify you saved your work.

### Notebook outputs cause huge git diffs

Two options:
1. Teach **Kernel → Restart & Clear Output** before commit if you want clean diffs.
2. Or accept the outputs as part of the submission (PLE's quality check expects outputs to be present).

---

## JupyterHub

### Cannot reach JupyterHub URL

- Confirm the URL with the IT team — it should end in `/hub/login`.
- Try opening it in a regular browser first.
- Check VPN / institutional network requirements.

### Set the JupyterHub URL

In PowerShell before launching:

```powershell
$env:PLE_JUPYTER_URL="https://your-jupyterhub.example.edu/hub/login"
.\.venv\Scripts\python main.py
```

---

## Packaging (PyInstaller)

### `dist/` folder is several GB

Expected. PyQt6 + WebEngine + TensorFlow + scientific stack are large. To shrink:
- Build with `requirements-core.txt` only when AI/DIP aren't needed.
- Use UPX compression (`--upx-dir`) at the cost of slower startup.

### `Failed to execute script 'main'`

Usually a missing `--add-data` for `assets`. Rebuild with:

```powershell
.\.venv\Scripts\pyinstaller --noconfirm --windowed `
  --name "Portable Learning Environment" `
  --icon assets\ico.ico `
  --paths src `
  --add-data "assets;assets" `
  --add-data "docs;docs" `
  --add-data "src\ple\views\theme\light.qss;ple\views\theme" `
  --add-data "src\ple\views\theme\dark.qss;ple\views\theme" `
  --collect-submodules ple `
  main.py
```

---

## Still stuck?

See [SUPPORT.md](SUPPORT.md) for how to file an issue with the right information attached.
