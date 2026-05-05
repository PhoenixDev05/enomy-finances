import os
from flask import request
from flask import Flask, render_template, redirect, session, url_for
from functools import wraps
from users import User
from usermanager import UserManager
from audit import Auditing
from currExchange import Exchange

#----------------------------
#CLASS INSTANCES AND APP INIT
#----------------------------
app = Flask(__name__)
app.secret_key = "12345"
UM = UserManager()
audit = Auditing()
currExchance = Exchange()

#-------------------------
#DECORATED FUNCTIONS
#-------------------------
def Login_Required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for('Login'))
        return f(*args, **kwargs)
    return decorated_function

#-------------------------
#APP ROUTING
#-------------------------

@app.route("/", methods=['GET', 'POST'])
#this is the default page that handles the login functionality!
def Login():
    if "username" in session:
        return redirect("/dashboard")
    
    error = None
    if request.method == 'POST':
        username = request.form["username"]
        print(username)
        password = request.form["password"]
        print(password)
        if UM.authenticate(username, password):
            userData = UM.getUserData(username)
            user = User(userData[0], userData[1], userData[2], userData[3])
            session["username"] = user.username
            session["fname"] = user.fname
            session["accessLevel"] = user.accessLevel
            audit.addEvent(username, "Login Attempt", "Successful Login")
            #go to the dashboard
            return redirect("/dashboard")
        else:
            error = "incorrect username or password you idiot!"
            audit.addEvent(username, "Login Attempt", "Failed Login Attempt")
            return render_template("login.html", error=error)

    else:
        return render_template("login.html", error=error)

@app.route("/dashboard")
@Login_Required
def dashboard():
    return render_template("dashboard.html")

@app.route("/exchange")
@Login_Required
def exchange():
    return render_template("exchange.html")
    

#logout
@app.route("/logout")
@Login_Required
def logout():
    session.clear()
    UM.logout()
    return redirect("/")
    

#run application
if __name__ == "__main__":
    app.run(debug=True)