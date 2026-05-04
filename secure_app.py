from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import bcrypt
import re

app = Flask(__name__)

def is_valid_username(username):
    """Kullanici adi kontrolu - sadece harf, rakam, alt cizgi"""
    if not username or len(username) < 3 or len(username) > 20:
        return False
    return bool(re.match(r'^[a-zA-Z0-9_]+$', username))

@app.route('/', methods=['GET', 'POST'])
def login():
    message = None
    success = False
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # GUVENLIK 1: Input validation
        if not is_valid_username(username):
            message = "Gecersiz kullanici adi! (3-20 karakter, sadece harf/rakam/_)"
            return render_template('login.html', mode='secure', message=message, success=False)
        
        # GUVENLIK 2: Prepared statement (SQL Injection korumasi)
        query = "SELECT * FROM users WHERE username=?"
        
        print("\n" + "="*60)
        print("Calistirilan SQL Sorgusu (Prepared Statement):")
        print(f"Sorgu: {query}")
        print(f"Parametre: username={username!r}")
        print("="*60 + "\n")
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            
            # GUVENLIK 3: Bcrypt ile sifre dogrulama
            if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
                message = f"Basarili! Hosgeldin {user[1]} (Rol: {user[3]})"
                success = True
            else:
                message = "Hatali kullanici adi veya sifre!"
        except Exception as e:
            message = f"Hata: {str(e)}"
        finally:
            conn.close()
    
    return render_template('login.html', mode='secure', message=message, success=success)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    success = False
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Input validation
        if not is_valid_username(username):
            message = "Gecersiz kullanici adi! (3-20 karakter, sadece harf/rakam/_)"
            return render_template('register.html', message=message, success=False)
        
        if len(password) < 6:
            message = "Sifre en az 6 karakter olmali!"
            return render_template('register.html', message=message, success=False)
        
        # Sifreyi hashle
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                (username, hashed, 'user')
            )
            conn.commit()
            message = f"Hesap olusturuldu! Artik giris yapabilirsiniz: {username}"
            success = True
        except sqlite3.IntegrityError:
            message = "Bu kullanici adi zaten alinmis!"
        except Exception as e:
            message = f"Hata: {str(e)}"
        finally:
            conn.close()
    
    return render_template('register.html', message=message, success=success)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("✓  GUVENLI SISTEM CALISIYOR (Bonus Ozelliklerle)")
    print("Giris: http://127.0.0.1:5001")
    print("Kayit: http://127.0.0.1:5001/register")
    print("Guvenlik onlemleri:")
    print("  1. Prepared Statements (SQL Injection korumasi)")
    print("  2. bcrypt ile sifre hashleme")
    print("  3. Input validation (girdi dogrulama)")
    print("="*60 + "\n")
    app.run(debug=True, port=5001)