import sqlite3 #enables use of Sqlite3

db = sqlite3.connect("ourDB.db") # opens ourDB.db
c = db.cursor() #creates cursor object to interact with database

#-------------------------------------------------------------------
version_number = 0
db_name = "data/test.db"
    
#begin a story
def modify_story(contributor, text_contributed, when, story_id):
    command = "INSERT INTO story_%d VALUES (%d, %s,%s,%s);" %(version_number,story_id, contributor, text_contributed, when)
    version_number += 1
    db.commit()

#Returns all the stories in the master table "stories" with their metadata as a list of dictionaries
def getAllStories():
    db = sqlite3.connect(db_name)
    c = db.cursor()
    list_of_tuples = c.execute("SELECT id, title, creator, genre, finished FROM stories;").fetchall()
    db.close()
    list_of_stories = []
    for story in list_of_tuples:
        list_of_stories.append(tuple_to_dictionary(story, ['id', 'title', 'author', 'genre', 'finished']))
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

#Filters a list of dictionaries, returning a list of those that contain the fragment in their title
def filter_by_title(fragment, list_of_stories):
    results = []
    for story in list_of_stories:
        if story["title"].find(fragment) != -1:
            results.append(story)
    return results

#Filters a list of dictionaries, returning a list of those that contain the specified genre
def filter_by_genre(genre, list_of_stories):
    results = []
    genre = genre.replace(' ', '_').lower()
    for story in list_of_stories:
        if story["genre"].find(genre) != -1:
            results.append(story)
    return results

#Filters a list of dictionaries, returning a list of those that have this author
def filter_by_author(author, list_of_stories):
    results = []
    for story in list_of_stories:
        if story["author"].find(author) != -1:
            results.append(story)
    return results

#Filters a list of dictionaries, returning a list of those that are finished/unfinished or both
def filter_by_status(status, list_of_stories):
    results = []
    if status == "all":
        return list_of_stories
    elif status == "finished":
        status = 1
    elif status == "unfinished":
        status = 0
    for story in list_of_stories:
        if story["finished"] == status:
            results.append(story)
    return results

#add a contribution to a story
#def add_contribution(story_contribution, story_id):
#command = "INSERT INTO story_%d VALUES (
