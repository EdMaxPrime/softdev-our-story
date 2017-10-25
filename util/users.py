import sqlite3 #enables control of an sqlite database

db = sqlite3.connect("data/ourDB.db") #opens ourDB.db
c = db.cursor() #opens a cursor object

#-------------------------------------------------------------

#Run once, creates the table
def create_table():
    c.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, full_name TEXT, likes TEXT);")

#Adds a new record to the users table    
def add_new_user(user, pw, name):
    command = "INSERT INTO users VALUES(%s,%s,%s);"%(user,pw,name)
    c.execute(command)

#Updates a user's username to a new one    
def update_username(old_user, new_user):
    command = "UPDATE users SET username = %s WHERE username = %s;" %(new_user,old_user)
    c.execute(command)

#Updates a user's password to a new one    
def update_password(user, old_pass, new_pass):
    command = "UPDATE users SET password = %s WHERE password = %s AND username = %s;" %(new_pass,old_pass,user)
    c.execute(command)

#Updates a user's fullname to a new one    
def update_fullname(user, old_name, new_name):
    command = "UPDATE users SET fullname = %s WHERE fullname = %s AND username = %s;" %(new_name,old_name,user)
    c.execute(command)

#Given a username, will retrieve the user's password and fullname
def get_user_info(user):
    command = "SELECT password,fullname FROM users WHERE username = %s;" %(user) 