# Support

How to get help and how to file a useful bug report.

---

## Before filing an issue

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for your exact error message.
2. Check [FAQ.md](FAQ.md).
3. Re-run the **Pre-flight check** inside PLE — many issues are environment problems it can catch.

---

## How to file an issue

Open an issue at: <https://github.com/anto112/portable-learning-environment/issues/new>

Include **all** of the following, or the issue is hard to act on:

### Required

- **PLE version** — git commit hash or release version (e.g. `c6e3390`).
- **OS** — Windows version, e.g. `Windows 11 23H2`.
- **Python version** — `python --version`.
- **Install path** — packaged app vs source.
- **What you were doing** — one sentence (e.g. "Clicked Start Lesson, pasted Classroom URL").
- **What you expected** — one sentence.
- **What actually happened** — one sentence.

### Required if there's an error

- **The exact error text** — copy/paste, not paraphrase, not screenshot of text.
- **Which cell or step failed** (for notebook problems).
- **The full traceback** if Python crashed.

### Helpful

- **Screenshot** if the bug is visual.
- **Course mode** and **delivery mode** selected at the time.
- **Pre-flight check output** — copy the result.

---

## Issue template

Paste this and fill in:

```
**PLE version:**
**OS:**
**Python version:**
**Install type:** packaged / source

**What I was doing:**
**What I expected:**
**What happened:**

**Error / traceback:**
```


**Pre-flight result (if relevant):**
```


**Screenshot (if relevant):**
```

---

## Security issues

If you find a security issue (token leakage, code execution, unsafe network behavior), **do not file a public issue**. Email the maintainer:

- Haryanto — <haryanto462@gmail.com>

Include reproduction steps and a description of the impact.

---

## Feature requests

Open a regular issue with the prefix `[feature]` in the title. Describe:

- The user role (Teacher / Student / IT / Stakeholder).
- The pain point you have today.
- The outcome you'd like.

Don't include implementation details unless you want to. The maintainer will discuss approach in the issue.

---

## Contributing

Pull requests welcome. Before submitting:

- Use a feature branch.
- Match existing code style (PyQt6 conventions, snake_case).
- Verify the app launches and pre-flight passes.
- Update docs if behavior changes.
