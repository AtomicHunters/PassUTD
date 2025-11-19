from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors, uuid
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)
@app.route("/")
def index():
    # {"site": "Bank of America", "username": "alice_banking", "password": "••••••••", "category": "Banking", "tag": {"label": "Important", "color": "bg-pink-200"}}
    passwords = [
        {"site": "Bank of America", "username": "alice_banking", "password": "••••••••", "category": "Banking", "tag": {"label": "Important", "color": "bg-pink-200"}},
        {"site": "Chase", "username": "bob123", "password": "••••••••", "category": "Banking", "tag": {"label": "Work", "color": "bg-purple-200"}},
        {"site": "Facebook", "username": "alice.fb", "password": "••••••••", "category": "Social Media", "tag": {"label": "Personal", "color": "bg-green-200"}},
        {"site": "Twitter", "username": "bob_tweets", "password": "••••••••", "category": "Social Media", "tag": {"label": "Side Project", "color": "bg-yellow-200"}},
    ]
    categories = ["All", "Banking", "Social Media", "Work", "Other"]
    return render_template("index.html", passwords=passwords, categories=categories)

@app.route("/add", methods=["GET","POST"]) # currently missing login page so can't generate userIDs
def add_password():
    if request.method == "POST":
        entryID = uuid.uuid4()
        site = request.form["site"]
        username = request.form["username"]
        password = request.form["password"]
        category = request.form["category"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO vault (entryID, user_userID, serviceUsername, serviceName, serviceCategory, encryptPassword) VALUES (%s, %s, %s, %s, %s, %s)',
            (1,1234,username,site,category,password)
        )
        mysql.connection.commit()
        msg = 'Added password successfully'
        return render_template("add_password.html", msg=msg)
    return render_template("add_password.html")

if __name__ == "__main__":
    app.run(debug=True)
