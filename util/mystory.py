import sqlite3 #enables control of Sqlite3

db_name = "data/test.db"

#--------------------------------------------------------------

#Create stories table
def create_stories_table():
    c.execute("CREATE TABLE AllStories (title TEXT, creator TEXT, id INTERGER PRIMARY KEY, genre TEXT, word_limit INTEGER, cooldown INTEGER, contributions INTEGER, finished BOOLEAN, likes INTEGER, views INTEGER);")

#Update various fields
def update_title(story_id,new_title):
    command = "UPDATE AllStories SET title = %s WHERE id = %d" % (new_title, story_id)
    c.execute(command)
    db.commit()

def update_genre(story_id,new_genre):
    command = "UPDATE AllStories SET genre = %s WHERE id = %d" % (new_genre, story_id)
    c.execute(command)
    db.commit()

def update_word_limit(story_id,new_limit):
    command = "UPDATE AllStories SET word_limit = %d WHERE id = %d" % (new_limit, story_id)
    c.execute(command)
    db.commit()

def update_cooldown(story_id,new_cd):
    command = "UPDATE AllStories SET cooldown = %d WHERE id = %d" % (new_cd, story_id)
    c.execute(command)
    db.commit()

def update_contributions(story_id,new_contribution):
    command = "UPDATE AllStories SET contributions = %d WHERE id = %d" % (new_contribution, story_id)
    c.execute(command)
    db.commit()

def update_finished(story_id):
    command = "UPDATE AllStories SET finished = ~finished WHERE id = %d" % (story_id)
    c.execute(command)
    db.commit()

def update_likes(story_id,new_likes):
    command = "UPDATE AllStories SET likes = %d WHERE id = %d" % (new_likes, story_id)
    c.execute(command)
    db.commit()

def update_views(story_id,new_viewcount):
    command = "UPDATE AllStories SET views = %d WHERE id = %d" % (new_viewcount, story_id)
    c.execute(command)
    db.commit()

#Add a new story to the table
def add_new_story(new_title, started_creator, selected_genre, word_lim, cooldown):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT MAX(id) FROM stories;"
    result = c.execute(command).fetchone()[0]
    id = 0
    if result:
        id = result + 1
    command = "INSERT INTO stories VALUES('%s', '%s', %d, '%s', %d, %d, 0, 0, 0, 0);"%(new_title, started_creator, id, selected_genre, word_lim, cooldown)
    c.execute(command)
    command = "CREATE TABLE story_%d (version_num INTEGER PRIMARY KEY, contributor TEXT, text_contributed TEXT, timestamp TEXT);" % (id,)
    c.execute(command)
    db.commit()
    db.close()
