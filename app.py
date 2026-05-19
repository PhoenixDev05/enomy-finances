import os
from flask import request, jsonify
from flask import Flask, render_template, redirect, session, url_for
from functools import wraps
from users import User
from usermanager import UserManager
from audit import Auditing
from currExchange import Exchange
from customerManager import CustomerManager
from investmentManager import investments

#----------------------------
#CLASS INSTANCES AND APP INIT
#----------------------------
app = Flask(__name__)
app.secret_key = "12345"
UM = UserManager()
audit = Auditing()
user = User()
#---------------------------
#Curr Exchange
#---------------------------
currExchange = Exchange()
currExchange.loadHistory()
currExchange.getLatestRates()
currExchange.loadFees()
currExchange.getNewRateAPI()

#----------------------------
#INVESTMENT MANAGER
#----------------------------
IM = investments()
IM.loadPlans()
IM.loadTaxes()
IM.loadQuotes()

#----------------------------
#CUSTOMERS
#----------------------------
cusData = CustomerManager()
cusData.loadCustomerData()

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
            user.username = userData[0]
            user.fname =userData[1]
            user.sname = userData[2]
            user.accessLevel = userData[3]
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

@app.route("/exchange", methods=["GET", "POST"])
@Login_Required
def exchange():
            
    return render_template("exchange.html")

@app.route("/customers")
@Login_Required
def customerView():
    return render_template("customers.html")


#-----------------------
#API CALLS
#-----------------------
@app.route("/api/exchange/<startCurr>/<targetCurr>/<startAmount>/<clientID>", methods=["GET", "POST"])
@Login_Required
def currExchangeAPI(startCurr, targetCurr, startAmount, clientID):
    
    currExchange.getBaseRate(startCurr)
    currExchange.getTargetRate(targetCurr)
    convertedValue = currExchange.conversion(startCurr, targetCurr, startAmount)
    feeInfo = currExchange.calcFees(startAmount, startCurr,convertedValue)
    fee = feeInfo["charge"]
    tax = feeInfo["tax"]
    total = feeInfo["total"]
    cusData.saveCurrTransaction(clientID,startCurr,targetCurr,currExchange.conversion(startCurr, targetCurr,1),startAmount,fee,total)
    audit.addEvent(session["username"], "CurrExchange Transaction", "Sucessful")
    return jsonify({"convertedValue": convertedValue, "fee": fee, "tax":tax, "total":total})

@app.route("/api/history/<startCurr>/<targetCurr>",methods=["GET","POST"])
@Login_Required
def historyGraphAPI(startCurr, targetCurr):
    #load history
    history = currExchange.historicalRates
    

    data = {"dates":[entry["date"]for entry in history],
            "rates":[entry["rates"][targetCurr]/entry["rates"][startCurr] for entry in history],
            "base": startCurr,
            "target": targetCurr}
    
    return data

#----------------------
#Customer API Call
#----------------------
@app.route("/api/customers/get/curr", methods=["GET", "POST"])
@Login_Required
def getCustomers():
    customers = cusData.customers

    data = {"clientID": [entry["clientID"] for entry in customers], 
            "firstName": [entry["firstName"] for entry in customers],
            "lastName": [entry["lastName"] for entry in customers]}
    return data

@app.route("/api/customers/get/currTrans/<clientID>", methods=["GET","POST"])
@Login_Required
def getCurrTransactions(clientID):
    transHistory = cusData.getCustomerCurrTransactions(clientID)
    return jsonify(transHistory)

#load customers
@app.route("/api/customers/get/all", methods=["GET", "POST"])
@Login_Required
def getCustomerData():
    data = cusData.getCustomers()
    print(data)
    return jsonify(data)

#modify btn
@app.route("/api/customers/modify/<clientID>/<firstName>/<lastName>/<email>/<phone>/<addr1>/<addr2>/<city>/<postcode>/<country>")
@Login_Required
def modifyCustomerRecord(clientID,firstName,lastName,email,phone,addr1,addr2,city,postcode,country):
    cusData.updateCustomer(clientID,firstName,lastName,email,phone,addr1,addr2,city,postcode,country)
    audit.addEvent(session["username"], f"CUSTOMER MODIFIED WITH ID: {clientID}", "SUCCESS")
    return jsonify({"success": True})

@app.route("/api/customers/add/<firstName>/<lastName>/<email>/<phone>/<addr1>/<addr2>/<city>/<postcode>/<country>", methods=["POST", "GET"])
@Login_Required
def addNewCustomerRecord(firstName,lastName,email,phone,addr1,addr2,city,postcode,country):
    cusData.addCustomer(firstName,lastName,email,phone,addr1,addr2,city,postcode,country)
    audit.addEvent(session["username"], "NEW CUSTOMER ADDED", "Success")
    return jsonify({"success": True})

#---------------------------
#ADMIN PANEL
#--------------------------
@app.route("/admin")
@Login_Required
def admin():
    return render_template("admin.html")

#----------------------------
#ADMIN API CALLS
#----------------------------
@app.route("/api/users/getsecure")
@Login_Required
def getSecure():
    data = UM.getUserDataSecure()
    return jsonify(data)

@app.route("/api/users/modify/<staffID>/<username>/<firstName>/<lastName>/<email>/<password>")
@Login_Required
def modifyStaff(staffID,username,firstName,lastName,email,password):
    UM.modifyUser(staffID,username,firstName,lastName,email,password)
    audit.addEvent(session["username"], f"USER OF ID:{staffID}", "Data MODIFICATION SUCCESSFUL")
    return jsonify({"success": True})

@app.route("/api/users/add/<username>/<firstName>/<lastName>/<email>/<password>")
@Login_Required
def addNewUser(username,firstName,lastName,email,password):
    UM.addUser(username,firstName,lastName,email,password)
    audit.addEvent(session["username"], "NEW USER ADDED", "Successful Addition of user")
    return jsonify({"success": True})

#logout
@app.route("/logout")
@Login_Required
def logout():
    session.clear()
    UM.logout()
    return redirect("/")

#------------------------
#INVESTMENTS
#------------------------
@app.route("/investments")
@Login_Required
def invest():
    return render_template("investments.html")

#INVESTMENT API CALL
@app.route("/api/invest/get/plans")
@Login_Required
def getInvestmentPlans():
    data = IM.getPlans()
    return jsonify(data)

@app.route("/api/invest/validate/<planID>/<initialAmount>/<monthlyAmount>")
@Login_Required
def validationChecker(planID,initialAmount, monthlyAmount):
    response = IM.validateValues(planID, initialAmount, monthlyAmount)
    return jsonify(response)

@app.route("/api/invest/quote/<clientID>/<planID>/<initialAmount>/<monthlyAmount>")
@Login_Required
def generateQuote(clientID,planID,initialAmount,monthlyAmount):
    response = IM.quoteMaker(clientID, planID,initialAmount,monthlyAmount)
    audit.addEvent(session["username"], "Quote Generation", "Successful Quote Made")
    return jsonify(response)

@app.route("/api/invest/get/quote/<clientID>")
@Login_Required
def grabQuotes(clientID):
    response = IM.getQuotes(clientID)
    return jsonify(response)

#run application
if __name__ == "__main__":
    app.run(debug=True)