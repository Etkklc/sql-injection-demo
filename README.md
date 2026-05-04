# SQL Injection Demonstration and Prevention

Information Technology Course Project — Project 2

This project is a Flask application developed to practically demonstrate how SQL Injection attacks work and how they can be prevented.

## About the Project

I built two separate applications to show what SQL Injection actually does in practice. The first one is intentionally insecure — it accepts user input the wrong way and ends up running attacker-controlled SQL. The second one performs the same login function but uses modern security techniques to block the same attack. Running them side by side makes the difference between secure and insecure code very obvious.

| Application | Description | Port |
|-------------|-------------|------|
| Vulnerable App | Intentionally insecure login system | 5000 |
| Secure App | Same system protected with modern security techniques | 5001 |

The same SQL Injection attack succeeds against the vulnerable system but is completely blocked by the secure one.

## Features

- User registration and login system
- SQLite database integration
- Web-based interface using HTML and CSS
- Prepared statements as the main defense against SQL Injection
- Password hashing with bcrypt
- Input validation using regular expressions

## Technologies

| Component | Technology |
|-----------|------------|
| Programming Language | Python 3.11 |
| Web Framework | Flask 2.2.5 |
| Database | SQLite 3 |
| Password Hashing | bcrypt 3.2 |
| Frontend | HTML5 + CSS3 |

## Installation

1. Install the required libraries:

pip install flask bcrypt

2. Create the database:

python database.py

This creates the users.db file and inserts three test users with bcrypt-hashed passwords.

## Usage

Run the vulnerable system:

python vulnerable_app.py

Open in your browser: http://127.0.0.1:5000

Run the secure system:

python secure_app.py

Open in your browser: http://127.0.0.1:5001

The registration page is available only on the secure system at http://127.0.0.1:5001/register

You can run both applications at the same time in two separate terminals to compare them directly.

## SQL Injection Demonstration

To see the attack in action, try logging in to the vulnerable system with these credentials:

| Field | Value |
|-------|-------|
| Username | ' OR '1'='1' -- |
| Password | anything |

The result: you log in as admin without knowing the actual password. The single quote closes the username string, the OR clause makes the condition always true, and the double dash turns the rest of the query into a comment, skipping the password check entirely.

When you try the same input on the secure system, it returns "Invalid username" and the attack fails.

## Security Layers

The secure version uses three layers of defense.

Input validation rejects anything that isn't a clean alphanumeric username:

def is_valid_username(username):
    return bool(re.match(r'^[a-zA-Z0-9_]+$', username))

Prepared statements separate SQL code from user data, so the database never interprets input as code:

# Dangerous version
query = "SELECT * FROM users WHERE username='" + username + "'"

# Secure version
cursor.execute("SELECT * FROM users WHERE username=?", (username,))

Password hashing with bcrypt ensures that even if the database is stolen, the original passwords can't be recovered:

hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

## Project Structure

sql-injection-projesi/
├── database.py              # Database setup script
├── vulnerable_app.py        # Vulnerable application (Port 5000)
├── secure_app.py            # Secure application (Port 5001)
├── users.db                 # SQLite database
├── README.md                # This file
└── templates/
    ├── login.html           # Login page
    └── register.html        # Registration page

## Test Users

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |
| ahmet | ahmet1234 | user |
| ayse | ayse5678 | user |

These are intentionally weak passwords used only for testing. In a real application, users should be required to choose strong passwords.

## Test Scenarios

| Scenario | Vulnerable (5000) | Secure (5001) |
|----------|-------------------|---------------|
| Valid login | Successful | Successful |
| SQL Injection attempt | Attack succeeded | Attack blocked |
| Wrong password | Rejected | Rejected |
| New registration | Not available | Hashed and stored |

## Important Note

The vulnerable_app.py file is for educational purposes only. It should never be deployed in a real production environment. Its only purpose is to make the attack visible so the corresponding defenses can be understood.

## A Note on AI Assistance

I used an AI assistant (Claude, by Anthropic) as a learning tool while building this project. It helped me in several ways: explaining how SQL Injection works at a conceptual level, walking me through setting up Python, Flask, SQLite, and bcrypt on my machine, suggesting code structure for both the vulnerable and secure versions, helping me debug environment and file path issues, and assisting with the documentation.

However, every line of code in this project was reviewed, tested, and understood by me. I can explain why each security measure is in place, how the injection payload manipulates the SQL query in the vulnerable version, and why the same payload fails against prepared statements. The AI was a tutor, not a substitute — the understanding is mine.

This is in line with the academic integrity policy in the course assignment, which allows AI-assisted code as long as the student demonstrates a clear understanding of what was implemented.

## Contact

Student: [Enes Tarık Kılıç]
Course: Information Technology
Instructor: Lorik Limani, PhD Student
Submission Date: 7 May 2025