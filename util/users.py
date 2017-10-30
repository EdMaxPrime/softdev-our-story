import sqlite3 #enables control of an sqlite database

db = sqlite3.connect("data/ourDB.db") #opens ourDB.db
cursor = db.cursor() #opens a cursor object

#-------------------------------------------------------------
db_name = "data/ourDB.db"

#Run once, creates the table
def create_table():
    cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, full_name TEXT, likes TEXT, contributions TEXT);")

def get_users():
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT username FROM users;"
    return c.execute(command).fetchall()

#Adds a new record to the users table    
def add_new_user(db, user, pw, name):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "INSERT INTO users VALUES ('%s', '%s', '%s', '', '');"%(user,pw,name)
    c.execute(command)
    db.commit()
    db.close()
    print 'done'

#Updates a user's username to a new one    
def update_username(old_user, new_user):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE users SET username = '%s' WHERE username = '%s';" %(new_user,old_user)
    c.execute(command)
    db.commit()
    db.close()

#Updates a user's password to a new one    
def update_password(user, old_pass, new_pass):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE users SET password = '%s' WHERE password = '%s' AND username = '%s';" %(new_pass,old_pass,user)
    c.execute(command)
    db.commit()
    db.close()

#Updates a user's fullname to a new one    
def update_fullname(user, new_name):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE users SET fullname = '%s' WHERE username = '%s';" % (new_name, user)
    c.execute(command)
    db.commit()
    db.close()

#Adds a user's contribution to the list of contributions
def add_contributions(story_id, user):
    user_prev = get_contributions(user)
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE users SET contributions = contributions || ' %s' WHERE username = '%s';" % (str(story_id), user)
    c.execute(command)
    db.commit()
    db.close()

#Retrieves all stories a user has contributed to
def get_contributions(user):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT contributions FROM users WHERE username = '%s';" %(user,)
    contributions = c.execute(command).fetchone()[0]
    db.close()
    return contributions
    
#Adds a story that a user has liked
def add_like(liked_id, user):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE users SET likes = likes || '%s ' WHERE username = '%s';"%(str(liked_id), user)
    print command
    c.execute(command)
    db.commit()
    db.close()

#Removes a story that a user has liked
def remove_like(liked_id, user):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    like_list = get_likes(user)
    like_list.pop(like_list.index(int(liked_id)))
    newlikes = ' '.join(like_list)
    command = "UPDATE users SET likes = '%s' WHERE username = '%s';"%(newlikes, user)
    c.execute(command)
    db.commit()
    db.close()

#Retrieves likes of a user
def get_likes(user):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT likes FROM users WHERE username = '%s';" %(user,)
    likes = c.execute(command).fetchone()[0]
    likes_as_list = likes.split(" ")
    likes = []
    for string in likes_as_list:
        if string.isdigit():
            likes.append(int(string))
    db.close()
    return likes

#Returns if a user has liked a given story or not
def has_user_liked(story_id, user):
    return int(story_id) in get_likes(user)

#Given a username, will retrieve the user's password and fullname
def get_user_info(c, user):
    command = "SELECT password,fullname FROM users WHERE username = '%s';" %(user) 

#Given a username and password, will return true if the two correspond, false otherwise
def validate_login(uname, pword):
    db = sqlite3.connect("data/ourDB.db")
    c = db.cursor()
    users = c.execute("SELECT password FROM users WHERE username='%s';" % (uname,)).fetchone()
    db.close()
    if users == None:
        return False
    return users[0] == pword
#create_table()
