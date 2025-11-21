
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors, uuid
import re
import random

app = Flask(__name__)
#iintialize cursor
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'passUTD'
app.config['MYSQL_DB'] = 'mydb'


mysql = MySQL(app)
@app.route("/")
def index():
    #random userid made everytime
    userid= random.randint(1, 10000)
    add_password(userid)


    curs = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT serviceName, serviceUsername, encryptPassword, serviceCategory FROM vault WHERE user_userID = %s', (userid,))
    account = curs.fetchall()
    for x in account:
        x["site"] = x.pop("serviceName")
        x["username"] = x.pop("serviceUsername")
        x["password"] = x.pop("encryptPassword")
        x["category"] = x.pop("serviceCategory")
        x["tag"]={"label": "Side Project", "color": "bg-yellow-200"}


    passwords=account
    categories = ["All", "Banking", "Social Media"]
    return render_template("index.html", passwords=passwords, categories=categories)

@app.route("/add")
def add_password(userid:int):

#definitely revert this change
    if 1 == 1:
        entryID = uuid.uuid4()
        site = "site"
        username = "username"
        password = "passy"
        category = "Banking"
        #creating user from the data for an account to make things work for now
        set_user(username,password,userid)
        mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO vault (entryID, user_userID, serviceUsername, serviceName, serviceCategory, encryptPassword) VALUES (%s, %s, %s, %s, %s, %s)',
            (1,userid,username,site,category,password)
        )
        mysql.connection.commit()
        msg = 'Added password successfully'
        return render_template("add_password.html", msg=msg)
    return render_template("add_password.html")

def set_user( username:str,loginPsswd: str, userID: int):
    curs = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    inSQL = 'INSERT INTO user (username,loginPsswd,userID) VALUES (%s, %s, %s)'
    curs.execute(inSQL, (username, loginPsswd, userID))
    mysql.connection.commit()
    curs.close()


if __name__ == "__main__":
    app.run(debug=True)
