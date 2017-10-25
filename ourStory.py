from flask import Flask, flash, render_template, request, session, redirect, url_for
import sqlite3


app = Flask(__name__)
app.secret_key = "THIS IS NOT SECURE"

@app.route('/')
def home():
    if 'user' in session:
                return render_template("input.html", user = session['user'], method = request.method)
    else:
	        return render_template('form.html', title = 'Main')

@app.route('/help')
def help():
    return


@app.route('/loginRedirect', methods=['POST','GET'])
def loginRedirect():
	print request.form['user']
        user = request.form['user']
        if user == 'bob':
                if request.form['password'] == 'secret':
                        session['user'] = request.form['user']
                        return render_template('input.html', title = user + "'s", user = user, method = request.method)
                else:
                	flash("Sorry, wrong password")
        else:
        	flash("Sorry, wrong username")
	return redirect(url_for('home'))       

@app.route('/create', methods=['POST','GET'])
def createStory():
    return render_template('createStory.html')

@app.route('/stories',methods=['POST','GET'])
def stories():
    return render_template('story.html')
    
@app.route('/logout')
def logout():
        session.pop('user')
        return redirect(url_for('home'))

if __name__ == "__main__":
	app.debug = True
	app.run()
