from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    message = None
    success = False
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # WARNING: DANGEROUS - Building SQL query with string concatenation
        # This code is vulnerable to SQL Injection attacks!
        query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
        
        # Print the resulting query to terminal (for educational purposes)
        print("\n" + "="*60)
        print("Executed SQL Query:")
        print(query)
        print("="*60 + "\n")
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            
            if user:
                message = f"Success! Welcome {user[1]} (Role: {user[3]})"
                success = True
            else:
                message = "Invalid username or password!"
        except Exception as e:
            message = f"Error: {str(e)}"
        finally:
            conn.close()
    
    return render_template('login.html', mode='vulnerable', message=message, success=success)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("WARNING: VULNERABLE SYSTEM RUNNING")
    print("Open in browser: http://127.0.0.1:5000")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)