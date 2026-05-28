"""Portable Learning Environment — desktop teaching workspace.

Top-level package. Submodules:
    core/        — constants, paths, cross-cutting helpers (no Qt).
    models/      — pure-Python state (no Qt widgets, may use QSettings).
    services/    — IO and business logic (subprocess, urllib, fs). Testable.
    views/       — PyQt6 widgets, pages, dialogs, theme.
    controllers/ — wire signals to services and models.

Until the migration finishes, ``MainWindow.py`` and ``controler.py`` in the
repo root still exist and re-export the legacy classes. Once everything has
been extracted into ``ple/``, those files will be removed and ``main.py``
will switch to ``from ple.app import App``.
"""

from .core.constants import APP_ID, APP_VERSION

__all__ = ["APP_ID", "APP_VERSION"]
