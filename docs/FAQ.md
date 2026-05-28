# Frequently Asked Questions

For terminology, see [GLOSSARY.md](GLOSSARY.md). For error messages, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## General

### Is PLE free?

Yes. PLE is released under the [MIT License](../LICENSE). GitHub and GitHub Classroom are also free for educators (see [GitHub Education](https://education.github.com/teachers)).

### Does PLE work on macOS or Linux?

The app is built on PyQt6, which runs on all three, but PLE is **tested on Windows 10/11**. macOS / Linux should work from source but may need small fixes. Issues and PRs welcome.

### Do students need accounts anywhere?

Yes — one **GitHub account** per student. No JupyterHub account is needed if you use the local notebook mode.

### Does PLE collect telemetry?

No. PLE makes no network calls except to Jupyter (local), JupyterHub (yours), and GitHub (when you clone/push).

---

## For teachers

### Do I need GitHub Education benefits to use Classroom?

No — Classroom works for any GitHub user. Education benefits give you free private repos for the organization, which is worth applying for.

### Can I reuse one organization across semesters?

Yes. Common patterns: `cs101-fall-2026`, then a fresh one each year, or one long-lived `cs101` with archived assignments.

### Can students submit multiple times?

Yes. Each push updates the same student repo. PLE doesn't enforce a one-shot rule — set your own policy.

### What about autograding?

GitHub Classroom supports autograding with tests, but PLE does not run it. Configure it in Classroom's web UI if needed.

### Can I use this for group assignments?

Yes — Classroom supports group assignments. PLE doesn't change behaviour for group work; the assignment URL just resolves to a team repo instead of an individual one.

### What if my course uses a language other than Python?

PLE ships with the bash and C Jupyter kernels (`bash_kernel`, `jupyter-c-kernel`). For other languages, install the corresponding Jupyter kernel into the same venv.

---

## For students

### My teacher gave me a Classroom invitation URL. What now?

Open PLE → **Start lesson** → paste the URL. PLE handles the rest.

### Where is my work saved?

In a folder PLE creates when you accept the assignment. The pre-flight check and the status badges show the path.

### I lost my PAT. What do I do?

GitHub never shows a token twice. Generate a new one ([instructions](GITHUB_CLASSROOM_SETUP.md#step-9--brief-your-students-on-personal-access-tokens-pats)) and paste the new one into PLE. The old one will stop working at expiration anyway.

### Will PLE remember my PAT?

The current version does not persist the token between launches. A planned settings panel will offer OS-keyring storage.

---

## For IT / admins

### Does PLE need admin rights to install?

For the **packaged app**, no. For the **source install**, only if Python and Git aren't already system-wide.

### Can I pre-install PLE on lab images?

Yes — the packaged app is a folder. Drop it into your image. The source install also works if the venv is checked into the image.

### How do I point all students at our JupyterHub?

Set the environment variable before launch:

```powershell
$env:PLE_JUPYTER_URL="https://hub.example.edu/hub/login"
```

For permanent deployment, set it system-wide (System Properties → Environment Variables).

### Does PLE need any inbound ports?

No. It only makes outbound connections (HTTPS to GitHub, your JupyterHub, and PyPI during install). Local Jupyter listens on `127.0.0.1:8899` and is not exposed.

---

## Privacy and policy

### Where are GitHub tokens stored?

Currently in memory only. Not written to disk, not sent anywhere except `https://api.github.com` and the git remote.

### Does PLE share data with the maintainer?

No.

### Can I fork PLE for my institution?

Yes — MIT license. Please keep attribution.
