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
    list_of_tuples = c.execute("SELECT id, title, creator, genre, finished, likes, views, contributions FROM stories;").fetchall()
    list_of_stories = []
    for story in list_of_tuples:
        story = tuple_to_dictionary(story, ['id', 'title', 'author', 'genre', 'finished', 'popularity', 'views', 'contributions'])
        story["modified"] = c.execute("SELECT timestamp FROM story_0;").fetchall()[-1][0]
        list_of_stories.append(story)
    db.close()
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
    genre = genre.lower()
    for story in list_of_stories:
        storyGenre = story["genre"].replace('_', ' ')
        if storyGenre.find(genre) != -1 or genre.find(storyGenre) != -1:
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
    elif criteria == 'd':
        list_of_stories.sort(key = lambda story: story["modified"])
    return list_of_stories

#Returns a list of dictionaries containing username and fullname, matching either one to the supplied input, call with 0 arguments to get ALL users
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

#Returns a dictionary with the following keys, similar to getAllStories:
#id, author, title, genre, finished, popularity, views, contributions, cooldown, like, likes, word_limit, pieces

#like is true if user has liked the story
#likes: # of likes this story has

#Pieces is an array of dictionaries pulled from the story_ID table, each has these keys:
#contributor, version_num, timestamp, text_contributed
def getStory(story_id):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    storydict = {}
    piecesdict = {}
    list_of_piecesdict = []
    command = "SELECT contributor, version_num, timestamp, text_contributed FROM story_%s;"%(story_id)
    list_of_pieces = c.execute(command).fetchall()
    for contribute in list_of_pieces:
        piecesdict = tuple_to_dictionary(contribute, ["contributor","version_num", "timestamp", "text_contributed"])
        list_of_piecesdict.append(piecesdict)
    command = "SELECT creator, title, genre, finished, likes, views, contributions, word_limit FROM stories WHERE id = %s;"%(story_id,)
    list_of_attributes = c.execute(command).fetchone()
    storydict = tuple_to_dictionary(list_of_attributes, ["%s"%(story_id,),"author", "title", "genre", "finished", "popularity", "views", "contributions", "cooldown", "word_limit", list_of_piecesdict])
    db.commit()
    db.close()
    return storydict

    
    

#returns latest update by looking at pieces and pulling text_contributed from latest timestamp
def latestUpdate(story_id):
    dict=getStory(story_id)
    #return

#checks to see if a user conributed to the story yet    
def contributedYet(user, story_id):
    dict=getStory(story_id)
    for piece in pieces:
        if piece["contributor"]==user:
            return True
    return False

#add a contribution to a story
#def add_contribution(story_contribution, story_id):
#command = "INSERT INTO story_%d VALUES (
