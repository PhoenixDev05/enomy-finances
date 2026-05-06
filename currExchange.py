import json

#------------------------------
#Uses GBP as the base currency
#------------------------------
class Exchange():
    def __init__(self):
        self.historicalRates = []
        self.currentRates = []
        self.targetRate = 0
        self.fees = []

    def loadHistory(self):
        with open("data/exchangeHistory.json", "r") as f:
            data = json.load(f)
            self.historicalRates = data
    
    def loadFees(self):
        with open("data/fees.json", "r") as f:
            data = json.load(f)
            dataSort = sorted(data, key=lambda x:x["minAmount"], reverse=True)
            self.fees = dataSort

    #depends on load history
    def getLatestRates(self):
        dataSort = sorted(self.historicalRates, key=lambda i: i["date"])

        latestData = dataSort[-1]
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
    
    def calcFees(self, startAmount, startCurrency):
            if startCurrency !="GBP":
                startAmount = self.conversion(startCurrency, "GBP", int(startAmount))
            for fee in self.fees:
                if fee["minAmount"] <= int(startAmount):
                    #Calc Fee
                    tax = fee["fee"]
                    charge = (tax/100) * int(startAmount)
                    charge = round(charge,2)
                    success = True

            if success:
                return {"charge": charge, "tax": tax}
            else:
                return 0