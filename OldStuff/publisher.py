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
	if msg and stat: pass#print(msg.timetoken, stat.status_code )
	else           : print( "Error", stat and stat.status_code )

class DatabaseSync(SubscribeListener):
	Data = None
	def message( self, pubnub, data ):
		self.Data = data
		print(data.message)

loanPackage = [100,3299,50000]
messageRespond = "yes"
loanRate = []

for package in loanPackage:
	if "yes" in messageRespond.lower():
		pubnub.publish().channel("Demo.1").message("Loan Package: {}".format(loanPackage.index(package)+1)).pn_async(show)
		time.sleep(2)
		pubnub.publish().channel("Demo.1").message("Amount: {}".format(package)).pn_async(show)
		time.sleep(2)

		sync = DatabaseSync()
		pubnub.add_listener(sync)
		pubnub.subscribe().channels("Demo.2").execute()
		time.sleep(5)
		messageRespond = sync.Data
		if messageRespond == None:
			messageRespond = "yes"
			pass
		elif "yes" in messageRespond.message.lower():
			sync2 = DatabaseSync()
			pubnub.add_listener(sync2)
			pubnub.subscribe().channels("Demo.2").execute()
			loanRate.append(sync2.Data.message)
		else:
			messageRespond = "yes"
	else:
		print("Ignored or Not")
