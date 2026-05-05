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
        with open("exchangeHistory.json", "r") as f:
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

    def getBaseRate(self, base):
        rate = self.currentRates["rates"][base]
        self.baseRate = rate
    
    def conversion(self, start, target, amount):
        if start != "GBP":
            #convtert to gbp first
            GBPtostart = self.getBaseRate(start)
            GBPValue = start /GBPtostart
        else:
            GBPValue = start

        targetRate = self.getTargetRate(target)

        conv= GBPValue * targetRate
        return conv 
            