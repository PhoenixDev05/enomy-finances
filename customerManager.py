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
    
    def getCustomers(self):
        return self.customers
    
    #------------------------
    #Customer CRUD operation
    #------------------------

    def saveCustomerUpdate(self):
        with open("data/customers.json", "w") as f:
            json.dump(self.customers, f, indent=4)


    def updateCustomer(self, clientID, firstName,lastName,email,phone,addr1,addr2,city,postcode,country):
        addr2 = "" if addr2== "null" else addr2
        for customer in self.customers:
            if str(customer["clientID"]) == str(clientID):
                #needs to update the customer
                customer["firstName"] = firstName
                customer["lastName"] = lastName
                customer["email"] = email
                customer["phone"] = phone
                customer["addressLine1"] = addr1
                customer["addressLine2"] = addr2
                customer["city"] = city
                customer["postcode"] = postcode
                customer["country"] = country
                #then dump the update
                self.saveCustomerUpdate()
        return True
                   
#ADD NEW CUSTOMER

    def addCustomer(self,firstName,lastName,email,phone,addr1,addr2,city,postcode,country):
        addr2 = "" if addr2== "null" else addr2
    #Get the new ID
    #then append to the list then dump ;)
        newClientID = self.customers[-1]["clientID"] +1
        newDict = {"clientID": newClientID,
               "firstName": firstName,
               "lastName": lastName,
               "email": email,
               "phone": phone,
               "addressLine1": addr1,
               "addressLine2": addr2,
               "city": city,
               "postcode": postcode,
               "country": country}
    
        self.customers.append(newDict)
        self.saveCustomerUpdate()

    def deleteCustomer(self, clientID):
        initCount = len(self.customers)
        self.customers = [customer for customer in self.customers if customer["clientID"] != int(clientID)]

        if len(self.customers) <initCount:
            self.saveCustomerUpdate()
            self.deleteTransactions(clientID)
            return True
        return False
    
    def deleteTransactions(self, clientID):
        with open("data/currencyTransactions.json", "r") as f:
            currTrans = json.load(f)
        
        with open("data/quotes.json", "r") as f:
            quotes = json.load(f)

        currTrans = [trans for  trans in currTrans if trans["clientID"] != str(clientID)]
        quotes = [quote for  quote in quotes if quote["clientID"] != int(clientID)]

        with open("data/currencyTransactions.json","w") as f:
            json.dump(currTrans,f,indent=4)
        
        with open("data/quotes.json", "w") as f:
            json.dump(quotes,f, indent=4)