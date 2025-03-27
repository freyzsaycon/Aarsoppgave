from flask import Flask, render_template, request, redirect, session
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = "sikkernøkkel"  # For session

# Koble til database
def get_db_connection():
    return mysql.connector.connect(
        host="10.2.2.14",
        user="frendon",
        password="MariaJa81",
        database="galleridb"
    )

# Hashe passordet med hashlib
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verifisere det hashende passordet
def verify_password(stored_password, password_to_check):
    return stored_password == hashlib.sha256(password_to_check.encode()).hexdigest()

@app.route('/')
def home():
    return render_template('login.html')

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

        if user and verify_password(user["password_hash"], password):  # Bruke det hasha passordet her
            session['user_id'] = user["id"]
            return redirect('/galleri')
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        # Sjekker hvis brukernavnet er brukt
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Username already taken, please choose another", 400
        
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))  # Use 'password_hash' here
        conn.commit()
        conn.close()    

        return redirect('/login')
    
    return render_template('register.html')


@app.route('/galleri')
def galleri():
    if 'user_id' not in session:
        return redirect('/login')

    # Statisk bilder for galleriet
    images = ['image1.jpg', 'image2.jpg', 'image3.jpg']
    
    return render_template('galleri.html', images=images)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")