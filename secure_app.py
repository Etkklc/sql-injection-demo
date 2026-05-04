from flask import Flask, render_template, request
import sqlite3
import bcrypt
import re

app = Flask(__name__)

def is_valid_username(username):
    """Username validation - only letters, digits, and underscore allowed"""
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
        
        # SECURITY 1: Input validation
        if not is_valid_username(username):
            message = "Invalid username! (3-20 characters, only letters/digits/_)"
            return render_template('login.html', mode='secure', message=message, success=False)
        
        # SECURITY 2: Prepared statement (SQL Injection protection)
        query = "SELECT * FROM users WHERE username=?"
        
        print("\n" + "="*60)
        print("Executed SQL Query (Prepared Statement):")
        print(f"Query: {query}")
        print(f"Parameter: username={username!r}")
        print("="*60 + "\n")
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            
            # SECURITY 3: Password verification with bcrypt
            if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
                message = f"Success! Welcome {user[1]} (Role: {user[3]})"
                success = True
            else:
                message = "Invalid username or password!"
        except Exception as e:
            message = f"Error: {str(e)}"
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
            message = "Invalid username! (3-20 characters, only letters/digits/_)"
            return render_template('register.html', message=message, success=False)
        
        if len(password) < 6:
            message = "Password must be at least 6 characters!"
            return render_template('register.html', message=message, success=False)
        
        # Hash the password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                (username, hashed, 'user')
            )
            conn.commit()
            message = f"Account created! You can now log in: {username}"
            success = True
        except sqlite3.IntegrityError:
            message = "This username is already taken!"
        except Exception as e:
            message = f"Error: {str(e)}"
        finally:
            conn.close()
    
    return render_template('register.html', message=message, success=success)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SECURE SYSTEM RUNNING (with Bonus Features)")
    print("Login: http://127.0.0.1:5001")
    print("Register: http://127.0.0.1:5001/register")
    print("Security measures:")
    print("  1. Prepared Statements (SQL Injection protection)")
    print("  2. Password hashing with bcrypt")
    print("  3. Input validation")
    print("="*60 + "\n")
    app.run(debug=True, port=5001)