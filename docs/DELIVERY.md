# Delivery Guide

This guide explains how to deliver Portable Learning Environment to teachers, students, and university IT teams.

## Delivery Models

### 1. Lab Computer Installation

Use this when the university controls the classroom computers.

Requirements:
- Windows 10/11
- Python 3.11 or newer
- Git
- Internet access for JupyterHub, GitHub Classroom, and package installation

Install:

```powershell
git clone https://github.com/anto112/portable-learning-environment.git
cd portable-learning-environment
py -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Run:

```powershell
.\.venv\Scripts\python main.py
```

Recommended for:
- Computer labs
- Courses with IT support
- JupyterHub-managed classes

### 2. Packaged Windows App

Use this when teachers or students should not manage Python directly.

Install PyInstaller:

```powershell
.\.venv\Scripts\python -m pip install pyinstaller
```

Build:

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

Output:

```text
dist/
  Portable Learning Environment/
    Portable Learning Environment.exe
    assets/
    ...
```

Distribute the whole folder:

```text
dist/Portable Learning Environment
```

Recommended for:
- BYOD classes
- Non-technical users
- Short workshops

## Jupyter Delivery Choices

### Student Practice - Local Jupyter Notebook

The app starts a local notebook server only when needed. It uses a free local port starting at `8899` and disables token prompts for the in-app session.

Use when:
- Students work on their own laptop
- The course does not require centralized server control
- Students need lightweight practice notebooks

### Teacher Controlled - JupyterHub

The teacher or IT team provides a JupyterHub URL. Students use the controlled server environment.

Use when:
- The university manages packages, users, storage, and GPUs
- Teachers need a consistent environment
- Courses use AI, large datasets, or shared computing resources

Optional environment variable:

```powershell
$env:PLE_JUPYTER_URL="https://your-jupyterhub.example.edu/hub/login"
```

## GitHub Classroom Requirements

Students need:
- A GitHub account
- Access to the classroom assignment
- Git installed on the computer
- A GitHub personal access token for upload/push

Token recommendation:
- Use fine-grained tokens when possible.
- Give access only to the required classroom repositories.
- Do not ask students for GitHub account passwords.

## Suggested University Rollout

1. Pilot in one programming or AI lab section.
2. Validate JupyterHub URL, GitHub Classroom workflow, and token instructions.
3. Package the app or install it on lab machines.
4. Train teachers with the Teacher Guide.
5. Provide students the Student Guide before the first lab.
6. Collect feedback after two assignments.

## Operational Checklist

- Python environment installs successfully.
- App opens with correct taskbar icon.
- Help Center opens.
- Pre-flight environment check passes or only shows acceptable warnings.
- Start lesson opens the correct Jupyter mode.
- Git clone works with a classroom assignment.
- Submission quality check appears before upload.
- Upload assignment works with a GitHub token.
- Status badges update.
- Help Stuck Students page opens.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for a complete list of installation, runtime, GitHub, JupyterHub, and packaging issues.
