import mysql.connector


def get_con():
    TheSqlDB= mysql.connector.connect(
        host="localhost",
        user="username",
        password="pasword",
        database="nameOfDB"
    )

#def get_user():


#def get_account():

#def set_user_password():
#def set_user_username():
#def set_account_password():
#def set_account_username():
def set_user( username:str,loginPsswd: str, userID: int):
    con=get_con()
    curs=con.cursor()
    inSQL="INSERT INTO user (username,loginpsswd,userID) VALUES (%s, %s, %s)"
    curs.execute(inSQL,(username,loginPsswd,userID))
    curs.commit()
    con.close()
    curs.close()

def set_account( entryID: int, user_userID: int, serviceUsername: str,serviceName:str, serviceCategory: str, encryptPassword: str):
    con=get_con()
    curs=con.cursor()
    inSQL="INSERT INTO vault (entryID,user_userID, serviceUsername, serviceName, serviceCategory, encryptPassword) VALUES (%s, %s, %s,%s, %s, %s)"
    curs.execute(inSQL,(entryID,user_userID, serviceUsername, serviceName, serviceCategory, encryptPassword))   
    curs.commit()
    con.close()
    curs.close()   
