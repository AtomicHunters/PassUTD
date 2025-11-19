import mysql.connector


def get_con():
    TheSqlDB= mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="root",
        database="mydb"
    )
    return TheSqlDB

#def get_user(): finds user
#con=get_con()
#curs=con.cursor()
#may have to call to get username and password from html front end
#inSQL="SELECT user (username,loginpsswd) VALUES (%s, %s)"
#curs.execute(inSQL,(username,loginPsswd,userID))
#curs.commit()
#curs.close()
#con.close()


#def get_account(): finds account
#con=get_con()
#curs=con.cursor()
#inSQL="SELECT account ("what do i use to look for, user and service?") VALUES (%s, %s)"
#curs.execute(inSQL,(username,loginPsswd,userID))
#curs.commit()
#curs.close()
#con.close()


#def set_user_password():
#def set_user_username(): used for login to maanager

#def set_account_password():
#con=get_con()
#curs=con.cursor()
#inSQL="SELECT user (username,loginpsswd) VALUES (%s, %s)"
#curs.execute(inSQL,(username,loginPsswd,userID))
#curs.commit()
#curs.close()
#con.close()


#def set_account_username(): what is used for account login
#con=get_con()
#curs=con.cursor()
#inSQL="SELECT user (username,loginpsswd) VALUES (%s, %s)"
#curs.execute(inSQL,(username,loginPsswd,userID))
#curs.commit()
#curs.close()
#con.close()


def set_user( username:str,loginPsswd: str, userID: int):
    con=get_con()
    curs=con.cursor()
    inSQL="INSERT INTO 'user' (username,loginPsswd,userID) VALUES (%s, %s, %s)"
    curs.execute(inSQL,(username,loginPsswd,userID))
    curs.commit()
    curs.close()
    con.close()

def set_account( entryID: int, user_userID: int, serviceUsername: str,serviceName:str, serviceCategory: str, encryptPassword: str):
    con=get_con()
    curs=con.cursor()
    inSQL="INSERT INTO vault (entryID,user_userID, serviceUsername, serviceName, serviceCategory, encryptPassword) VALUES (%s, %s, %s,%s, %s, %s)"
    curs.execute(inSQL,(entryID, user_userID, serviceUsername, serviceName, serviceCategory, encryptPassword))   
    curs.commit()
    curs.close()
    con.close()  
