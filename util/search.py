import sqlite3 #enables use of Sqlite3

db = sqlite3.connect("ourDB.db") # opens ourDB.db
c = db.cursor() #creates cursor object to interact with database

#-------------------------------------------------------------------
version_number = 0
db_name = "data/test.db"

#Returns all the stories in the master table "stories" with their metadata as a list of dictionaries
def getAllStories():
    db = sqlite3.connect(db_name)
    c = db.cursor()
    list_of_tuples = c.execute("SELECT id, title, creator, genre, finished, likes, views FROM stories;").fetchall()
    db.close()
    list_of_stories = []
    for story in list_of_tuples:
        list_of_stories.append(tuple_to_dictionary(story, ['id', 'title', 'author', 'genre', 'finished', 'popularity', 'views']))
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

#Sorts a list of dictionaries by a single letter criteria
# a: alphabetically by title, c: date created (id), v: number of views, p: number of likes
def sortby(criteria, list_of_stories):
    if criteria == 'a':
        list_of_stories.sort(key = lambda story: story["title"])
    elif criteria == 'c':
        list_of_stories.sort(key = lambda story: story["id"])
    elif criteria == 'v':
        list_of_stories.sort(key = lambda story: story["views"])
    elif criteria == 'p':
        list_of_stories.sort(key = lambda story: story["popularity"])
    return list_of_stories

def getUsers(matching=""):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = ""
    if matching != "":
        command = "SELECT username, full_name FROM users WHERE (username LIKE '%fragment%') OR (full_name LIKE '%fragment%');"
        command = command.replace("fragment", matching)
    else:
        command = "SELECT username, full_name FROM users;"
    list_of_tuples = c.execute(command).fetchall()
    db.close()
    list_of_users = []
    for user in list_of_tuples:
        list_of_users.append(tuple_to_dictionary(user, ["username", "full_name"]))
    return list_of_users

#add a contribution to a story
#def add_contribution(story_contribution, story_id):
#command = "INSERT INTO story_%d VALUES (
