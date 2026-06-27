"""Authentication module for Black Meridian Logon UI"""

import time
import re
import bcrypt
from config import (
    MIN_USERNAME_LENGTH,
    MIN_PASSWORD_LENGTH,
    MAX_USERNAME_LENGTH,
    MAX_PASSWORD_LENGTH,
    MAX_LOGIN_ATTEMPTS,
    LOCKOUT_DURATION,
    BCRYPT_ROUNDS,
    REQUIRE_UPPERCASE,
    REQUIRE_LOWERCASE,
    REQUIRE_NUMBERS,
    REQUIRE_SPECIAL_CHARS
)
from database import DatabaseManager


def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password, password_hash):
    """Verify password against hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False


class AuthenticationManager:
    """Manages user authentication and validation with database support"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.login_attempts = 0
        self.lockout_time = None
        self.authenticated_user = None
        self.authenticated_user_id = None
    
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
        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            return False, "Username can only contain letters, numbers, underscore, and hyphen"
        
        return True, ""
    
    def validate_password(self, password):
        """Validate password strength"""
        if not password:
            return False, "Password cannot be empty"
        
        if len(password) < MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
        
        if len(password) > MAX_PASSWORD_LENGTH:
            return False, f"Password cannot exceed {MAX_PASSWORD_LENGTH} characters"
        
        # Check password complexity
        if REQUIRE_UPPERCASE and not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        
        if REQUIRE_LOWERCASE and not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        
        if REQUIRE_NUMBERS and not re.search(r"[0-9]", password):
            return False, "Password must contain at least one number"
        
        if REQUIRE_SPECIAL_CHARS and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"
        
        return True, ""
    
    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        # Check if account is locked (application-level)
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
        
        # Check database for user
        user = self.db.get_user(username)
        
        if not user:
            self.login_attempts += 1
            self.db.log_login_attempt(username, False)
            
            if self.login_attempts >= MAX_LOGIN_ATTEMPTS:
                self.lockout_time = time.time()
                return False, "Too many failed attempts. Account locked"
            
            remaining_attempts = MAX_LOGIN_ATTEMPTS - self.login_attempts
            return False, f"Invalid username or password. ({remaining_attempts} attempts remaining)"
        
        # Check if user is inactive
        if not user['is_active']:
            self.db.log_login_attempt(username, False, user['id'])
            return False, "Account is inactive. Contact administrator"
        
        # Check if user is locked in database
        if self.db.is_user_locked(username):
            return False, "Account is locked due to too many failed attempts"
        
        # Verify password
        if verify_password(password, user['password_hash']):
            # Login successful
            self.login_attempts = 0
            self.authenticated_user = username
            self.authenticated_user_id = user['id']
            
            # Update database
            self.db.update_last_login(user['id'])
            self.db.reset_failed_attempts(username)
            self.db.log_login_attempt(username, True, user['id'])
            self.db.log_audit(user['id'], username, "Login successful")
            
            return True, f"Welcome, {user.get('full_name', username)}!"
        else:
            # Login failed
            failed_count = user['failed_attempts'] + 1
            self.db.increment_failed_attempts(username)
            self.db.log_login_attempt(username, False, user['id'])
            self.db.log_audit(user['id'], username, "Login failed")
            
            if failed_count >= MAX_LOGIN_ATTEMPTS:
                self.db.lock_user(username, LOCKOUT_DURATION)
                return False, "Too many failed attempts. Account locked for 5 minutes"
            
            remaining_attempts = MAX_LOGIN_ATTEMPTS - failed_count
            return False, f"Invalid username or password. ({remaining_attempts} attempts remaining)"
    
    def register_user(self, username, password, email=None, full_name=None):
        """Register a new user"""
        # Validate inputs
        valid_user, user_msg = self.validate_username(username)
        if not valid_user:
            return False, user_msg
        
        valid_pass, pass_msg = self.validate_password(password)
        if not valid_pass:
            return False, pass_msg
        
        # Create user in database
        return self.db.create_user(username, password, email, full_name)
    
    def logout(self):
        """Logout current user"""
        if self.authenticated_user_id:
            self.db.log_audit(self.authenticated_user_id, self.authenticated_user, "Logout")
        
        self.authenticated_user = None
        self.authenticated_user_id = None
    
    def is_authenticated(self):
        """Check if user is currently authenticated"""
        return self.authenticated_user is not None
    
    def get_authenticated_user(self):
        """Get currently authenticated user"""
        return self.authenticated_user
    
    def get_authenticated_user_info(self):
        """Get full information of authenticated user"""
        if self.authenticated_user_id:
            return self.db.get_user_by_id(self.authenticated_user_id)
        return None
