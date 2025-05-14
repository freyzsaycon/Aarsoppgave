from flask import Flask, render_template, request, redirect, session
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = "sikkernøkkel"  # For session

# Koble til database
def get_db_connection():
    return mysql.connector.connect(
        host="10.2.1.177",
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

    if user and verify_password(user["password_hash"], password):
        session['user_id'] = user["id"]
        session['username'] = user["username"]  
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
            return "Brukernavn er allerede tatt, bruk et annet.", 400
        
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))  #Bruk 'password_hash' her som i databasen
        conn.commit()
        conn.close()    

        return redirect('/login')
    
    return render_template('register.html')


@app.route('/galleri')
def galleri():
    if 'user_id' not in session:
        return redirect('/login')

    username = session.get('username') 

    # Statisk bilder for galleriet
    images = [
        {"filename": "image1.jpg", "description": "Lilla blomster ved Aker Brygge (Canon 600D)"},
        {"filename": "image2.jpg", "description": "Inbetween. Bilde tatt av Frendon(Canon 600D)"},
        {"filename": "image3.jpg", "description": "Sørenga. Bilde tatt av Frendon(Canon 600D)"},
        {"filename": "image4.jpg", "description": " Maserati bil. Bilde tatt av Frendon (Canon 600D)"}
    ]
    return render_template('galleri.html', images=images, username=username)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")