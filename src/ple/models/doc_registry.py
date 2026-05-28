"""Single source of truth for documents shown in the in-app Documentation
page. Add a new entry here and the sidebar list, the Help-menu shortcuts,
and the (?) help icons will all pick it up automatically.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DocEntry:
    title: str
    filename: str
    subtitle: str


DOC_ENTRIES: tuple[DocEntry, ...] = (
    DocEntry("Install on Windows", "INSTALL_WINDOWS.md",
             "Prerequisites and step-by-step setup"),
    DocEntry("GitHub Classroom Setup", "GITHUB_CLASSROOM_SETUP.md",
             "Org, classroom, roster, assignments, PATs"),
    DocEntry("Teacher Guide", "TEACHER_GUIDE.md",
             "Run a class session end-to-end"),
    DocEntry("Student Guide", "STUDENT_GUIDE.md",
             "Open notebooks, submit your work"),
    DocEntry("Delivery Guide", "DELIVERY.md",
             "Lab install, packaging, JupyterHub"),
    DocEntry("Stakeholder Brief", "STAKEHOLDER_BRIEF.md",
             "Evaluation, pilot, success metrics"),
    DocEntry("Troubleshooting", "TROUBLESHOOTING.md",
             "Common errors and fixes"),
    DocEntry("FAQ", "FAQ.md", "Frequently asked questions"),
    DocEntry("Glossary", "GLOSSARY.md",
             "Jupyter vs JupyterHub vs Classroom"),
    DocEntry("Support", "SUPPORT.md", "How to file a useful issue"),
    DocEntry("Changelog", "CHANGELOG.md", "What changed"),
)


def find_entry(filename: str) -> DocEntry | None:
    for entry in DOC_ENTRIES:
        if entry.filename == filename:
            return entry
    return None


__all__ = ["DOC_ENTRIES", "DocEntry", "find_entry"]
