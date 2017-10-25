import sqlite3 #enables use of Sqlite3

f = "data/ourDB.db"

db = sqlite3.connect(f) # opens ourDB.db
c = db.cursor() #creates cursor object to interact with database

#-------------------------------------------------------------------
version_number = 0

#Create story_id table (RUN ONCE)
def create_story_table(story_id):
    command = "CREATE TABLE story_%d (version_num INTEGER PRIMARY KEY, contributor TEXT, text_contributed TEXT, when TEXT);"%(story_id)
    c.execute(command)
    db.commit()
    
#begin a story
def modify_story(contributor, text_contributed, when, story_id):
    command = "INSERT INTO story_%d VALUES (%d, %s,%s,%s);" %(version_number,story_id, contributor, text_contributed, when)
    version_number += 1
    db.commit()

#add a contribution to a story
#def add_contribution(story_contribution, story_id):
#command = "INSERT INTO story_%d VALUES (
