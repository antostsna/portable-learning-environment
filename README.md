# Portable Learning Environment (PLE)

Portable Learning Environment is a desktop teaching workspace for programming, digital image processing, AI, and general computing lectures. It combines guided lesson setup, Jupyter Notebook/JupyterHub access, GitHub Classroom assignment flow, submission status, and help pages for students who get stuck.

## Who It Is For

- **Teachers**: run guided lab sessions, open Jupyter, clone assignments, show lesson checklists, and track assignment progress.
- **Students**: practice in notebooks, follow checklists, submit work to GitHub Classroom, and get help for common notebook errors.
- **University stakeholders / IT**: deploy a consistent learning environment for lab courses and support either local practice or institution-managed JupyterHub.

## Main Features

- Course modes: General lecture, Programming language, Digital image processing, AI / machine learning, General lab.
- Delivery modes: local Jupyter Notebook for student practice or teacher-controlled JupyterHub.
- Start lesson workflow: choose course, choose delivery, clone assignment, open notebook environment, show checklist.
- Pre-flight environment check before class.
- Submission quality check before upload.
- Assignment status: cloned, opened, submitted, pushed.
- GitHub token upload flow instead of account passwords.
- Help Center and Help Stuck Students pages.
- Responsive PyQt6 desktop UI.

## Quick Start for Development

```powershell
git clone https://github.com/anto112/portable-learning-environment.git
cd portable-learning-environment
py -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python main.py
```

## Delivery Options

For a university course, there are two practical ways to deliver the app:

1. **Source delivery for lab computers**
   - IT installs Python, Git, and requirements once.
   - Teachers or students run `python main.py`.
   - Best for controlled computer labs where IT can manage Python environments.

2. **Packaged desktop app**
   - Build a Windows executable with PyInstaller.
   - Distribute the `dist` folder or installer to teachers/students.
   - Best for non-technical users and BYOD classes.

See [Delivery Guide](docs/DELIVERY.md) for build and rollout details.

## Documentation

- [Delivery Guide](docs/DELIVERY.md)
- [Teacher Guide](docs/TEACHER_GUIDE.md)
- [Student Guide](docs/STUDENT_GUIDE.md)
- [University Stakeholder Brief](docs/STAKEHOLDER_BRIEF.md)

## Recommended Course Workflow

1. Teacher selects course type and delivery mode on the dashboard.
2. Teacher clicks **Start lesson**.
3. Teacher pastes the GitHub Classroom assignment URL.
4. App clones the assignment and opens Jupyter Notebook or JupyterHub.
5. Students follow the checklist.
6. Students upload assignment with a GitHub personal access token.
7. Teacher checks status badges and GitHub Classroom submissions.

## Contact

Developed by Haryanto  
Email: haryanto462@gmail.com
