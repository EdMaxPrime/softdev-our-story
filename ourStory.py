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
        return redirect(url_for('stories'))
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
            return redirect(url_for('stories'))
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
        return redirect(url_for('stories'))
    else:
        flash("Passwords do not match")
    return redirect(url_for('join'))
    

@app.route('/stories')
def stories():
    return render_template("list.html", page_title="Stories", listStories=search.filter_by_status("all", search.getAllStories()))

@app.route('/story', methods = ['GET'])
def story():
    return

@app.route('/search', methods = ['GET'])
def search_route():
    return

@app.route('/user', methods = ['GET'])
def user():
    return 

@app.route('/create', methods=['POST','GET'])
def createStory():
    return render_template('createStory.html')

@app.route('/logout')
def logout():
        session.pop('user')
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.debug = True
    app.run()
