import json
from datetime import datetime
from security import security
class UserManager:
    def __init__(self):
        self.users = []
        self.authUserData = []
        self.secure = security()

        self.users = self.getUsers()

    def authenticate(self, username, password):
        for user in self.users:
            if user["username"] == username and self.secure.verifyPass(password,user["password"]):
                return True
        return False
    
    def getUserData(self, username):
        for user in self.users:
            if user["username"] == username:
                self.authUserData.append(username)
                self.authUserData.append(user["firstName"])
                self.authUserData.append(user["lastName"])
                self.authUserData.append(user["accessLevel"])
                return self.authUserData
        return None
    
    def logout(self):
        self.authUserData = []

    def getUsers(self):
        with open("data/users.json","r") as file:
            users = json.load(file)
            return users
        
    def getUserDataSecure(self):
        safeData = []
        for user in self.users:
            safeData.append({"staffID": user["staffID"], "username": user["username"], "firstName": user["firstName"],
                             "lastName": user["lastName"], "email": user["email"], "created": user["created"], "lastLogin": user["lastLogin"]})
            
        return safeData
    
    def modifyUser(self, staffID,username, firstName,lastName,email,password):
        for user in self.users:
            if str(user["staffID"]) == str(staffID):
                user["username"] = username
                user["firstName"] = firstName
                user["lastName"] = lastName
                user["email"] = email
                if password != "null":
                    user["password"] = self.secure.hashPassword(password)
                self.saveUserData()

        return True
    
    def addUser(self, username, firstName, lastName, email, password):
        creation = datetime.now().strftime("%Y-%m-%d %H:%M")
        newStaffID = self.users[-1]["staffID"] +1
        newDict = {"staffID": newStaffID, "username":username, "firstName": firstName, "lastName": lastName,
                   "email": email, "password": self.secure.hashPassword(password),"accessLevel":0, "created": creation, "lastLogin": ""}
        
        self.users.append(newDict)
        self.saveUserData()
    
    def saveUserData(self):
        with open("data/users.json", "w") as f:
            json.dump(self.users, f, indent=4)