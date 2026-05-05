from datetime import datetime
from flask import request
class Auditing:
    #needs to log user login
    #failed user attempts etc

    def __init__(self):
        pass

    def addEvent(self, user, action, result):
        ip = request.remote_addr
        now = datetime.now()
        timeStr = now.strftime("%Y-%m-%d %H:%M:%S")
        date = now.strftime("%Y-%m-%d")
        with open(f"audit/{date}.log", "a") as file:
            file.write(f"[{timeStr}] [{ip}] [User: {user} | Action: {action} | Result: {result}]\n")