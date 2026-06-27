"""Configuration settings for Black Meridian Logon UI"""

# Application Settings
APP_TITLE = "Black Meridian Logon"
APP_VERSION = "1.0.0"

# Window Settings
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
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
MIN_PASSWORD_LENGTH = 6
MAX_USERNAME_LENGTH = 50
MAX_PASSWORD_LENGTH = 100

# Authentication
AUTH_TIMEOUT = 30  # seconds
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 300  # 5 minutes in seconds

# Demo Credentials (for testing)
# In production, implement proper authentication with a backend
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "password123"
USE_DEMO_AUTH = True  # Set to False to implement real authentication