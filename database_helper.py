import sqlite3
import os

DB_FILE = 'users.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Create profiles table
    c.execute('''CREATE TABLE IF NOT EXISTS profiles 
                 (name TEXT PRIMARY KEY, 
                  age INTEGER, 
                  weight REAL, 
                  height REAL, 
                  gender TEXT,
                  goal TEXT,
                  restrictions TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()


def save_profile(profile):
    """Save or update a user profile"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    try:
        c.execute('''INSERT OR REPLACE INTO profiles 
                     (name, age, weight, height, gender, goal, restrictions)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (profile['name'], profile['age'], profile['weight'], profile['height'],
                   profile['gender'], profile['goal'],
                   profile['restrictions']))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving profile: {e}")
        return False
    finally:
        conn.close()


def get_profile(name):
    """Retrieve a specific user profile"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    try:
        c.execute('SELECT name, age, weight, height, gender, goal, restrictions FROM profiles WHERE name = ?', (name,))
        profile = c.fetchone()
        return profile
    except Exception as e:
        print(f"Error retrieving profile: {e}")
        return None
    finally:
        conn.close()


def get_all_profiles():
    """Retrieve all user profiles"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    try:
        c.execute('SELECT name, age, weight, height, gender, goal, restrictions FROM profiles ORDER BY created_at DESC')
        profiles = c.fetchall()
        return profiles
    except Exception as e:
        print(f"Error retrieving profiles: {e}")
        return []
    finally:
        conn.close()


def delete_profile(name):
    """Delete a user profile"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    try:
        c.execute('DELETE FROM profiles WHERE name = ?', (name,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting profile: {e}")
        return False
    finally:
        conn.close()


def update_profile(name, **kwargs):
    """Update specific fields in a profile"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    try:
        # Build dynamic update query
        set_clause = ', '.join([f'{key} = ?' for key in kwargs.keys()])
        values = list(kwargs.values()) + [name]
        
        c.execute(f'UPDATE profiles SET {set_clause} WHERE name = ?', values)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating profile: {e}")
        return False
    finally:
        conn.close()
