from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from second import second
from helper_functions import getLoginStatus
import hashlib

app = Flask(__name__)
app.secret_key = "A1WHhgMhpTvb63eeO@7Zyp38v7KwvWDR81EdgEe&"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(second, url_prefix="/admin")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    # If updating the table is desired, please refer to the documentation
    # https://flask-migrate.readthedocs.io/en/latest/

    # Update the init as well!
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

@app.route('/')
def index():
    return render_template('index.html', loginButtonInnerHTML=getLoginStatus())

# See all accounts stored in the db in the current session
@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all(), loginButtonInnerHTML=getLoginStatus())

# Create a new account
@app.route("/register", methods=["POST", "GET"])
def register():
    password = hashlib.new("SHA256")

    # If there is no user currently signed in
    if request.method == "POST":
        session.permanent = True

        # Grab the info from the html form on the page
        userName = request.form['userName']
        password.update(request.form['password'].encode())
        userPassword = password.hexdigest()

        # Put the info into the session
        session["user"] = userName
        session["password"] = userPassword

        # If the user already exists and the correct password is input,
        # simply sign the user in
        foundUser = users.query.filter_by(name=userName).first()
        if foundUser and foundUser.password == userPassword:
            flash("Account already exists! Logging in now!", "info")
            return redirect(url_for('login'))
        
        # If the user exists but the input password is incorrect
        elif foundUser and foundUser.password != userPassword:
            flash("Username taken! Choose another name.", "info")
            return render_template('register.html', loginButtonInnerHTML=getLoginStatus())
        
        # If the username has not been registered before
        else:
            newUser = users(userName, "", userPassword)
            db.session.add(newUser)
            db.session.commit()
        flash("Account Created Successfully", "info")
        return redirect(url_for('user'))
    
    # If there is already a user signed in
    else:
        if "user" in session:
            flash("Previous Session Restored!")
            return redirect(url_for("user"))
        return render_template('register.html', loginButtonInnerHTML=getLoginStatus())

# Log into an account which already exists in the session
@app.route('/login', methods=["POST", "GET"])
def login():
    password = hashlib.new("SHA256")

    # If there is no user currently signed in
    if request.method == "POST":
        session.permanent = True

        # Grab the info from the html form on the page
        userName = request.form['userName']
        password.update(request.form['password'].encode())
        userPassword = password.hexdigest()

        # Put the info into the session
        session["user"] = userName
        session["password"] = userPassword

        # If the user already exists and the correct password is input,
        # simply sign the user in
        foundUser = users.query.filter_by(name=userName).first()
        #print(f"{foundUser.password} == {userPassword} => {foundUser.password == userPassword}")
        if foundUser and foundUser.password == userPassword:
            session["email"] = foundUser.email
            session["user"] = foundUser.name

        # Otherwise, redirect the user to register a new account
        else:
            session.pop("user", None)
            session.pop("email", None)
            flash("User doesn't exist or password does not match!", "info")
            return redirect(url_for('register'))
        flash("Login Successful!", "info")
        return redirect(url_for('user'))
    
    # If there is already a user signed in
    else:
        if "user" in session:
            flash("Previous Session Restored!")
            return redirect(url_for("user"))
        return render_template('login.html', loginButtonInnerHTML=getLoginStatus())

# Homepage of signed in user
@app.route('/user', methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        userName = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            foundUser = users.query.filter_by(name=userName).first()
            foundUser.email = email
            db.session.commit()
            flash("Email entered successfully.")
        else:
            if "email" in session:
                email = session["email"]
        return render_template('user.html', userName=userName, email=email, loginButtonInnerHTML=getLoginStatus())
    else:
        flash("Not logged in!")
        return redirect(url_for('login'))

# Signs the user out
@app.route('/logout')
def logout():
    if "user" in session:
        userName = session["user"]
        flash(f"Logged {userName} Out Successfully", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for('login'))

# Removes selected account from the db
@app.route('/delete/<userName>')
def delete(userName):
    sessionUser = session.get("user")

    # If the user attempts to delete a user which does not exist... don't.
    foundUser = users.query.filter_by(name=userName).first()
    if foundUser == None:
        flash(f"{userName} is not a registered user!", "info")
        return redirect(url_for('login'))
    
    # Otherwise, proceed with deletion
    else:
        foundUser = foundUser.name

    #print(f"{sessionUser} == {foundUser} => {sessionUser == foundUser}")

    # Magical delete statement I totally understand
    """ THIS IS WHERE DELETION OCCURS """
    users.query.filter_by(name=userName).delete()
    db.session.commit()

    # If the user being deleted is the one currently signed in,
    # sign out the currently signed in user
    if sessionUser == foundUser:
        flash(f"Signed {sessionUser} out!", "info")
        return redirect(url_for('logout'))
    flash(f"Deleted {foundUser} successfully.", "info")
    return redirect(url_for('login'))

# Page has potential
@app.route('/about')
def about():
    return render_template('about.html', loginButtonInnerHTML=getLoginStatus())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)