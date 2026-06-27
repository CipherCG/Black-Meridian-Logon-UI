"""Configuration settings for Black Meridian Logon UI"""

import os

# Application Settings
APP_TITLE = "Black Meridian Logon"
APP_VERSION = "1.1.0"

# Database Settings
DB_PATH = os.path.join(os.path.dirname(__file__), "data")
DB_FILE = os.path.join(DB_PATH, "logon.db")
DB_BACKUP_DIR = os.path.join(DB_PATH, "backups")

# Window Settings
WINDOW_WIDTH = 450
WINDOW_HEIGHT = 350
WINDOW_RESIZABLE = False

# Color Scheme (Dark Professional Theme)
BACKGROUND_COLOR = "#1e1e1e"
PRIMARY_COLOR = "#0d47a1"  # Deep Blue
SECONDARY_COLOR = "#1976d2"  # Blue
TEXT_COLOR = "#ffffff"
ERROR_COLOR = "#d32f2f"  # Red
SUCCESS_COLOR = "#388e3c"  # Green
BORDER_COLOR = "#404040"

# Font Settings
FONT_FAMILY = "Arial"
FONT_SIZE_TITLE = 18
FONT_SIZE_LABEL = 11
FONT_SIZE_INPUT = 11
FONT_SIZE_BUTTON = 12

# Input Validation
MIN_USERNAME_LENGTH = 3
MIN_PASSWORD_LENGTH = 8
MAX_USERNAME_LENGTH = 50
MAX_PASSWORD_LENGTH = 100

# Authentication
AUTH_TIMEOUT = 30  # seconds
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 300  # 5 minutes in seconds

# Password Security
BCRYPT_ROUNDS = 12  # Number of rounds for bcrypt hashing
REQUIRE_UPPERCASE = True
REQUIRE_LOWERCASE = True
REQUIRE_NUMBERS = True
REQUIRE_SPECIAL_CHARS = False

# Database Features
ENABLE_USER_REGISTRATION = True
ENABLE_AUDIT_LOG = True
ENABLE_SESSION_TRACKING = True

# Demo Account (for first-time setup)
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "Admin@123"
DEMO_EMAIL = "admin@blackmeridian.local"
CREATE_DEMO_ACCOUNT = True  # Create demo account on first run