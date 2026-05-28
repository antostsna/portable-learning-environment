"""Pure data + state for the app. No Qt widgets; may use QSettings only for
persistence in :mod:`ple.models.settings_model`."""

from .assignment import AssignmentStatus
from .doc_registry import DOC_ENTRIES, DocEntry
from .lesson import LessonPreferences

__all__ = [
    "AssignmentStatus",
    "DOC_ENTRIES",
    "DocEntry",
    "LessonPreferences",
]
