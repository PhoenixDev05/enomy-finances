import json
from datetime import datetime
import requests
#------------------------------
#Uses GBP as the base currency
#------------------------------
class Exchange():
    def __init__(self):
        self.historicalRates = []
        self.currentRates = {}
        self.targetRate = 0
        self.fees = []

    def getNewRateAPI(self):
        #check rate for today not exist in system
        #if not then do api call
        #if api fail then use yesterday rate
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        #print(self.currentRates["date"])
        if self.currentRates["date"] != date:
            #try:
            url = "https://api.exchangerate-api.com/v4/latest/GBP"
            response = requests.get(url).json()
            print(response)
            with open("data/todayRate.json", "w") as f:
                json.dump({"base": "GBP","date": date, "rates": response["rates"]}, f, indent=4)

            with open("data/exchangeHistory.json", "r") as f:
                data = json.load(f)
                        
            data.append({"base": "GBP","date": date, "rates": response["rates"]})
                
            with open("data/exchangeHistory.json", "w") as f:
                json.dump(data, f, indent=4)
            
            #except:
                print("AHHHHHH")
            
            #then appends it to json file
        

    def loadHistory(self):
        with open("data/exchangeHistory.json", "r") as f:
            data = json.load(f)
            self.historicalRates = data
    
    def loadFees(self):
        with open("data/fees.json", "r") as f:
            data = json.load(f)
            dataSort = sorted(data, key=lambda x:x["minAmount"], reverse=True)
            self.fees = dataSort

    def getLatestRates(self):
        with open("data/todayRate.json", "r") as f:
            data = json.load(f)

        latestData = data
        self.currentRates = latestData

    def getTargetRate(self,target):
        rate = self.currentRates["rates"][target]
        self.targetRate = rate
        return self.targetRate

    def getBaseRate(self, base):
        rate = self.currentRates["rates"][base]
        self.baseRate = rate
        return self.baseRate
    
    def conversion(self, start, target, amount):
        if start != "GBP":
            #convtert to gbp first
            GBPtostart = self.getBaseRate(start)
            GBPValue = int(amount) /GBPtostart
        else:
            GBPValue = int(amount)

        targetRate = self.getTargetRate(target)
        print(type(GBPValue),type(targetRate))
        conv= GBPValue * targetRate
        conv = round(conv,2)
        return conv 
    
    def calcFees(self, startAmount, startCurrency,convAmount):
            if startCurrency !="GBP":
                startAmount_1 = self.conversion(startCurrency, "GBP", int(startAmount))
            else:
                startAmount_1 = startAmount
            for fee in self.fees:
                
                if fee["minAmount"] <= int(startAmount_1):
                    #Calc Fee
                    tax = fee["fee"]
                    charge = (tax/100) * int(startAmount_1)
                    charge = round(charge,2)
                    total = int(convAmount) - self.conversion("GBP", startCurrency,charge)
                    success = True
                    print(total)
            if success:
                return {"charge": charge, "tax": tax, "total": total}
            else:
                return 0
            
