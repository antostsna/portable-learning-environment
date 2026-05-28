# Student Guide

Portable Learning Environment helps you open notebooks, work on assignments, and submit your work to GitHub Classroom.

## What You Need

- A computer with the app installed.
- A GitHub account.
- Access to your GitHub Classroom assignment.
- A GitHub personal access token if your teacher asks you to upload from the app.

## Start Your Work

1. Open Portable Learning Environment.
2. Follow your teacher's instruction.
3. If your teacher asks, run **Pre-flight check** before starting.
4. If your teacher uses **Start lesson**, wait for the assignment and checklist to open.
5. If you are working independently, click **Open JupyterHub** or use the assignment menu.

## Notebook Practice

When the notebook opens:

1. Open the correct assignment folder.
2. Open the notebook file, usually ending in `.ipynb`.
3. Run cells from top to bottom.
4. Read the error message if something fails.
5. Save your notebook often.

## Common Notebook Problems

### ModuleNotFoundError

The package may not be installed. Ask your teacher or check the requirements.

### FileNotFoundError

The notebook cannot find a file. Check that the dataset or image file is in the correct folder.

### NameError

A variable or function was used before it was created. Run earlier cells again or check spelling.

### Kernel died

Restart the kernel and run from the top. If it happens again, tell your teacher.

## Submit Your Assignment

1. Run the notebook from top to bottom.
2. Save the notebook.
3. Choose **Assignment > Upload assignment**.
4. Select your assignment folder.
5. Review the submission quality check.
6. Fix failed checks if possible.
7. Paste your GitHub personal access token.
8. Click upload.
9. Confirm the status badge says **Pushed**.

## Submission Quality Check

The app checks whether your notebook can be read, whether empty code cells exist,
whether outputs are saved, whether Git is configured, and whether there are files
to submit. A warning is not always wrong, but you should read it carefully before
uploading.

## Before Asking for Help

Prepare:
- Assignment name.
- What you clicked.
- The exact error message.
- Screenshot if the problem is visual.
- Which cell failed.

## Good Learning Habits

- Do not only make the code work once. Restart the kernel and run from the top.
- Write short explanations for your results.
- For image processing, compare before and after images.
- For AI, explain the metric, not only the accuracy number.
- Commit and submit early if your teacher allows multiple submissions.
