import pubnub
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

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

	def doSomething():
		#Saves the dictionary list
		f= open("BorrowerLoanRequest","w+")
		f.write("BorrowerID,LoanAmount,IntRate,year\n")
		for keys,value in borrowerDict.items():
			f.write("{},{},{},{}\n".format(keys,value[0],value[1],value[2]))
		f.close()

	def addToList(self):
		global borrowerDict
		global borrowerCount

		if self.Data.message != None and self.Data.message != "End":
			if self.Data.message[0] not in borrowerDict:
				borrowerCount += 1
				borrowerDict[self.Data.message[0]] = [[self.Data.message[1],self.Data.message[2]]]
			else:
				borrowerDict[self.Data.message[0]].append([self.Data.message[1],self.Data.message[2]])

			#print(borrowerDict)

	def checkStatus(message):
		global borrowerCount
		global endCount
		if "End" in message:
			endCount += 1
			if endCount == borrowerCount:
				#We can call the compare algorithm here
				print(borrowerDict)
				DatabaseSync.doSomething()
			pass
		else:
			DatabaseSync.neatPrint(message)

	def neatPrint(message):
		print("Borrower: {}\tAmount: {}\tIntRate: {}".format(message[0],message[1],message[2]))

	def message( self, pubnub, data ):
		self.Data = data
		DatabaseSync.checkStatus(data.message)
		DatabaseSync.addToList(self)

def getConstraints():
	print("Welcome broker, please set your constraints for the loan application.")
	loanConstraint = int(input("Loan constraint (Maximum a borrower can take out): "))
	yearConstraint = int(input("Year constraint (Maimum year to pay off loan): "))
	intRConstraint = int(input("Interest rate constraint (Maximum interest rate): "))
	return [loanConstraint,yearConstraint,intRConstraint]

def publishConstraints(constraints):
	pubnub.publish().channel("Demo.1").message("Welcome to our loan application").pn_async(show)
	time.sleep(1)
	pubnub.publish().channel("Demo.1").message("The following are constraints for this auction:").pn_async(show)
	time.sleep(1)
	pubnub.publish().channel("Demo.1").message("Please note the following constraints are the maximum limits").pn_async(show)
	time.sleep(1)
	pubnub.publish().channel("Demo.1").message("Loan constraints Year constraints Interest rate constraints").pn_async(show)
	time.sleep(1)
	pubnub.publish().channel("Demo.1").message("{} {} {}".format(constraints[0],constraints[1],constraints[2])).pn_async(show)
	time.sleep(1)
	pubnub.publish().channel("Demo.1").message("End").pn_async(show)

constraints = getConstraints()
publishConstraints(constraints)

sync = DatabaseSync()
pubnub.add_listener(sync)
pubnub.subscribe().channels("Demo.2").execute()

borrowerDict = {}
borrowerCount = 0
endCount = 0
