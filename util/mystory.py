import sqlite3 #enables control of Sqlite3
from users import add_contributions
db_name = "data/test.db"

#--------------------------------------------------------------

#Create stories table
def create_stories_table():
    c.execute("CREATE TABLE AllStories (title TEXT, creator TEXT, id INTERGER PRIMARY KEY, genre TEXT, word_limit INTEGER, cooldown INTEGER, contributions INTEGER, finished BOOLEAN, likes INTEGER, views INTEGER);")

#Returns true if story exists, false if not
def story_exists(story_id):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT name FROM sqlite_master WHERE type='table' AND name='story_%d';"%(int(story_id))
    result = c.execute(command).fetchall()
    db.commit()
    db.close()
    if result:
        return True
    else:
        return False

#Update various fields
def update_title(story_id,new_title):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE AllStories SET title = %s WHERE id = %d" % (new_title, story_id)
    c.execute(command)
    db.commit()
    db.close()

def update_genre(story_id,new_genre):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE AllStories SET genre = %s WHERE id = %d" % (new_genre, story_id)
    c.execute(command)
    db.commit()
    db.close()

def update_word_limit(story_id,new_limit):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE AllStories SET word_limit = %d WHERE id = %d" % (new_limit, story_id)
    c.execute(command)
    db.commit()
    db.close()

def update_cooldown(story_id,new_cd):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE AllStories SET cooldown = %d WHERE id = %d" % (new_cd, story_id)
    c.execute(command)
    db.commit()
    db.close()

#Adds one to the total number of contributions to this story, used by modify_story, don't call on your own
def update_contributions(story_id):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT contributions FROM stories WHERE id = %d;" % (story_id,)
    total = c.execute(command).fetchone()[0] + 1
    command = "UPDATE stories SET contributions = %d WHERE id = %d;" % (total, story_id)
    c.execute(command)
    db.commit()
    db.close()
    return total

#Returns true if contributed, false otherwise
def has_contributed(story_id, username):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT * FROM story_%d WHERE contributor = '%s';" % (story_id, username)
    contributions = len(c.execute(command).fetchall())
    db.close()
    return contributions > 0

#Toggles the status of a story, either finished->unfinished or unfinished->finished
def update_finished(story_id):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE stories SET finished = ~finished WHERE id = " + story_id + ";"
    c.execute(command)
    db.commit()
    db.close()

#Returns true if the story is finished, false otherwise
def is_finished(story_id):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT finished FROM stories WHERE id = " + story_id + ";"
    status = c.execute(command).fetchone()[0]
    db.close()
    return status == 1

# Expects the story ID and either +1(new like) or -1(unlike) for delta
def update_likes(story_id, delta):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE stories SET likes = likes + %d WHERE id = %s;" % (delta, story_id)
    c.execute(command)
    db.commit()
    db.close()

def get_likes(story_id):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT likes FROM stories WHERE id = " + story_id + ";"
    likes = c.execute(command).fetchone()[0]
    db.close()
    return likes

#Adds 1 view to the total
def update_views(story_id):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE stories SET views = views + 1 WHERE id = " + story_id + ";"
    c.execute(command)
    db.commit()
    db.close()

#Returns the number of views this story has
def get_views(story_id):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT views FROM stories WHERE id = " + story_id + ";"
    views = c.execute(command).fetchone()[0]
    db.close()
    return views

#Add a new story to the table
def add_new_story(new_title, started_creator, selected_genre, word_lim, cooldown):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT MAX(id) FROM stories;"
    result = c.execute(command).fetchone()[0]
    id = 0
    if result:
        id = result + 1
    command = "INSERT INTO stories VALUES('%s', '%s', %d, '%s', %d, %d, 1, 0, 0, 0);"%(new_title, started_creator, id, selected_genre, int(word_lim), cooldown)
    c.execute(command)
    command = "CREATE TABLE story_%d (version_num INTEGER PRIMARY KEY, contributor TEXT, text_contributed TEXT, timestamp TEXT);" % (id,)
    c.execute(command)
    db.commit()
    db.close()
    return id

def idNow():
    db = sqlite3.connect(db_name)
    command = "SELECT MAX(id) FROM stories;"
    c = db.cursor()
    result = c.execute(command).fetchone()[0]
    id = 0
    if result:
        return result

#add contribution to a story
def modify_story(contributor, text_contributed, story_id):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT contributions FROM stories WHERE id = %d;" % (story_id,)
    version_num = c.execute(command).fetchone()[0]
    command = "INSERT INTO story_%d VALUES (%d, '%s', '%s', datetime('now'));" %(story_id, version_num, contributor, text_contributed)
    c.execute(command)
    db.commit()
    db.close()
    #add_contributions(story_id, user)
    add_contributions(story_id, contributor)
    update_contributions(story_id) #add 1 to the total

