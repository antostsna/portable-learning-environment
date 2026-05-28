"""Lesson preferences and the per-course checklist templates.

This module holds the textual content that the teacher sees on the home page
and inside the Start lesson dialog. Keeping it in models means a designer can
edit the wording without touching the controller or the view.
"""

from dataclasses import dataclass

from ple.core.constants import (
    COURSE_MODES,
    DELIVERY_HUB,
    DELIVERY_LOCAL,
    DELIVERY_MODES,
)


# Short paragraphs shown under the course/delivery selects on the home page.
COURSE_NOTES = {
    "General lecture":
        "Use this for concept explanation, demonstration, discussion, and a short exit ticket.",
    "Programming language":
        "Focus on syntax practice, debugging, functions, control flow, and code explanation.",
    "Digital image processing":
        "Guide students through image loading, transformation, filtering, comparison, and output evidence.",
    "AI / machine learning":
        "Guide students through dataset inspection, model training, evaluation, and result reflection.",
    "General lab":
        "Use this for open-ended lab work with setup checks, checkpoints, evidence, and submission.",
}

DELIVERY_NOTES = {
    DELIVERY_LOCAL:
        "Students practice on a local notebook server started only when needed.",
    DELIVERY_HUB:
        "The teacher or institution controls the notebook server and student environment.",
}

# Per-course suggested checklist; pre-filled in the Start lesson dialog and
# may be edited before the lesson actually starts.
CHECKLIST_TEMPLATES = {
    "General lecture": (
        "1. State the learning objective in one sentence.\n"
        "2. Show one worked example.\n"
        "3. Ask students to predict the next result.\n"
        "4. Run a short practice task.\n"
        "5. Collect one reflection or exit-ticket answer."
    ),
    "Programming language": (
        "1. Open the starter notebook.\n"
        "2. Run setup cells from top to bottom.\n"
        "3. Complete syntax and variable exercises.\n"
        "4. Complete function or control-flow checkpoints.\n"
        "5. Explain one bug and how it was fixed.\n"
        "6. Save and upload the assignment."
    ),
    "Digital image processing": (
        "1. Load and display the sample image.\n"
        "2. Convert color spaces or grayscale.\n"
        "3. Apply enhancement, thresholding, filtering, or edge detection.\n"
        "4. Compare before and after results.\n"
        "5. Save output images and explain the parameter choices.\n"
        "6. Save and upload the assignment."
    ),
    "AI / machine learning": (
        "1. Load the dataset and inspect samples.\n"
        "2. Split data into training and testing sets.\n"
        "3. Train a baseline model.\n"
        "4. Evaluate accuracy, loss, or relevant metrics.\n"
        "5. Improve one model setting and explain the result.\n"
        "6. Save and upload the assignment."
    ),
    "General lab": (
        "1. Open the lab notebook or instructions.\n"
        "2. Run all setup checks.\n"
        "3. Complete each checkpoint in order.\n"
        "4. Save evidence of results.\n"
        "5. Submit work and confirm the pushed status."
    ),
}


@dataclass
class LessonPreferences:
    """User's selected course mode and delivery mode for the current lesson."""

    course: str = COURSE_MODES[0]
    delivery: str = DELIVERY_LOCAL

    def checklist_template(self) -> str:
        return CHECKLIST_TEMPLATES.get(self.course, CHECKLIST_TEMPLATES["General lecture"])

    def preview_text(self) -> str:
        return f"{COURSE_NOTES.get(self.course, '')} {DELIVERY_NOTES.get(self.delivery, '')}"

    @property
    def is_hub(self) -> bool:
        return self.delivery == DELIVERY_HUB


def lesson_template(course_mode: str) -> str:
    """Return the suggested checklist text for a course mode."""
    return CHECKLIST_TEMPLATES.get(course_mode, CHECKLIST_TEMPLATES["General lecture"])


__all__ = [
    "CHECKLIST_TEMPLATES",
    "COURSE_MODES",
    "COURSE_NOTES",
    "DELIVERY_HUB",
    "DELIVERY_LOCAL",
    "DELIVERY_MODES",
    "DELIVERY_NOTES",
    "LessonPreferences",
    "lesson_template",
]
