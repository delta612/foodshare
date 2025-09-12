#!/usr/bin/env python3
import sqlite3

# Create a simple SQLite database manually
conn = sqlite3.connect('foodshare.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    profile_picture VARCHAR(255),
    bio TEXT,
    is_active BOOLEAN DEFAULT 1,
    is_admin BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create categories table
cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Insert test categories
categories = [
    ('Fruits', 'Fresh fruits and berries', '🍎'),
    ('Vegetables', 'Fresh vegetables and greens', '🥬'),
    ('Grains', 'Rice, pasta, bread, cereals', '🍞'),
    ('Dairy', 'Milk, cheese, yogurt, eggs', '🥛'),
    ('Meat', 'Chicken, beef, pork, fish', '🥩'),
    ('Prepared Food', 'Cooked meals, leftovers', '🍽️'),
    ('Baked Goods', 'Bread, pastries, desserts', '🧁'),
    ('Pantry Items', 'Canned goods, spices, condiments', '🥫'),
    ('Beverages', 'Drinks, juices, coffee, tea', '☕'),
    ('Other', 'Miscellaneous food items', '📦'),
]

for name, desc, icon in categories:
    cursor.execute('INSERT OR IGNORE INTO categories (name, description, icon) VALUES (?, ?, ?)', (name, desc, icon))

# Insert test users
from auth import get_password_hash

test_user_hash = get_password_hash("password123")
admin_user_hash = get_password_hash("admin123")

cursor.execute('''
INSERT OR IGNORE INTO users (username, email, password_hash, full_name, phone, address, city, state, zip_code, bio, is_active, is_admin)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', ('testuser', 'test@example.com', test_user_hash, 'Test User', '555-0123', '123 Test Street', 'Test City', 'Test State', '12345', 'This is a test user for development purposes', 1, 0))

cursor.execute('''
INSERT OR IGNORE INTO users (username, email, password_hash, full_name, phone, address, city, state, zip_code, bio, is_active, is_admin)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', ('admin', 'admin@example.com', admin_user_hash, 'Admin User', '555-0124', '456 Admin Avenue', 'Admin City', 'Admin State', '54321', 'This is an admin user for testing admin functionality', 1, 1))

conn.commit()
conn.close()

print("✅ Database initialized successfully!")
print("📋 Test Users Created:")
print("   Regular User: username='testuser', email='test@example.com', password='password123'")
print("   Admin User: username='admin', email='admin@example.com', password='admin123'")
