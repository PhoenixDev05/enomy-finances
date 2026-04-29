import os
from flask import request
from flask import Flask, render_template


#create instance of app
app = Flask(__name__)

#app routing
@app.route("/", methods=['GET', 'POST'])
def Login():
    #if request.method == 'POST':
        
    #else:
    return render_template("login.html")


#run application
if __name__ == "__main__":
    app.run(debug=True)