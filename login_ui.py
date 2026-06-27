"""Login UI Module for Black Meridian"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_RESIZABLE,
    BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, ERROR_COLOR,
    SUCCESS_COLOR, FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    FONT_SIZE_INPUT, FONT_SIZE_BUTTON, BORDER_COLOR
)
from auth import AuthenticationManager
import os


class LoginWindow(QMainWindow):
    """Main login window for Black Meridian"""
    
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthenticationManager()
        self.init_ui()
        self.apply_stylesheet()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Window settings
        self.setWindowTitle("Black Meridian")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Set resizable property
        if not WINDOW_RESIZABLE:
            self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.setWindowIcon(self.get_icon())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 40, 30, 40)
        main_layout.setSpacing(20)
        
        # Title
        title = QLabel("Black Meridian")
        title_font = QFont(FONT_FAMILY, FONT_SIZE_TITLE, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Secure Authentication System")
        subtitle_font = QFont(FONT_FAMILY, 10)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: {PRIMARY_COLOR};")
        main_layout.addWidget(subtitle)
        
        # Username section
        username_label = QLabel("Username:")
        username_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_LABEL))
        main_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFont(QFont(FONT_FAMILY, FONT_SIZE_INPUT))
        self.username_input.setMinimumHeight(35)
        main_layout.addWidget(self.username_input)
        
        # Password section
        password_label = QLabel("Password:")
        password_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_LABEL))
        main_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont(FONT_FAMILY, FONT_SIZE_INPUT))
        self.password_input.setMinimumHeight(35)
        main_layout.addWidget(self.password_input)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont(FONT_FAMILY, FONT_SIZE_BUTTON, QFont.Bold))
        self.login_button.setMinimumHeight(40)
        self.login_button.clicked.connect(self.on_login_clicked)
        button_layout.addWidget(self.login_button)
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFont(QFont(FONT_FAMILY, FONT_SIZE_BUTTON))
        self.clear_button.setMinimumHeight(40)
        self.clear_button.clicked.connect(self.on_clear_clicked)
        button_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready to login")
        self.status_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_LABEL))
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        main_layout.addStretch()
        central_widget.setLayout(main_layout)
        
        # Connect enter key to login
        self.password_input.returnPressed.connect(self.on_login_clicked)
    
    def get_icon(self):
        """Get window icon"""
        icon_paths = [
            os.path.join(os.path.dirname(__file__), "assets", "icon.png"),
            os.path.join(os.path.dirname(__file__), "assets", "black_meridian.png"),
        ]
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                return QIcon(icon_path)
        
        return QIcon()
    
    def apply_stylesheet(self):
        """Apply custom stylesheet"""
        stylesheet = f"""
        QMainWindow {{
            background-color: {BACKGROUND_COLOR};
        }}
        
        QLabel {{
            color: {TEXT_COLOR};
        }}
        
        QLineEdit {{
            background-color: #2d2d2d;
            color: {TEXT_COLOR};
            border: 2px solid {BORDER_COLOR};
            border-radius: 5px;
            padding: 5px;
            font-size: 11pt;
        }}
        
        QLineEdit:focus {{
            border: 2px solid {PRIMARY_COLOR};
        }}
        
        QPushButton {{
            background-color: {PRIMARY_COLOR};
            color: {TEXT_COLOR};
            border: none;
            border-radius: 5px;
            font-weight: bold;
            padding: 8px;
        }}
        
        QPushButton:hover {{
            background-color: #1565c0;
        }}
        
        QPushButton:pressed {{
            background-color: #0d47a1;
        }}
        """
        self.setStyleSheet(stylesheet)
    
    def on_login_clicked(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        # Attempt authentication
        success, message = self.auth_manager.authenticate(username, password)
        
        if success:
            self.status_label.setText("Login successful!")
            self.status_label.setStyleSheet(f"color: {SUCCESS_COLOR};")
            
            # Clear inputs
            self.username_input.clear()
            self.password_input.clear()
            
            # Show success message
            user_info = self.auth_manager.get_authenticated_user_info()
            welcome_msg = user_info.get('full_name', username) if user_info else username
            QMessageBox.information(self, "Black Meridian", f"Welcome, {welcome_msg}!")
            
            # Reset status after 2 seconds
            QTimer.singleShot(2000, self.reset_status)
        else:
            self.status_label.setText(message)
            self.status_label.setStyleSheet(f"color: {ERROR_COLOR};")
            self.password_input.clear()
    
    def on_clear_clicked(self):
        """Handle clear button click"""
        self.username_input.clear()
        self.password_input.clear()
        self.reset_status()
    
    def reset_status(self):
        """Reset status label"""
        self.status_label.setText("Ready to login")
        self.status_label.setStyleSheet(f"color: {TEXT_COLOR};")
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
