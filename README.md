# Portable Learning Environment (PLE)

A desktop teaching workspace that combines **Jupyter notebooks**, **GitHub Classroom**, and a guided lesson workflow into one app for programming, image processing, AI, and general computing courses.

---

## I am a…

### 👩‍🏫 Teacher

You want to run a lab session with guided checklists and GitHub Classroom assignments.

1. [Install PLE on Windows](docs/INSTALL_WINDOWS.md) (≈5 min)
2. [Set up GitHub Classroom](docs/GITHUB_CLASSROOM_SETUP.md) (once per course)
3. [Daily teaching workflow](docs/TEACHER_GUIDE.md)

### 🧑‍🎓 Student

You want to open notebooks and submit assignments.

1. [Install PLE on Windows](docs/INSTALL_WINDOWS.md) (or ask your teacher for the packaged app)
2. [Student workflow](docs/STUDENT_GUIDE.md)

### 🛠️ IT / Lab Administrator

You want to roll PLE out to many machines or host a JupyterHub.

- [Delivery guide](docs/DELIVERY.md) — lab install, packaged app, JupyterHub.
- [Troubleshooting](docs/TROUBLESHOOTING.md)

### 🏛️ University Stakeholder

You want to evaluate PLE for a department or course.

- [Stakeholder brief](docs/STAKEHOLDER_BRIEF.md) — goals, risks, metrics, pilot plan.

---

## What PLE does

- **Course modes:** General lecture, Programming, Digital Image Processing, AI / ML, General lab.
- **Delivery modes:** local Jupyter Notebook (student practice) or teacher-controlled JupyterHub.
- **Lesson workflow:** pre-flight check → choose course → clone assignment → open notebook → checklist → submit → push.
- **GitHub Classroom integration** with fine-grained personal access tokens (no passwords).
- **Submission quality check** before upload (empty cells, missing outputs, missing artefacts, dirty git state).
- **Help Center** and **Help Stuck Students** pages built into the app.

Screenshots: see [`assets/`](assets/).

---

## Quick start for developers

```powershell
git clone https://github.com/anto112/portable-learning-environment.git
cd portable-learning-environment
py -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements-core.txt
.\.venv\Scripts\python main.py
```

For DIP or AI courses, also install `requirements-dip.txt` and/or `requirements-ai.txt`. See [INSTALL_WINDOWS.md](docs/INSTALL_WINDOWS.md) for the full guide including prerequisites.

---

## Project layout

```
portable-learning-environment/
├── main.py                       Entry shim — adds src/ to sys.path
├── assets/                       Icons, HTML help pages, screenshots
├── docs/                         Markdown guides (rendered in-app)
├── requirements*.txt             Tiered installs (core / dip / ai)
├── .github/workflows/release.yml CI: build packaged Windows .zip
└── src/                          All source code
    ├── main.py                   (reserved for future entry point)
    ├── MainWindow.py             Legacy view (to be split into ple/views/)
    ├── controler.py              Legacy controller (to be split into ple/controllers/)
    └── ple/                      New MVC package
        ├── core/                 Constants, paths — no Qt
        ├── models/               Data + state — no Qt widgets
        ├── services/             (planned) IO + business logic
        ├── views/                Qt widgets
        │   └── theme/            light.qss, dark.qss, markdown_css.py
        └── controllers/          (planned) signal wiring
```

See [docs/CHANGELOG.md](docs/CHANGELOG.md) for the migration status.

---

## Documentation index

| Doc | Audience | Purpose |
| --- | --- | --- |
| [INSTALL_WINDOWS.md](docs/INSTALL_WINDOWS.md) | Everyone | Prerequisites + install |
| [GITHUB_CLASSROOM_SETUP.md](docs/GITHUB_CLASSROOM_SETUP.md) | Teachers | One-time Classroom setup |
| [TEACHER_GUIDE.md](docs/TEACHER_GUIDE.md) | Teachers | Daily teaching workflow |
| [STUDENT_GUIDE.md](docs/STUDENT_GUIDE.md) | Students | Working on assignments |
| [DELIVERY.md](docs/DELIVERY.md) | IT | Lab rollout + packaging |
| [DEPLOYMENT_CHECKLIST.md](docs/DEPLOYMENT_CHECKLIST.md) | Maintainers | Pre-release + build + publish steps |
| [STAKEHOLDER_BRIEF.md](docs/STAKEHOLDER_BRIEF.md) | Leaders | Evaluation + pilot |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Everyone | Common errors and fixes |
| [FAQ.md](docs/FAQ.md) | Everyone | Frequent questions |
| [GLOSSARY.md](docs/GLOSSARY.md) | Everyone | Jupyter vs JupyterHub vs Classroom, etc. |
| [SUPPORT.md](docs/SUPPORT.md) | Everyone | How to get help, file issues |
| [CHANGELOG.md](docs/CHANGELOG.md) | Everyone | What changed |
| [SCREENSHOTS.md](docs/SCREENSHOTS.md) | Maintainers | Screenshots referenced by guides |

---

## License

[MIT](LICENSE)

## Contact

Developed by **Haryanto** — <haryanto462@gmail.com>
