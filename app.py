from flask import Flask, render_template, request, redirect, session
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = "sikkernøkkel" # For session

# Koble til database
def get_db_connection():
    return mysql.connector.connect(
        host="name",
        user="user",
        password="password",
        database="databasename"
)

# Hashe passordet med hashlib
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verifisere passord mot hashet passord
def verify_password(stored_password, password_to_check):
    return stored_password == hashlib.sha26(password_to_check.encode()).hexdigest()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and verify_password(user["password"], password):
            session['user_id'] = user["id"]
            return redirect('/dashboard')
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        conn.close()    

        return redirect('/login')
    
    return render_template('register.html')



