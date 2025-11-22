from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors, uuid
from Password_hashing import hash_password, verify_password
from encryption import derive_key, encrypt_vault_entry, decrypt_vault_entry
import base64
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password' # should probably be set to a .env variable
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    # {"site": "Bank of America", "username": "alice_banking", "password": "••••••••", "category": "Banking", "tag": {"label": "Important", "color": "bg-pink-200"}}
    # {"label": "Important", "color": "bg-pink-200"}
    # {"label": "Work", "color": "bg-purple-200"}
    # {"label": "Personal", "color": "bg-green-200"}
    # {"label": "Side Project", "color": "bg-yellow-200"}
    if "userID" not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        passwords = []
        userID = session.get('userID')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM vault WHERE user_userID = %s', (userID,)
        )
        for row in cursor.fetchall():
            passwords.append({
                "id": row["entryID"],
                "site": row["serviceName"],
                "username": row["serviceUsername"],
                "password": "••••••••",
                "category": row["serviceCategory"],
                "tag": {
                    "label": row["serviceTag"],
                    "color": tag_color(row["serviceTag"])
                }
            })

    categories = ["All", "Banking", "Social Media", "Work", "Other"]
    return render_template("index.html", passwords=passwords, categories=categories)

def tag_color(tag):
    match tag:
        case 'Important':
            return "bg-pink-200"
        case 'Work':
            return "bg-purple-200"
        case 'Personal':
            return "bg-green-200"
        case 'Side Project':
            return "bg-yellow-200"
@app.route("/add", methods=['GET','POST']) # currently missing login page so can't generate userIDs
def add_password():
    if request.method == "POST":
        entryID = uuid.uuid4()
        site = request.form["site"]
        username = request.form["username"]
        userID = session.get('userID')
        vault_password = request.form["password"]
        category = request.form["category"]
        tag = request.form["tag"]

        key = base64.b64decode(session['key'])
        encrypted = encrypt_vault_entry(key, vault_password)
        ciphertext = encrypted["ciphertext"]
        nonce = encrypted["nonce"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO vault (entryID, user_userID, serviceUsername, serviceName, serviceCategory, encryptPassword, nonce, serviceTag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (entryID,userID,username,site,category,ciphertext,nonce,tag)
        )
        mysql.connection.commit()
        msg = 'Added password successfully'
        return render_template("add_password.html", msg=msg)
    return render_template("add_password.html")

@app.route("/view/<entryID>")
def view_password(entryID):
    if "userID" not in session:
        return redirect(url_for('login'))

    userID = session['userID']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT encryptPassword, nonce FROM vault WHERE entryID=%s AND user_userID=%s',
        (entryID,userID)
    )
    vault_row = cursor.fetchone()
    if vault_row is None:
        return "Entry not found", 404

    key = base64.b64decode(session['key'])
    decrypted = decrypt_vault_entry(key, {"ciphertext": vault_row["encryptPassword"],"nonce": vault_row["nonce"]})

    return render_template("view_password.html", password=decrypted)

@app.route("/login", methods=['GET','POST'])
def login():
    if(request.method == "POST"):
        username = request.form["username"]
        login_password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user WHERE username = %s',
            (username,)
        )
        user = cursor.fetchone()
        if(user is None): # no username in records
            msg = 'Login failed'
            return render_template(msg=msg)
        elif not verify_password(user['password'], login_password):  # wrong password
            msg = 'Login failed'
            return render_template(msg=msg)
        else:
            key = derive_key(login_password, user['salt'])  # derive key
            session['key'] = base64.b64encode(key).decode()
            session['userID'] = user['user_userID']
            return redirect(url_for('index'))
    return render_template()

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        login_password = request.form["password"]
        login_password2 = request.form["confPassword"]
        if(login_password != login_password2): # password mismatch
            msg = 'Registration failed'
            return render_template(msg=msg)
        salt = os.urandom(16)
        hashed = hash_password(login_password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO user (username, password, salt) VALUES (%s, %s, %s)',
            (username, hashed, salt)
        )
        mysql.connection.commit()
        return redirect(url_for('login'))
    return render_template()

if __name__ == "__main__":
    app.run(debug=True)
