#!/usr/bin/env python3
"""Black Meridian - Main Entry Point"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from login_ui import LoginWindow
from config import APP_TITLE, APP_VERSION


def get_app_icon():
    """Get application icon"""
    icon_paths = [
        os.path.join(os.path.dirname(__file__), "assets", "icon.png"),
        os.path.join(os.path.dirname(__file__), "assets", "black_meridian.png"),
    ]
    
    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            return QIcon(icon_path)
    
    # Return a default icon if no icon file exists
    return QIcon()


def main():
    """Main application entry point"""
    # Create application
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Black Meridian")
    app.setApplicationVersion(APP_VERSION)
    app.setApplicationDisplayName("Black Meridian")
    
    # Set application icon
    app_icon = get_app_icon()
    if not app_icon.isNull():
        app.setWindowIcon(app_icon)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show login window
    login_window = LoginWindow()
    login_window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
