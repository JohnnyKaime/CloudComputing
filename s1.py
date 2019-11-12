import pubnub
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

name = input("Greetings, enter your ID: ")

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-0f1e68a2-0464-11ea-b6a6-32c7c2eb6eff"
pnconfig.publish_key = "pub-c-a516a8bf-4e77-4cf5-a454-bc44137ade7f"
pnconfig.uuid = name
#pnconfig.ssl = False
pubnub = PubNub(pnconfig)

class DatabaseSync(SubscribeListener):
	Data = None
	def message(self, pubnub, data):
		self.Data = data
		print(data.message)

#Shows message and status
def show(msg, stat):
	if msg and stat: pass#print( "\n",msg.timetoken, stat.status_code )
	else           : print( "Error", stat and stat.status_code )

sync = DatabaseSync()
pubnub.add_listener(sync)
pubnub.subscribe().channels("Demo.1").execute()

requestLoans = []

iteration = int(input("How many bet request do you want? "))
for i in range(iteration):
	amount = int(input("Enter loan amount: "))
	interestRate = int(input("Enter desired interest rate: "))
	requestLoans.append([pnconfig.uuid,amount,interestRate])
	pubnub.publish().channel("Demo.2").message([requestLoans[i][0],requestLoans[i][1],requestLoans[i][2]]).pn_async(show)
#End of Subscriber action
pubnub.publish().channel("Demo.2").message("End").pn_async(show)