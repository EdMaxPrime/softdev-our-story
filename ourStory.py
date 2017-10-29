from flask import Flask, flash, render_template, request, session, redirect, url_for
import sqlite3
import util.users as users
import util.search as search
import util.mystory as mystory


app = Flask(__name__)
app.secret_key = "THIS IS NOT SECURE"

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('stories_route'))
    else:
        return render_template('form.html', title = 'OurStory Website')

@app.route('/help')
def help():
    return

@app.route('/login', methods=['POST','GET'])
def login():
    db = sqlite3.connect("data/ourDB.db") #opens ourDB.db
    c = db.cursor() #opens a cursor object
    #print request.form['user']
    user = request.form['user']
    print user
    command = "SELECT password FROM users WHERE username='%s';"%(user)
    print command
    c.execute(command)
    credentials = c.fetchall()
    print credentials
    db.close()
    print users.validate_login(user, request.form["password"])
    if credentials:
        password = credentials[0][0]
        if request.form['password'] == password:
            session['user'] = request.form['user']
            return redirect(url_for('stories_route'))
        else:
            flash("Sorry, wrong password and/or username")
    else:
        flash("User not found")
    return redirect(url_for('home'))

@app.route('/join')
def join():
    return render_template("join.html")

@app.route('/joinRedirect', methods=['POST','GET'])
def joinRedirect():
    db = sqlite3.connect("data/ourDB.db") #opens ourDB.db
    if request.form['password'] == request.form['passwordConfirm']:
        users.add_new_user(db, request.form['user'], request.form['password'], request.form['name'])
        db.commit()
        session['user'] = request.form['user']
        return redirect(url_for('stories_route'))
    else:
        flash("Passwords do not match")
    return redirect(url_for('join'))
    

@app.route('/stories')
def stories_route():
    return render_template("list.html", page_title="Stories", listStories=search.getAllStories())

##DIDNT TEST YET
@app.route('/story', methods = ['GET'])
def story_route():
    #return render_template("invalid.html") when story?id=blah doesn't exist in db
    storyId=request.args.get("id","")
    dictStoryInfo=search.getStory(storyId)
    if 'user' in session: #check if user is logged in
        user=session["user"]
        if dictStoryInfo["finished"]: #check if story is finished
            return render_template("fullStory.html", likes=dictStoryInfo["popularity"], title=dictStoryInfo["title"], author=dictStoryInfo["author"], genre=dictStoryInfo["genre"],id=dictStoryInfo["id"], pieces=dictStoryInfo["pieces"]) 
        else: #story is not finished  
            if not search.contributedYet(user, storyId): #user did not contribute yet, so user is directed to edit the story
               return render_template("editStory.html",title=dictStoryInfo["title"],lastUpdate=search.latestUpdate(storyId),charLimit=dictStoryInfo["word_limit"])
            else: #user has already contributed, so show story
               return render_template("fullStory.html",likes=dictStoryInfo["popularity"], title=dictStoryInfo["title"], author=dictStoryInfo["author"], genre=dictStoryInfo["genre"],id=dictStoryInfo["id"], pieces=dictStoryInfo["pieces"])
    else: #not logged in
       if dictStoryInfo["finished"]: #checks if story is finished, guests can view finished story
           return render_template("fullStory.html", likes=dictStoryInfo["popularity"], title=dictStoryInfo["title"], author=dictStoryInfo["author"], genre=dictStoryInfo["genre"],id=dictStoryInfo["id"],  pieces=dictStoryInfo["pieces"]) 
       else: #prompts user to log in because story is not finished
           flash("Please log in to view/edit story")
           return redirect(url_for('home'))

                
@app.route('/search', methods = ['GET'])
def search_route():
    results = search.getAllStories()
    listUsers = False #jinja wont render this if you are not searching for author/user
    query = request.args.get("q", "")
    author = request.args.get("by", "")
    genre = request.args.get("genre", "")
    status = request.args.get("status", "")
    sortby = request.args.get("sort", "c")
    if query != "":
        results = search.filter_by_title(query, results)
    if genre != "":
        results = search.filter_by_genre(genre, results)
    if author != "":
        results = search.filter_by_author(author, results)
        listUsers = search.getUsers(author)
    if status != "":
        results = search.filter_by_status(status, results)
    results = search.sortby(sortby, results)
    return render_template("list.html", page_title="Search Results", listStories=results, listUsers=listUsers)

@app.route('/user', methods = ['GET'])
def user():
    userName=request.args.get("id", "")
    return render_template("user.html", page_title=userName, user=userName)

@app.route('/create', methods=['POST','GET'])
def createStory():
    return render_template('createStory.html', page_title="Create Story")

@app.route('/create/submit', methods=['POST','GET'])
def created():
    title=request.form["title"]
    genre=request.form["genre"]
    wordLimit=request.form["charLimit"]
    content=request.form["storyContent"]
    userName=session["user"]
    idNum=mystory.add_new_story(title, userName, genre,wordLimit, 100)
    return redirect(url_for('story_route')+'?id='+str(idNum))

@app.route('/contribute',methods=['POST','GET'])
def contribute():
    #didn't test yet
    userName=session["user"]
    textAdded=request.form["contributedText"]
    storyId=request.args.get("id", "")
    mystory.modify_story(userName, textAdded,storyId)
    return redirect(url_for('story_route')+'?id='+str(storyId))

@app.route('/logout')
def logout():
        session.pop('user')
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.debug = True
    app.run()
