"""Authentication module for Black Meridian Logon UI"""

import time
from config import (
    MIN_USERNAME_LENGTH,
    MIN_PASSWORD_LENGTH,
    MAX_USERNAME_LENGTH,
    MAX_PASSWORD_LENGTH,
    MAX_LOGIN_ATTEMPTS,
    LOCKOUT_DURATION,
    DEMO_USERNAME,
    DEMO_PASSWORD,
    USE_DEMO_AUTH
)


class AuthenticationManager:
    """Manages user authentication and validation"""
    
    def __init__(self):
        self.login_attempts = 0
        self.lockout_time = None
        self.authenticated_user = None
    
    def is_locked_out(self):
        """Check if account is locked due to failed attempts"""
        if self.lockout_time is None:
            return False
        
        elapsed = time.time() - self.lockout_time
        if elapsed >= LOCKOUT_DURATION:
            self.lockout_time = None
            self.login_attempts = 0
            return False
        
        return True
    
    def get_lockout_remaining(self):
        """Get remaining lockout time in seconds"""
        if self.lockout_time is None:
            return 0
        
        elapsed = time.time() - self.lockout_time
        remaining = LOCKOUT_DURATION - elapsed
        return max(0, int(remaining))
    
    def validate_username(self, username):
        """Validate username format"""
        if not username:
            return False, "Username cannot be empty"
        
        if len(username) < MIN_USERNAME_LENGTH:
            return False, f"Username must be at least {MIN_USERNAME_LENGTH} characters"
        
        if len(username) > MAX_USERNAME_LENGTH:
            return False, f"Username cannot exceed {MAX_USERNAME_LENGTH} characters"
        
        # Allow alphanumeric, underscore, and hyphen
        import re
        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            return False, "Username can only contain letters, numbers, underscore, and hyphen"
        
        return True, ""
    
    def validate_password(self, password):
        """Validate password format"""
        if not password:
            return False, "Password cannot be empty"
        
        if len(password) < MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
        
        if len(password) > MAX_PASSWORD_LENGTH:
            return False, f"Password cannot exceed {MAX_PASSWORD_LENGTH} characters"
        
        return True, ""
    
    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        # Check if account is locked
        if self.is_locked_out():
            remaining = self.get_lockout_remaining()
            return False, f"Account locked. Try again in {remaining} seconds"
        
        # Validate inputs
        valid_user, user_msg = self.validate_username(username)
        if not valid_user:
            return False, user_msg
        
        valid_pass, pass_msg = self.validate_password(password)
        if not valid_pass:
            return False, pass_msg
        
        # Check credentials
        if USE_DEMO_AUTH:
            # Demo authentication
            if username == DEMO_USERNAME and password == DEMO_PASSWORD:
                self.login_attempts = 0
                self.authenticated_user = username
                return True, "Login successful"
            else:
                self.login_attempts += 1
                remaining_attempts = MAX_LOGIN_ATTEMPTS - self.login_attempts
                
                if self.login_attempts >= MAX_LOGIN_ATTEMPTS:
                    self.lockout_time = time.time()
                    return False, "Too many failed attempts. Account locked"
                
                return False, f"Invalid username or password. ({remaining_attempts} attempts remaining)"
        else:
            # TODO: Implement real authentication with backend
            # This could connect to LDAP, database, etc.
            return False, "Real authentication not yet implemented"
    
    def logout(self):
        """Logout current user"""
        self.authenticated_user = None
    
    def is_authenticated(self):
        """Check if user is currently authenticated"""
        return self.authenticated_user is not None
    
    def get_authenticated_user(self):
        """Get currently authenticated user"""
        return self.authenticated_user