import sqlite3
import bcrypt

# Veritabani dosyasini olustur (yoksa)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Onceki tabloyu sil (temiz baslangic icin)
cursor.execute('DROP TABLE IF EXISTS users')

# users tablosunu olustur
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
''')

# Test kullanicilari - sifreler hashlenmis olarak saklanacak
test_users = [
    ('admin', 'admin123', 'admin'),
    ('ahmet', 'ahmet1234', 'user'),
    ('ayse', 'ayse5678', 'user'),
]

for username, plain_password, role in test_users:
    # Sifreyi bcrypt ile hashle
    # bcrypt.gensalt() rastgele bir "tuz" uretir, ayni sifre bile her seferinde farkli hash uretir
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    
    cursor.execute(
        'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
        (username, hashed, role)
    )

conn.commit()
conn.close()

print("Veritabani olusturuldu!")
print("Sifreler bcrypt ile hashlenmis halde saklaniyor.")
print("\nTest kullanicilari:")
print("  - admin / admin123 (admin)")
print("  - ahmet / ahmet1234 (user)")
print("  - ayse / ayse5678 (user)")