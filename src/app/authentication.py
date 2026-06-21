"""
automation/auth.py — Secure Authentication Backend
==================================================
Provides SQLite database integration and PBKDF2 cryptographic hashing
for secure user registration and login validation.
"""

import os
import sqlite3
import hashlib
import secrets
from pathlib import Path

# Define database path
DB_PATH = Path("automation/users.db")

def _hash_password(password: str, salt: str) -> str:
    """Hashes a password using PBKDF2 HMAC with SHA-256."""
    key = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    )
    return key.hex()

def init_db():
    """Initializes the SQLite database and creates the users table if it doesn't exist."""
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT DEFAULT 'Viewer'
        )
    ''')
    
    # Auto-seed default admin user if it doesn't exist
    cursor.execute('SELECT COUNT(*) FROM users WHERE email = ?', ('admin@readynest.com',))
    if cursor.fetchone()[0] == 0:
        salt = secrets.token_hex(16)
        password_hash = _hash_password('admin', salt)
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, salt, role) VALUES (?, ?, ?, ?, ?)",
            ('Admin User', 'admin@readynest.com', password_hash, salt, 'Admin')
        )
        
    conn.commit()
    conn.close()

def register_user(name: str, email: str, password: str, role: str = 'Admin') -> tuple[bool, str]:
    """Registers a new user. Returns (Success_Boolean, Message)."""
    init_db()
    email = email.lower().strip()
    
    # Generate cryptographic salt
    salt = secrets.token_hex(16)
    password_hash = _hash_password(password, salt)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, salt, role) VALUES (?, ?, ?, ?, ?)",
            (name, email, password_hash, salt, role)
        )
        conn.commit()
        conn.close()
        return True, "User registered successfully."
    except sqlite3.IntegrityError:
        return False, "Email address is already registered."
    except Exception as e:
        return False, f"Database error: {str(e)}"

def verify_login(email: str, password: str) -> dict | None:
    """Verifies user credentials. Returns a dictionary of user data if successful, else None."""
    init_db()
    email = email.lower().strip()
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return None
        
    # Re-hash provided password with the stored salt
    stored_hash = user['password_hash']
    stored_salt = user['salt']
    computed_hash = _hash_password(password, stored_salt)
    
    if computed_hash == stored_hash:
        return {
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "role": user['role']
        }
    return None
