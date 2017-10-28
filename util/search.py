import sqlite3 #enables use of Sqlite3

db = sqlite3.connect("ourDB.db") # opens ourDB.db
c = db.cursor() #creates cursor object to interact with database

#-------------------------------------------------------------------
version_number = 0
db_name = "data/test.db"

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

#Returns all the stories in the master table "stories" with their metadata as a list of dictionaries
def getAllStories():
    db = sqlite3.connect(db_name)
    c = db.cursor()
    list_of_tuples = c.execute("SELECT id, title, creator, genre FROM stories;").fetchall()
    db.close()
    list_of_stories = []
    for story in list_of_tuples:
        list_of_stories.append(tuple_to_dictionary(story, ['id', 'title', 'author', 'genre']))
    return list_of_stories
    #return [{"id":0, "title":"Fairy Tale", "author":"Max"}]

#Given a tuple/list and a list of strings, will create a dictionary where the first key in the list corresponds to the first element in the tuple
def tuple_to_dictionary(tuuple, list_of_keys):
    d = {} #the dictionary
    index = 0 #the column index
    while index < len(tuuple):
        d[ list_of_keys[index] ] = tuuple[index]
        index += 1
    return d

#add a contribution to a story
#def add_contribution(story_contribution, story_id):
#command = "INSERT INTO story_%d VALUES (
