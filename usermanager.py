import json
class UserManager:
    def __init__(self):
        self.users = []
        self.authUserData = []

        self.users = self.getUsers()

    def authenticate(self, username, password):
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                return True
        return False
    
    def getUserData(self, username):
        for user in self.users:
            if user["username"] == username:
                self.authUserData.append(username)
                self.authUserData.append(user["firstName"])
                self.authUserData.append(user["lastName"])
                self.authUserData.append(user["password"])
                self.authUserData.append(user["accessLevel"])
                return self.authUserData
        return None
    
    def logout(self):
        self.authUserData = []

    def getUsers(self):
        with open("data/users.json","r") as file:
            users = json.load(file)
            return users