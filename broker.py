import pubnub
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

import knapsack

pnconf = PNConfiguration()
pnconf.subscribe_key = "sub-c-0f1e68a2-0464-11ea-b6a6-32c7c2eb6eff"
pnconf.publish_key = "pub-c-a516a8bf-4e77-4cf5-a454-bc44137ade7f"
pnconf.uuid = "PUBLISHER"
#pnconf.ssl = False
pubnub = PubNub(pnconf)

def show(msg, stat):
	if msg and stat: print(msg.timetoken, stat.status_code )
	else           : print( "Error", stat and stat.status_code )

class DatabaseSync(SubscribeListener):
	Data = None

	def returnBorrower():
		flag = True
		tiredArray = []
		for i in kArray:
			if flag:
				print("Broker will yield {} amount after borrower repay".format(i))
				flag = False
			else:
				for j in i:
					tiredArray.append([finalLoanRequest[j][0],borrowerDict[finalLoanRequest[j][0]][finalLoanRequest[j][1]]])
					
		pubnub.publish().channel("Demo.1").message("Final").pn_async(show)
		pubnub.publish().channel("Demo.1").message(tiredArray).pn_async(show)

	def knapSacking():
		#creating neccessary variables
		weight = []
		value = []
		capacity = listOfConstraints[0]

		for borrower in finalLoanRequest:
			weight.append(borrowerDict[borrower[0]][borrower[1]][0])
			value.append(borrower[2])
		
		print("Knapsack solution returns:")
		global kArray
		kArray = knapsack.knapsack(weight, value).solve(capacity)

	def sortLoan():
		global finalLoanRequest
		for key in cleanLoanRequest:
			maxValueLoanRequest = max(cleanLoanRequest[key])
			indexOfMaxValue = cleanLoanRequest[key].index(maxValueLoanRequest)
			finalLoanRequest.append([key,indexOfMaxValue,maxValueLoanRequest])
		print(finalLoanRequest)

	def cleanLoanRequest():
		global cleanLoanRequest
		for key in borrowerDict:
			for value in borrowerDict[key]:
				valueSI = value[0] * value[1] * value[2] / 100
				if key not in cleanLoanRequest:
					cleanLoanRequest[key] = [valueSI]
				else:
					cleanLoanRequest[key].append(valueSI)

	def addToList(self):
		global borrowerDict
		global borrowerCount

		if self.Data.message != None and self.Data.message != "End":
			if self.Data.message[0] not in borrowerDict:
				borrowerCount += 1
				borrowerDict[self.Data.message[0]] = [[self.Data.message[1],self.Data.message[2],self.Data.message[3]]]
			else:
				borrowerDict[self.Data.message[0]].append([self.Data.message[1],self.Data.message[2],self.Data.message[3]])

	def checkStatus(message):
		global borrowerCount
		global endCount
		if "End" in message:
			endCount += 1
			if endCount == borrowerCount:
				#We can call the compare algorithm here
				print(borrowerDict)
				#DatabaseSync.doSomething()
				DatabaseSync.cleanLoanRequest()
				DatabaseSync.sortLoan()
				DatabaseSync.knapSacking()
				DatabaseSync.returnBorrower()
			pass
		else:
			DatabaseSync.neatPrint(message)

	def neatPrint(message):
		print("Borrower: {}\tAmount: {}\tIntRate: {}\tYear: {}".format(message[0],message[1],message[2],message[3]))

	def message( self, pubnub, data ):
		self.Data = data
		DatabaseSync.checkStatus(data.message)
		DatabaseSync.addToList(self)

def getConstraints():
	global listOfConstraints
	print("Welcome broker, please set your constraints for the loan application.")
	loanConstraint = int(input("Loan constraint (Maximum a borrower can take out): "))
	yearConstraint = int(input("Year constraint (Maimum year to pay off loan): "))
	intRConstraint = int(input("Interest rate constraint (Maximum interest rate): "))
	listOfConstraints.append(loanConstraint)
	listOfConstraints.append(yearConstraint)
	listOfConstraints.append(intRConstraint)

def publishConstraints():
	pubnub.publish().channel("Demo.1").message("Welcome to our loan application").pn_async(show)
	time.sleep(1)
	pubnub.publish().channel("Demo.1").message("The following are constraints for this auction:").pn_async(show)
	time.sleep(1)
	pubnub.publish().channel("Demo.1").message("Please note the following constraints are the maximum limits").pn_async(show)
	time.sleep(1)
	pubnub.publish().channel("Demo.1").message("Loan constraints Year constraints Interest rate constraints").pn_async(show)
	time.sleep(1)
	pubnub.publish().channel("Demo.1").message("{} {} {}".format(listOfConstraints[0],listOfConstraints[1],listOfConstraints[2])).pn_async(show)
	time.sleep(1)
	pubnub.publish().channel("Demo.1").message("End").pn_async(show)

#Loan info
cleanLoanRequest = {}
#Amount info after Simple Interest
borrowerDict = {}
#Final loan request after cleaning
#format as follows:
#	key, loan request package no., amount yield (borrower needs to pay/broker receives)
finalLoanRequest = []
#Use to trigger start end events
borrowerCount = 0
endCount = 0
#3 constratis loan amount, year, interest rate
listOfConstraints = []
kArray = []
getConstraints()
publishConstraints()

sync = DatabaseSync()
pubnub.add_listener(sync)
pubnub.subscribe().channels("Demo.2").execute()