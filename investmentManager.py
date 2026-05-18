import json
class investments:
    def __init__(self):
        self.plans = []
        self.taxes = []


    def loadPlans(self):
        with open("data/investmentPlans.json", "r") as f:
            self.plans = json.load(f)

    def loadTaxes(self):
        with open("data/taxes.json", "r") as f:
            self.taxes = json.load(f)

    def getPlans(self):
        planData = []
        index = 0
        for plan in self.plans:
            data = {"planID": plan["planID"], "planName": plan["planName"], "desc": plan["desc"], "maxInvestYr": plan["maxInvestYr"],
                    "minMonthly": plan["minMonthly"], "minLump": plan["minLump"], "minReturnRate": plan["minReturnRate"], "maxReturnRate": plan["maxReturnRate"],
                    "taxRate": self.taxes[index]["taxRate"], "threshold": self.taxes[index]["threshold"], "fee": plan["monthlyFeeRate"]}
            index = index +1
            
            planData.append(data)
        return planData
    
    def validateValues(self, planID, initialAmount, monthlyAmount):
        planData = self.plans[int(planID)-1]
        print(planData)
        yearInvest = float(monthlyAmount) *12
        print(initialAmount)
        print(monthlyAmount)

        if float(initialAmount) < planData["minLump"]:
            return {"success": False, "message": "Initial Lump sum too Low"}
        elif float(monthlyAmount) < planData["minMonthly"]:
            return {"success": False, "message": "Monthly amount too low"}
        elif yearInvest > planData["maxInvestYr"] and planData["maxInvestYr"] !=0:
            return {"success": False, "message": "You have exceeded the maximum"}
        else:
            return {"success": True, "message": ""}
        

    def quoteMaker(self, clientID:int, planID:int, initialAmount:float, monthlyAmount:float):
        #Get plan and taxRate
        years = [1,5,10]
        minProfit = 0
        maxProfit = 0
        planData = self.plans[int(planID)-1]
        taxRate = self.taxes[planData["taxCode"]-1]["taxRate"]
        taxThreshold = self.taxes[planData["taxCode"]-1]["threshold"]
        minReturnRate = planData["minReturnRate"] / 100
        maxReturnRate = planData["maxReturnRate"] / 100
        feeRate = planData["monthlyFeeRate"] /100
        minTax = 0.0
        maxTax =0.0
        initialAmount = float(initialAmount)
        monthlyAmount = float(monthlyAmount)
        output = {}

        for year in years:
            months = year*12
            maxReturn = float(initialAmount) * ((1+maxReturnRate) ** float(months)) + monthlyAmount * (((1 + maxReturnRate) ** float(months) - 1) / maxReturnRate)
            minReturn = float(initialAmount) * ((1+minReturnRate) ** float(months)) + monthlyAmount * (((1 + minReturnRate) ** float(months) - 1) / minReturnRate)
            
            totalInvested = initialAmount + (monthlyAmount * 12 * year)
            maxProfit = maxReturn - totalInvested
            minProfit = minReturn - totalInvested

            fee = (monthlyAmount *months) * feeRate

            #TAX CHECKER - Validate is over threshold then steal money
            print(len(taxRate))
            if len(taxRate) <2:
                if minProfit > taxThreshold:
                    minTax = (minProfit- taxThreshold)*taxRate[0]
                else:
                    minTax =0
                if maxProfit > taxThreshold:
                    maxTax = (maxProfit - taxThreshold) *taxRate[0]
                else:
                    maxTax = 0
            else:
                if minProfit > taxThreshold[1]:
                    minTax = ((minProfit - taxThreshold[1])*taxRate[1])+((taxThreshold[1] - taxThreshold[0])*taxRate[0])
                elif minProfit > taxThreshold[0]:
                    minTax = (minProfit - taxThreshold[0])*taxRate[0]
                else:
                    minTax = 0

                if maxProfit > taxThreshold[1]:
                    maxTax = ((maxProfit - taxThreshold[1])*taxRate[1])+((taxThreshold[1] - taxThreshold[0])*taxRate[0])
                elif minProfit > taxThreshold[0]:
                    maxTax = (maxProfit - taxThreshold[0])*taxRate[0]
                else:
                    maxTax = 0

            output[year] = {
                "maxReturn": round(maxReturn,2),
                "minReturn": round(minReturn,2),
                "maxProfit": round(maxProfit,2),
                "minProfit": round(minProfit,2),
                "fee": round(fee,2),
                "maxTax":round(maxTax,2),
                "minTax": round(minTax,2)
            }
            #self.saveQuote(clientID, output)
        return output
            #DATA RETURN
            #SAVE DATA TO QUOTE

    #def loadQuotes(self):

    #def saveQuote(self,clientID, output):