# GitHub Classroom Setup for Teachers

> *Last tested: 2026-05.*

This guide walks a teacher with **no prior GitHub experience** through everything needed to run an assignment with Portable Learning Environment.

You only do steps 1–5 **once per course**. Step 6 (creating an assignment) repeats for each lab.

---

## What you will create

```
GitHub Account (you)
   └── GitHub Organization (your course)
         └── GitHub Classroom (linked to the org)
               ├── Roster (your student list)
               ├── Starter Repository (template notebook)
               └── Assignments (one per lab)
                     └── Student Repository (auto-created per student)
```

PLE talks to **student repositories** for clone, submit, and push.

---

## Step 1 — Create a GitHub account

If you already have one, skip this step.

1. Go to <https://github.com/signup>.
2. Use your **university email** if possible (it makes Step 2 faster).
3. Verify the email.

---

## Step 2 — Apply for GitHub Education (optional but recommended)

GitHub Education gives teachers free private repositories, free Classroom features, and access to the Teacher Toolbox.

1. Go to <https://education.github.com/teachers>.
2. Click **Get teacher benefits**.
3. Upload proof of teaching status (faculty ID card, course page, or letter).
4. Wait for approval. Usually **1–7 days**.

You can continue with the rest of this guide while waiting — Classroom works without Education benefits, but private repos may cost money for organizations without them.

---

## Step 3 — Create an organization for your course

A GitHub Organization is a shared namespace owned by you, where student repos will live.

1. Click your avatar (top-right) → **Your organizations** → **New organization**.
2. Choose the **Free** plan.
3. Organization name: something stable like `cs101-fall-2026` or `dip-uni-name`.
4. Contact email: your university email.
5. This organization belongs to: **A business or institution** (recommended for universities).
6. Skip "Invite members" — you don't need TAs yet.

**Tip:** one organization per **course offering**, not per assignment. Reuse it each semester or roll over to a new one annually.

---

## Step 4 — Create a Classroom

1. Go to <https://classroom.github.com>.
2. Click **Sign in with GitHub** and authorize the app.
3. Click **New classroom**.
4. **Select an organization:** pick the one from Step 3.
5. Classroom name: `CS101 — Fall 2026` (this is shown to students).
6. Click **Create classroom**.

---

## Step 5 — Add students to the roster

You need a list of student identifiers (names, student IDs, or university emails).

1. Inside your Classroom, click **Students** → **Update students**.
2. Choose how to identify them:
   - **Upload from LMS** (Canvas, Moodle, Google Classroom) — easiest if available.
   - **Upload CSV** — one student identifier per line.
   - **Manual entry** — paste identifiers separated by commas.
3. After upload, each student gets a unique **classroom join link**. You will share this with students later.

> Students don't have to be on the roster to start, but using a roster ties their GitHub account to their real identity for grading.

---

## Step 6 — Create a starter repository (template)

This is the notebook the students will clone and edit.

1. In your **organization** (not the classroom), click **New repository**.
2. Repository name: `lab01-starter` (or similar).
3. Visibility: **Private**.
4. Tick **Add a README**.
5. Click **Create repository**.

Add a sample notebook:

1. Open the new repo → **Add file → Create new file**.
2. Filename: `lab01.ipynb`.
3. Paste a minimal notebook (you can also upload a real `.ipynb` file).
4. Add a `.gitignore` file with the content below (copy the whole block):

   ```gitignore
   # Jupyter
   .ipynb_checkpoints/
   *.pyc
   __pycache__/

   # OS
   .DS_Store
   Thumbs.db

   # Large generated artefacts (uncomment if you want students to NOT submit these)
   # *.h5
   # *.pkl
   # data/raw/
   ```

5. **Important:** mark the repo as a template.
   - Repo → **Settings** → tick **Template repository**.

This is what GitHub Classroom will clone for each student.

---

## Step 7 — Create your first assignment

1. Open <https://classroom.github.com> → your classroom → **Assignments** → **New assignment**.
2. **Assignment basics:**
   - Title: `Lab 01 — Variables and Loops`.
   - Type: **Individual** (or **Group** if you want teams).
   - Repository visibility: **Private**.
   - Grant students admin access: **No** (recommended — keeps the repo clean).
3. **Starter code and feedback:**
   - Add a **template repository** → select the one from Step 6.
   - Supported editor: leave blank (students will use PLE / Jupyter).
4. **Grading and feedback:** skip autograding for now; you can add tests later.
5. **Deadline:** set if applicable.
6. Click **Create assignment**.
7. On the next page, **copy the invitation URL** — looks like:
   `https://classroom.github.com/a/AbCd1234`

You will paste this URL into PLE when starting the lesson.

---

## Step 8 — Test the flow as a student (recommended)

Before class:

1. Open the invitation URL in an **incognito window** signed in as a test account.
2. Accept the assignment. GitHub Classroom creates a repo named `lab01-<your-username>` inside the organization.
3. Open PLE → **Start lesson** → paste the invitation URL (or the student repo URL).
4. Confirm the clone, open, edit, and submit flow works end-to-end.

---

## Step 9 — Brief your students on Personal Access Tokens (PATs)

Students need a token to push from PLE. **Do not use account passwords.**

Send students this short instruction:

> 1. Go to <https://github.com/settings/personal-access-tokens/new> (fine-grained tokens).
> 2. **Token name:** `PLE - <course code>`.
> 3. **Expiration:** end of semester (e.g. **90 days**).
> 4. **Repository access:** *Only select repositories* → choose your assignment repo (e.g. `lab01-yourname`).
> 5. **Repository permissions:**
>    - `Contents` → **Read and write**.
>    - `Metadata` → **Read-only** (auto-selected).
>    - Leave everything else as **No access**.
> 6. Click **Generate token**.
> 7. Copy the token immediately and paste it into PLE when it asks. **GitHub will not show it again.**

Token recap for teachers:

- Fine-grained tokens are safer than classic tokens.
- Scoped to a single repo, not the whole account.
- Auto-expire at end of semester — students just generate a new one next term.

---

## Per-lab checklist (every week)

For each new lab, you only repeat Step 7. Step 6 (template repo) can be reused or duplicated.

1. Update or duplicate the starter repo with the new notebook.
2. Classroom → **New assignment** → link the template.
3. Copy the invitation URL.
4. Share the URL with students (LMS, email, or QR code).
5. In class, open PLE → **Start lesson** → paste URL.

---

## Troubleshooting

| Problem | Likely cause | Fix |
| --- | --- | --- |
| Student gets `404` on clone | Repo is private and PAT lacks access | Re-issue PAT with `Contents: Read/write` on the specific repo. |
| Push fails with `403` | Wrong PAT, expired PAT, or wrong username | Generate a fresh fine-grained PAT scoped to the repo. |
| Student can't accept assignment | Not on roster, or wrong account signed in | Add them to roster, confirm correct GitHub login. |
| All students get the same repo | Assignment created as Group, not Individual | Recreate the assignment as Individual. |
| Notebook outputs cause huge diffs | Outputs committed to git | Add `*.ipynb_checkpoints/` to `.gitignore`; teach **Kernel → Restart & Clear Output** before commit if your course requires clean diffs. |

See also [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for app-level issues.

---

## Next steps

- [GET_STARTED_TEACHER.md](TEACHER_GUIDE.md) — daily teaching workflow.
- [STUDENT_GUIDE.md](STUDENT_GUIDE.md) — what to tell students.
- [FAQ.md](FAQ.md) — common questions.
