import json

#------------------------------
#Uses GBP as the base currency
#------------------------------
class Exchange():
    def __init__(self):
        self.historicalRates = []
        self.currentRates = []
        self.targetRate = 0

    def loadHistory(self):
        with open("data/exchangeHistory.json", "r") as f:
            data = json.load(f)
            self.historicalRates = data

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
        return conv 
            