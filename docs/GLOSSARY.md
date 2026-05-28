# Glossary

Plain-language definitions of the tools and concepts PLE uses. The point of this page is to remove the most common source of confusion in lab courses: people thinking *Jupyter*, *JupyterHub*, *GitHub*, and *GitHub Classroom* are the same thing. They aren't.

---

## Tools

### Python

A programming language. PLE is written in Python, and student notebooks usually run Python code.

### Jupyter Notebook

A file format (`.ipynb`) and a local app for running code in cells, mixed with text and charts. **Runs on your own computer.** PLE launches its own local notebook server when you choose **Student Practice** mode.

### JupyterHub

A **server** that runs Jupyter notebooks for many users at once. Your university hosts it. Students sign in to a URL and get a notebook environment in their browser without installing Python locally. PLE supports JupyterHub in **Teacher Controlled** mode.

| | Jupyter Notebook | JupyterHub |
| --- | --- | --- |
| Where it runs | Student's laptop | University server |
| Who installs it | Each student (or PLE) | IT once |
| Good for | Individual practice, BYOD | Lab courses, shared GPUs, consistent environment |

### Git

A version-control tool. Tracks file changes locally and pushes them to a remote server (like GitHub).

### GitHub

A website that hosts Git repositories. <https://github.com>

### GitHub Classroom

A separate website (<https://classroom.github.com>) that uses GitHub for teaching. It automatically creates one repository per student for each assignment, manages a class roster, and shows submission status. **You still need a regular GitHub account and a GitHub Organization.**

### GitHub Organization

A shared account on GitHub that holds repositories owned by a group (not a single person). Your course belongs to an organization. Student repositories live inside it.

### PyQt6

The Windows desktop UI framework PLE is built with. End users don't interact with it directly.

---

## Concepts

### Repository (repo)

A project tracked by Git. For PLE, this usually means **one assignment per repo**. Each student gets their own copy.

### Template repository

A regular GitHub repo marked as "template" in Settings. GitHub Classroom uses it as the starting code for every student's assignment repo.

### Clone

Download a copy of a repo to your computer. PLE clones the assignment for you when you start a lesson.

### Commit

A snapshot of your changes in Git, saved locally with a message.

### Push

Upload your local commits to GitHub. PLE pushes for you when you submit.

### Personal Access Token (PAT)

A long string that authenticates you to GitHub instead of a password. PLE asks for one when pushing your work.

- **Classic** vs **Fine-grained:** prefer fine-grained — they're scoped to specific repos.
- **Expiration:** required; pick end-of-semester.
- **Scope for PLE:** `Contents: Read and write` on the assignment repo. Nothing else.

See [GITHUB_CLASSROOM_SETUP.md](GITHUB_CLASSROOM_SETUP.md#step-9--brief-your-students-on-personal-access-tokens-pats) for the click-by-click steps.

### Kernel

The Python (or Bash, C, etc.) interpreter behind a notebook. "Restart the kernel" means throw away all current variables and start over.

### Cell

One block in a notebook. Either **code** (runs and produces output) or **markdown** (formatted text).

---

## PLE-specific terms

### Course mode

What kind of class you're running: General Lecture, Programming, Digital Image Processing, AI/ML, or General Lab. PLE adjusts checklists and pre-flight checks based on this.

### Delivery mode

- **Student Practice** — PLE starts a local Jupyter notebook server on your machine.
- **Teacher Controlled** — PLE opens your university's JupyterHub URL.

### Pre-flight check

A scan PLE runs before class to confirm Python, Git, Jupyter, and required packages are working. Run this before every first-class-of-the-semester.

### Submission quality check

A scan PLE runs **before** you push, to catch empty cells, missing outputs, missing artefacts, and unconfigured git identity.

### Assignment status badges

- **Cloned** — the assignment exists on disk.
- **Opened** — you opened it in Jupyter at least once.
- **Submitted** — you marked it ready to upload.
- **Pushed** — Git successfully pushed to GitHub.
