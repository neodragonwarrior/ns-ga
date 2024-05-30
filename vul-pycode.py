import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Hard-coded sensitive data (misconfiguration issue)
DATABASE = 'example.db'
SECRET_KEY = 'supersecretkey'  # Hard-coded sensitive data

# Database setup (misconfiguration issue: no input validation)
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/login', methods=['POST'])
def login():
    # SQL Injection vulnerability
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"message": "Login failed"}), 401

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # IDOR vulnerability
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"user": user})
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/run_command', methods=['POST'])
def run_command():
    # Command Injection vulnerability
    command = request.form['command']
    os.system(command)
    return jsonify({"message": "Command executed"})

if __name__ == '__main__':
    # Misconfiguration issue: Debug mode enabled in production
    app.run(debug=True)
