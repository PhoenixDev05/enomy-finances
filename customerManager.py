import json
from datetime import datetime

class CustomerManager:
    def __init__(self):
        self.customers = []

    def loadCustomerData(self):
        with open("data/customers.json","r") as f:
            data = json.load(f)
            self.customers = data

    def saveCurrTransaction(self, clientID, baseCurr,targetCurr,targetRate,startAmount, fee, totalAmount):
        date = datetime.now().today()
        with open("data/currencyTransactions.json", "r") as f:
            index = 1
            data = json.load(f)
            for i in range(0,len(data)):
                index = index+1
        
        with open("data/currencyTransactions.json", "w") as f:
            data.append({"transID": index, "clientID": clientID,"date": str(date.strftime("%Y-%m-%d")) ,"baseCurr": baseCurr, "targetCurr": targetCurr, "targetRate": targetRate, "startAmount": startAmount, "fee": fee, "totalAmount": totalAmount})
            json.dump(data, f, indent=4)

    def getCustomerCurrTransactions(self, clientID):
        with open("data/currencyTransactions.json", "r") as f:
            userData = []
            data = json.load(f)
            for item in data:
                if item["clientID"] == clientID:
                    userData.append(item)
                    
        return userData
