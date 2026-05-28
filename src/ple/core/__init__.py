"""Core helpers shared by every layer. No Qt, no business logic."""

from .constants import (
    APP_ID,
    APP_NAME,
    APP_ORG,
    APP_VERSION,
    COURSE_MODES,
    DEFAULT_LOCAL_JUPYTER_URL,
    DELIVERY_HUB,
    DELIVERY_LOCAL,
    DELIVERY_MODES,
    ENV_JUPYTER_URL,
    LOCAL_JUPYTER_PORT_START,
    SETTINGS_DEFAULT_COURSE,
    SETTINGS_HUB_URL,
    SETTINGS_THEME,
    SETTINGS_WELCOME_SEEN,
    SETTINGS_WORK_FOLDER,
    THEME_DARK,
    THEME_LIGHT,
    THEMES,
)
from .paths import ASSET_DIR, DOCS_DIR, THEME_DIR, asset_path, docs_path, theme_path

__all__ = [
    # App identity
    "APP_ID",
    "APP_NAME",
    "APP_ORG",
    "APP_VERSION",
    # Jupyter
    "DEFAULT_LOCAL_JUPYTER_URL",
    "ENV_JUPYTER_URL",
    "LOCAL_JUPYTER_PORT_START",
    # QSettings keys
    "SETTINGS_DEFAULT_COURSE",
    "SETTINGS_HUB_URL",
    "SETTINGS_THEME",
    "SETTINGS_WELCOME_SEEN",
    "SETTINGS_WORK_FOLDER",
    # Catalogues
    "COURSE_MODES",
    "DELIVERY_HUB",
    "DELIVERY_LOCAL",
    "DELIVERY_MODES",
    "THEME_DARK",
    "THEME_LIGHT",
    "THEMES",
    # Paths
    "ASSET_DIR",
    "DOCS_DIR",
    "THEME_DIR",
    "asset_path",
    "docs_path",
    "theme_path",
]
