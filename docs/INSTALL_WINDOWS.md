# Install Portable Learning Environment on Windows

> *Last tested: 2026-05 on Windows 11 with Python 3.11.*

This guide is for first-time users. No prior Python or Git knowledge is required.

There are **two ways** to install PLE. Choose one:

| Path | Who it's for | Time |
| --- | --- | --- |
| **A. Packaged app (recommended)** | Teachers, students, anyone who just wants to run the app | ~5 min |
| **B. From source** | IT admins, contributors, lab machine images | ~15 min |

---

## Path A — Packaged app (recommended)

1. Go to the [Releases page](https://github.com/anto112/portable-learning-environment/releases).
2. Download the latest `PortableLearningEnvironment-windows.zip`.
3. Right-click the zip → **Extract All** → choose a short path such as `C:\PLE`.
   - Avoid `Desktop` or `Documents` — Windows long-path limits can break some packages.
4. Open the extracted folder and double-click `Portable Learning Environment.exe`.
5. On first launch Windows may show **"Windows protected your PC"**. Click **More info → Run anyway**.

That's it. Skip to [First-run checklist](#first-run-checklist).

> **No Releases yet?** Use Path B until a packaged build is published.

---

## Path B — From source

### Step 1. Check disk space and network

- **Disk:** at least **10 GB free** (full AI/DIP install is large).
- **Network:** access to `github.com`, `pypi.org`, and your university JupyterHub if used.

### Step 2. Install Python 3.11 or newer

1. Download Python from <https://www.python.org/downloads/windows/>.
2. Run the installer. **Important:** tick **"Add python.exe to PATH"** before clicking Install.
3. Open **PowerShell** (Start menu → type "PowerShell") and verify:

   ```powershell
   python --version
   ```

   You should see `Python 3.11.x` or newer. If you see "command not found", reinstall Python with the PATH option ticked.

### Step 3. Install Git

1. Download Git from <https://git-scm.com/download/win>.
2. Run the installer. Accept the defaults.
3. Verify in PowerShell:

   ```powershell
   git --version
   ```

   You should see `git version 2.x`.

### Step 4. Pick an install location

Use a **short path** to avoid Windows long-path errors:

```powershell
cd C:\
mkdir ple
cd ple
```

### Step 5. Clone and install

```powershell
git clone https://github.com/anto112/portable-learning-environment.git
cd portable-learning-environment
py -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements-core.txt
```

`requirements-core.txt` installs the minimum needed to run the app (~300 MB, ~2 min).

To add extras for your course type, install one or both of:

```powershell
.\.venv\Scripts\python -m pip install -r requirements-dip.txt   # Digital Image Processing
.\.venv\Scripts\python -m pip install -r requirements-ai.txt    # AI / Machine Learning
```

Or install everything at once with the original `requirements.txt`.

### Step 6. Run

```powershell
.\.venv\Scripts\python main.py
```

The app window should open within a few seconds.

---

## First-run checklist

When the app opens:

1. Click **Pre-flight check** on the dashboard.
2. Review the results:
   - **Green / pass** — you're ready.
   - **Warning** — read it; usually safe to proceed.
   - **Red / fail** — fix before starting class. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
3. If you plan to use GitHub Classroom, follow [GITHUB_CLASSROOM_SETUP.md](GITHUB_CLASSROOM_SETUP.md) once.

---

## Common installation problems

| Symptom | Cause | Fix |
| --- | --- | --- |
| `'py' is not recognized` | Python not on PATH | Reinstall Python, tick "Add to PATH". |
| `'git' is not recognized` | Git not installed | Install Git from git-scm.com. |
| `error: Microsoft Visual C++ 14.0 is required` | Missing build tools | Install [Build Tools for Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/). |
| Long-path / `ERROR: Could not install packages` after a deep path | Windows MAX_PATH | Move project to `C:\ple`. |
| PyQt6 fails to install | Old pip | Re-run `python -m pip install --upgrade pip`. |
| Install hangs on TensorFlow | Slow network or 32-bit Python | Confirm 64-bit Python; retry on better connection. |

More items in [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## Next steps

- Teachers → [GET_STARTED_TEACHER.md](GET_STARTED_TEACHER.md)
- Students → [GET_STARTED_STUDENT.md](GET_STARTED_STUDENT.md)
- IT / lab admins → [DELIVERY.md](DELIVERY.md)
