# University Stakeholder Brief

Portable Learning Environment is a desktop application designed to improve practical computing courses by reducing setup friction and giving teachers a guided workflow for notebook-based learning.

## Target Courses

- Programming language courses
- Digital image processing
- Artificial intelligence and machine learning
- General computing labs
- Short technical workshops

## Educational Value

The app supports teaching efficacy by:
- Making lesson setup explicit.
- Checking the environment before class begins.
- Giving students a visible checklist.
- Reducing confusion between Jupyter Notebook, JupyterHub, GitHub, and GitHub Classroom.
- Helping teachers identify whether students are stuck at clone, open, submit, or push.
- Providing immediate help pages for common notebook and Git problems.

## Delivery Models

### Local Student Practice

Students run notebooks on their own computer. This is low infrastructure and suitable for basic programming and small data/image tasks.

Benefits:
- Simple deployment.
- Works without university server resources.
- Good for individual practice.

Risks:
- Student machines may differ.
- Package installation can vary.
- Not ideal for GPU-heavy AI work.

### Teacher Controlled JupyterHub

The university hosts JupyterHub and controls packages, accounts, storage, and compute resources.

Benefits:
- Consistent environment.
- Easier support.
- Better for AI, large datasets, and lab management.

Risks:
- Requires server administration.
- Needs account and access management.
- Requires network reliability.

## Stakeholder Responsibilities

### Teachers

- Prepare GitHub Classroom assignments.
- Choose course type and delivery mode.
- Provide checklist/rubric.
- Monitor assignment status.
- Support conceptual learning.

### Students

- Follow the lesson checklist.
- Save notebooks.
- Submit work using GitHub token.
- Report errors clearly.

### IT / Lab Administrators

- Install Python, Git, and app dependencies, or distribute packaged app.
- Configure JupyterHub if used.
- Confirm network access to GitHub and JupyterHub.
- Maintain lab machine images.

### Program / Department Leaders

- Decide standard delivery model.
- Approve GitHub Classroom and JupyterHub usage.
- Support teacher onboarding.
- Collect feedback and learning outcome evidence.

## Privacy and Security

- The app should not collect student data by itself.
- GitHub account passwords should not be used.
- Students should use GitHub personal access tokens with limited scope.
- If JupyterHub is used, university authentication policy applies.
- Assignment repositories should follow course privacy policy.

## Success Metrics

Track:
- Time required to start first lab activity.
- Number of setup-related support requests.
- Assignment submission success rate.
- Number of failed pre-flight checks before lab.
- Number of submissions with quality-check warnings.
- Number of students stuck before notebook execution.
- Quality of student reflection/explanation.
- Teacher satisfaction after each lab cycle.

## Recommended Pilot

1. Select one programming or image processing course.
2. Run two assignments through PLE.
3. Compare setup issues with previous offering.
4. Collect student feedback.
5. Decide whether to scale to AI and larger lab courses.
