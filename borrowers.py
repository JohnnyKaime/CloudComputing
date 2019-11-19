import pubnub
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

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

	def goAhead():
	#iteration = int(input("How many bet request do you want? "))
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
			requestLoans.append([pnconfig.uuid,amount,interestRate,year])
			pubnub.publish().channel("Demo.2").message([requestLoans[i][0],requestLoans[i][1],requestLoans[i][2],requestLoans[i][3]]).pn_async(show)
		#End of Subscriber action
		pubnub.publish().channel("Demo.2").message("End").pn_async(show)

	def checkGoAhead(message):
		if "End" in message:
			DatabaseSync.goAhead()
		else:
			print(message)
			global messages
			messages.append(message)

	def message(self, pubnub, data):
		self.Data = data
		DatabaseSync.checkGoAhead(data.message)

#Shows message and status
def show(msg, stat):
	if msg and stat: pass#print( "\n",msg.timetoken, stat.status_code )
	else           : print( "Error", stat and stat.status_code )

sync = DatabaseSync()
pubnub.add_listener(sync)
pubnub.subscribe().channels("Demo.1").execute()

requestLoans = []