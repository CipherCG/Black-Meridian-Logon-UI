"""Database module for Black Meridian"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path
from config import DB_FILE, DB_PATH, DB_BACKUP_DIR, CREATE_DEMO_ACCOUNTS, DEMO_ACCOUNTS


class DatabaseManager:
    """Manages SQLite database operations"""
    
    def __init__(self):
        self.db_path = DB_FILE
        self._ensure_db_directory()
        self._initialize_database()
    
    def _ensure_db_directory(self):
        """Ensure database directory exists"""
        Path(DB_PATH).mkdir(parents=True, exist_ok=True)
        Path(DB_BACKUP_DIR).mkdir(parents=True, exist_ok=True)
    
    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _initialize_database(self):
        """Initialize database with required tables"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT UNIQUE,
                    full_name TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    is_admin BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    failed_attempts INTEGER DEFAULT 0,
                    is_locked BOOLEAN DEFAULT 0,
                    locked_until TIMESTAMP
                )
            ''')
            
            # Login attempts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS login_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT NOT NULL,
                    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success BOOLEAN NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Audit log table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Create indices for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_login_attempts_user ON login_attempts(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id)')
            
            conn.commit()
            
            # Create demo accounts if needed
            if CREATE_DEMO_ACCOUNTS:
                for account in DEMO_ACCOUNTS:
                    if not self.user_exists(account['username']):
                        self.create_user(
                            username=account['username'],
                            password=account['password'],
                            email=account['email'],
                            full_name=account['full_name'],
                            is_admin=account['is_admin']
                        )
        
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
        
        finally:
            conn.close()
    
    def user_exists(self, username):
        """Check if user exists"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            return cursor.fetchone() is not None
        finally:
            conn.close()
    
    def create_user(self, username, password, email=None, full_name=None, is_admin=False):
        """Create a new user"""
        from auth import hash_password
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, full_name, is_admin, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            ''', (username, password_hash, email, full_name, is_admin))
            
            conn.commit()
            self.log_audit(None, username, f"User created", f"Admin user: {is_admin}")
            return True, "User created successfully"
        
        except sqlite3.IntegrityError:
            return False, "Username or email already exists"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()
    
    def get_user(self, username):
        """Get user by username"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    def update_last_login(self, user_id):
        """Update last login timestamp"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user_id,))
            conn.commit()
        finally:
            conn.close()
    
    def increment_failed_attempts(self, username):
        """Increment failed login attempts"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username = ?
            ''', (username,))
            conn.commit()
        finally:
            conn.close()
    
    def reset_failed_attempts(self, username):
        """Reset failed login attempts after successful login"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET failed_attempts = 0, is_locked = 0 WHERE username = ?
            ''', (username,))
            conn.commit()
        finally:
            conn.close()
    
    def lock_user(self, username, duration_seconds):
        """Lock user account"""
        from datetime import datetime, timedelta
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            locked_until = datetime.now() + timedelta(seconds=duration_seconds)
            cursor.execute('''
                UPDATE users SET is_locked = 1, locked_until = ? WHERE username = ?
            ''', (locked_until, username))
            conn.commit()
        finally:
            conn.close()
    
    def is_user_locked(self, username):
        """Check if user is locked"""
        from datetime import datetime
        
        user = self.get_user(username)
        if not user or not user['is_locked']:
            return False
        
        if user['locked_until']:
            locked_until = datetime.fromisoformat(user['locked_until'])
            if datetime.now() > locked_until:
                self.reset_failed_attempts(username)
                return False
        
        return True
    
    def log_login_attempt(self, username, success, user_id=None, ip_address=None, user_agent=None):
        """Log login attempt"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO login_attempts (user_id, username, success, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, success, ip_address, user_agent))
            conn.commit()
        finally:
            conn.close()
    
    def log_audit(self, user_id, username, action, details=None):
        """Log audit event"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO audit_log (user_id, username, action, details)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, action, details))
            conn.commit()
        finally:
            conn.close()
    
    def get_login_history(self, username, limit=10):
        """Get login history for a user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM login_attempts 
                WHERE username = ? 
                ORDER BY attempt_time DESC 
                LIMIT ?
            ''', (username, limit))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def get_all_users(self, include_inactive=False):
        """Get all users"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            if include_inactive:
                cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
            else:
                cursor.execute('SELECT * FROM users WHERE is_active = 1 ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def delete_user(self, user_id):
        """Soft delete user (mark as inactive)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('UPDATE users SET is_active = 0 WHERE id = ?', (user_id,))
            conn.commit()
            return True
        finally:
            conn.close()
    
    def backup_database(self):
        """Create database backup"""
        import shutil
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(DB_BACKUP_DIR, f"logon_{timestamp}.db")
        
        try:
            shutil.copy2(self.db_path, backup_file)
            return True, backup_file
        except Exception as e:
            return False, str(e)
