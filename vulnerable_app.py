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
        
        # ⚠ TEHLIKELI: String birlestirme ile SQL sorgusu
        # Bu kod SQL Injection saldirisina acik!
        query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
        
        # Olusan sorguyu terminale yazdir (egitim amacli)
        print("\n" + "="*60)
        print("Calistirilan SQL Sorgusu:")
        print(query)
        print("="*60 + "\n")
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            
            if user:
                message = f"Basarili! Hosgeldin {user[1]} (Rol: {user[3]})"
                success = True
            else:
                message = "Hatali kullanici adi veya sifre!"
        except Exception as e:
            message = f"Hata: {str(e)}"
        finally:
            conn.close()
    
    return render_template('login.html', mode='vulnerable', message=message, success=success)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("⚠  SAVUNMASIZ SISTEM CALISIYOR")
    print("Tarayicidan acin: http://127.0.0.1:5000")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)