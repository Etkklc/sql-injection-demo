import sqlite3
import bcrypt

# Create the database file (if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Drop the previous table (for a clean start)
cursor.execute('DROP TABLE IF EXISTS users')

# Create the users table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
''')
PS C:\Users\user\Desktop\sql-injection-projesi>
# Test users - passwords will be stored in hashed form
test_users = [
    ('admin', 'admin123', 'admin'),
    ('ahmet', 'ahmet1234', 'user'),
    ('ayse', 'ayse5678', 'user'),
]

for username, plain_password, role in test_users:
    # Hash the password with bcrypt
    # bcrypt.gensalt() generates a random "salt" - even the same password produces a different hash each time
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    
    cursor.execute(
        'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
        (username, hashed, role)
    )

conn.commit()
conn.close()

print("Database created!")
print("Passwords are stored as bcrypt hashes.")
print("\nTest users:")
print("  - admin / admin123 (admin)")
print("  - ahmet / ahmet1234 (user)")
print("  - ayse / ayse5678 (user)")