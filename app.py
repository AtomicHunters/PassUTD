from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors, uuid
app = Flask(__name__)
app.secret_key = 'a7329ca869d9d4ac97f5a71f0e88726077de0a58b84eb6a97960990e6bc522883797a8207bebcc0fb977ca9a8f4754aa3aaf9dd2f7ce2cbf858201ed90557a20'

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
        selected_category = request.args.get('category')
        if not selected_category or selected_category == 'All':
            cursor.execute(
                'SELECT * FROM vault WHERE user_userID = %s',
                (userID,)
            )
        else:
            cursor.execute(
                'SELECT * FROM vault WHERE user_userID = %s AND serviceCategory = %s',
                (userID, selected_category)
            )
        for row in cursor.fetchall():
            passwords.append({
                "passwordID": row['entryID'],
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
        return render_template("index.html", passwords=passwords, categories=categories, show_add=True)
    if request.method == 'POST':
        passID = request.form['password_id']
        action = request.form['action']
        if passID == '' or action == '':
            return redirect(url_for('index'))
        if action == 'delete':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'DELETE FROM vault WHERE entryID = %s',
                (passID,)
            )
            mysql.connection.commit()
            return redirect(url_for('index'))
    return redirect(url_for('index'))

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
    if "userID" not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        entryID = uuid.uuid4()
        site = request.form["site"]
        username = request.form["username"]
        userID = session.get('userID')
        password = request.form["password"]
        category = request.form["category"]
        tag = request.form["tag"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO vault (entryID, user_userID, serviceUsername, serviceName, serviceCategory, encryptPassword, serviceTag)'
            'VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (entryID,userID,username,site,category,password,tag)
        )
        mysql.connection.commit()
        msg = 'Added password successfully'
        return render_template("add_password.html", msg=msg)
    return render_template("add_password.html")

@app.route("/login", methods=['GET','POST'])
def login():
    if(request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"] # hash this
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user WHERE username = %s',
            (username,)
        )
        user = cursor.fetchone()
        if(user is None): # no username in records
            msg = 'Login failed'
            return render_template('login.html',msg=msg)
        elif user['loginPsswd'] != password: # wrong password
            msg = 'Login failed'
            return render_template('login.html',msg=msg)
        else:
            session['userID'] = user['userID']
            return redirect(url_for('index'))
    return render_template('login.html') # add login.html

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"] # hash this
        password2 = request.form["confPassword"] # hash this
        if(password != password2): # password mismatch
            msg = 'Registration failed'
            return render_template('register.html',msg=msg)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO user (username, loginPsswd) VALUES (%s, %s)',
            (username, password,) # timestamp and userID auto increment
        )
        mysql.connection.commit()
        return redirect(url_for('login'))
    return render_template('register.html') # add register.html

@app.route("/logout")
def logout():
    session.clear()
    return render_template('logout.html', delay=3)

if __name__ == "__main__":
    app.run(debug=True)
