"""Assignment lifecycle state.

A single `AssignmentStatus` tracks how far a student is through the lesson
flow: cloned → opened → submitted → pushed. The model is intentionally a
dataclass so it serialises trivially and tests don't need Qt.
"""

from dataclasses import asdict, dataclass


@dataclass
class AssignmentStatus:
    """Boolean checkpoints for one assignment's progress."""

    cloned: bool = False
    opened: bool = False
    submitted: bool = False
    pushed: bool = False

    # ------------------------------------------------------------------
    # Transitions — each method records that a stage was completed.
    # They are forward-only by convention; an assignment never "uncloned"s
    # mid-session. Use ``reset()`` between assignments.
    # ------------------------------------------------------------------
    def mark_cloned(self) -> None:
        self.cloned = True

    def mark_opened(self) -> None:
        self.opened = True

    def mark_submitted(self) -> None:
        self.submitted = True

    def mark_pushed(self) -> None:
        self.pushed = True

    def reset(self) -> None:
        self.cloned = False
        self.opened = False
        self.submitted = False
        self.pushed = False

    # ------------------------------------------------------------------
    # Compatibility helpers — the legacy controller used a plain dict for
    # the status. These keep the existing view code working unchanged.
    # ------------------------------------------------------------------
    def as_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AssignmentStatus":
        return cls(
            cloned=bool(data.get("cloned", False)),
            opened=bool(data.get("opened", False)),
            submitted=bool(data.get("submitted", False)),
            pushed=bool(data.get("pushed", False)),
        )
