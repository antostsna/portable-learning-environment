# Teacher Guide

Portable Learning Environment helps teachers run programming, digital image processing, AI, and general lab sessions with less setup friction.

## Teaching Goals

Use the app to:
- Run pre-flight checks before class.
- Start a lesson with a clear workflow.
- Choose the correct learning mode for the course.
- Open Jupyter Notebook or JupyterHub.
- Clone GitHub Classroom assignments.
- Show students a task checklist.
- Track assignment progress.
- Help stuck students quickly.

## Course Types

### General Lecture

Best for concept explanation, demonstrations, discussion, and short reflection.

Use when:
- You do not need a full coding lab.
- You want to demonstrate a notebook.
- You want students to answer an exit question.

### Programming Language

Best for syntax, variables, functions, loops, control flow, debugging, and code explanation.

Suggested checklist:
- Run setup cells.
- Complete syntax practice.
- Complete function/control-flow checkpoint.
- Explain one bug and fix.
- Save and submit.

### Digital Image Processing

Best for OpenCV, NumPy, image transformations, filters, thresholds, edges, and output comparison.

Suggested checklist:
- Load and display image.
- Convert color/grayscale.
- Apply filter or threshold.
- Compare before/after.
- Save output image.
- Explain parameter choices.

### AI / Machine Learning

Best for datasets, model training, evaluation, and reflection.

Suggested checklist:
- Load dataset.
- Inspect samples.
- Split train/test.
- Train baseline model.
- Evaluate metrics.
- Improve one setting and explain result.

### General Lab

Best for mixed practical tasks or non-standard workshops.

## Delivery Modes

### Student Practice - Local Jupyter Notebook

Use this when students work independently on their own machine. The app starts local Jupyter only after the lesson begins.

### Teacher Controlled - JupyterHub

Use this when the university manages the server, packages, users, storage, or GPU access. Enter the JupyterHub URL during Start lesson.

## Start Lesson Workflow

1. Select the course type on the dashboard.
2. Select the delivery mode.
3. Click **Pre-flight check** and fix required failures.
4. Click **Start lesson**.
5. Paste the GitHub Classroom assignment URL if there is an assignment.
6. Select the work folder.
7. Review or edit the checklist.
8. Click **Start**.
9. Keep the checklist visible while students work.

## Pre-flight Environment Check

Run this before the first lab activity. It checks:

- Python availability.
- Git availability.
- Jupyter availability.
- Git `user.name` and `user.email`.
- Common packages such as NumPy, Pandas, Matplotlib, OpenCV, and scikit-learn.
- TensorFlow when the course mode is AI / machine learning.
- JupyterHub URL reachability when teacher-controlled JupyterHub is selected.

Treat failed checks as blockers. Treat warnings as items to review before class.

## Assignment Status

- **Cloned**: assignment repository exists on the computer.
- **Opened**: assignment folder was opened in Jupyter.
- **Submitted**: work was marked ready for upload.
- **Pushed**: Git successfully pushed to GitHub.

Use these badges to quickly see where the class is stuck.

## Submission Quality Check

When students upload, the app checks:

- The selected folder is a Git repository.
- Git identity is configured.
- Notebook files exist and are readable JSON.
- Empty code cells are flagged.
- Notebook outputs are present when code cells exist.
- Common evidence artifacts exist, such as images, CSV files, reports, or model files.
- Git has changed files to submit.

Warnings do not always mean the submission is wrong. For example, a programming-only task may not require image output. Use the warnings as a final teaching checkpoint.

## Helping Stuck Students

Open **Help > Help stuck students** or use the dashboard button.

Start with:
- Restart kernel.
- Run notebook from top.
- Check first error, not last error.
- Check dataset path.
- Pull latest starter code if the teacher updated the assignment.
- Submit again after saving.

## Good Assignment Design

For better learning outcomes:
- Put learning objectives at the top.
- Include one worked example.
- Use small checkpoints.
- Ask students to explain one result.
- Ask for evidence: output image, metric, screenshot, or short reflection.
- Keep setup code separate from concept work.

## GitHub Token Reminder

Students should use GitHub personal access tokens, not account passwords. This is safer and matches current GitHub authentication.
