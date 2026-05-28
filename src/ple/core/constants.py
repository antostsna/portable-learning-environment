"""Application-wide constants. Pure data, no imports beyond stdlib."""

APP_ID = "portable.learning.environment"
APP_VERSION = "2026.05"
APP_NAME = "Portable Learning Environment"
APP_ORG = "PLE"

# Local Jupyter
LOCAL_JUPYTER_PORT_START = 8899
DEFAULT_LOCAL_JUPYTER_URL = f"http://localhost:{LOCAL_JUPYTER_PORT_START}/tree?"

# Environment variable that overrides the JupyterHub URL at startup
ENV_JUPYTER_URL = "PLE_JUPYTER_URL"

# QSettings keys — keep stable; users have these on disk
SETTINGS_HUB_URL = "jupyter/hub_url"
SETTINGS_WORK_FOLDER = "work/folder"
SETTINGS_DEFAULT_COURSE = "ui/default_course"
SETTINGS_THEME = "ui/theme"
SETTINGS_WELCOME_SEEN = "ui/welcome_seen"

# Course modes — single source of truth, ordered as shown in the UI
COURSE_MODES = (
    "General lecture",
    "Programming language",
    "Digital image processing",
    "AI / machine learning",
    "General lab",
)

# Delivery modes
DELIVERY_LOCAL = "Student practice - local Jupyter Notebook"
DELIVERY_HUB = "Teacher controlled - JupyterHub"
DELIVERY_MODES = (DELIVERY_LOCAL, DELIVERY_HUB)

# Themes
THEME_LIGHT = "Light"
THEME_DARK = "Dark"
THEMES = (THEME_LIGHT, THEME_DARK)
