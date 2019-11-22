import pubnub
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

final = False
messages = []
name = input("Greetings, enter your ID: ")

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-0f1e68a2-0464-11ea-b6a6-32c7c2eb6eff"
pnconfig.publish_key = "pub-c-a516a8bf-4e77-4cf5-a454-bc44137ade7f"
pnconfig.uuid = name
#pnconfig.ssl = False
pubnub = PubNub(pnconfig)

class DatabaseSync(SubscribeListener):
	Data = None
	count = 0

	def showResult(message):
		global final
		for i in message:
			if i[0] == name:
				print("Loan Package accepted\nAmount: {}\tYear: {}\tIntRate: {}".format(i[1][0],i[1][1],i[1][2]))
				final = False
				break

		if final:
			print("Your loan request was not accepted")


	def goAhead():
	#iteration = int(input("How many bet request do you want? "))
		#print(messages)
		constraints = messages[-1].split()
		iteration = 3
		for i in range(iteration):
			#for i in messages[-1]:
			#print(i)
			amount = int(input("Enter loan amount: "))
			while( (amount > int(constraints[0])) or (amount < 99)):
				print("Amount invalid")
				amount = int(input("Enter loan amount: "))

			year = int(input("Enter loan repay period in years: "))
			while((year > int(constraints[1])) or (year < 1)):
				print("Repay period in years invalid")
				year = int(input("Enter loan repay period in years: "))

			interestRate = int(input("Enter desired interest rate: "))
			while((interestRate > int(constraints[2])) or (interestRate < 1)):
				print("Interest rate invalid")
				interestRate = int(input("Enter desired interest rate: "))

			print("End of request\n")
			requestLoans.append([pnconfig.uuid,amount,year,interestRate])
			pubnub.publish().channel("Demo.2").message([requestLoans[i][0],requestLoans[i][1],requestLoans[i][2],requestLoans[i][3]]).pn_async(show)
		#End of Subscriber action
		pubnub.publish().channel("Demo.2").message("End").pn_async(show)

	def checkGoAhead(message):
		if "End" in message:
			DatabaseSync.goAhead()
		elif "Final" in message:
			global final
			final = True
		else:
			print(message)
			global messages
			messages.append(message)

	def message(self, pubnub, data):
		self.Data = data
		if final:
			DatabaseSync.showResult(data.message)
		else:
			DatabaseSync.checkGoAhead(data.message)

#Shows message and status
def show(msg, stat):
	if msg and stat: pass#print( "\n",msg.timetoken, stat.status_code )
	else           : print( "Error", stat and stat.status_code )

sync = DatabaseSync()
pubnub.add_listener(sync)
pubnub.subscribe().channels("Demo.1").execute()

requestLoans = []