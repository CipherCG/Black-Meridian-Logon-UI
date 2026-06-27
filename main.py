#!/usr/bin/env python3
"""Black Meridian Logon UI - Main Entry Point"""

import sys
from PyQt5.QtWidgets import QApplication
from login_ui import LoginWindow
from config import APP_TITLE, APP_VERSION


def main():
    """Main application entry point"""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    app.setApplicationVersion(APP_VERSION)
    
    # Create and show login window
    login_window = LoginWindow()
    login_window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()