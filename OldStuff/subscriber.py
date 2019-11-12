import pubnub
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-0f1e68a2-0464-11ea-b6a6-32c7c2eb6eff"
pnconfig.publish_key = "pub-c-a516a8bf-4e77-4cf5-a454-bc44137ade7f"
pnconfig.uuid = "Johnny"
#pnconfig.ssl = False
pubnub = PubNub(pnconfig)

class DatabaseSync(SubscribeListener):
	Data = None
	def message(self, pubnub, data):
		self.Data = data
		print(data.message)

#Shows message and status
def show(msg, stat):
	if msg and stat: pass#print( msg.timetoken, stat.status_code )
	else           : print( "Error", stat and stat.status_code )

while True:
	sync = DatabaseSync()
	pubnub.add_listener(sync)
	pubnub.subscribe().channels("Demo.1").execute()

	time.sleep(2)

	if sync.Data != None:
		if "Amount" in sync.Data.message:
			respond = input("Yes to take loan, no to ignore\n")
			time.sleep(1)
			if "yes" in respond.lower():
				pubnub.publish().channel("Demo.2").message("Yes").pn_async(show)
				pubnub.publish().channel("Demo.2").message("0.15").pn_async(show)
			else:
				print("ADSFSADFADSFASDF")
		else:
			print("None Input")
