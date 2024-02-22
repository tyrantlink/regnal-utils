from enum import Enum

class GatewayOpCode(Enum): # comments from client perspective
	UNDEFINED = 0 # reserved
	ACK = 1 # server -> client
	HEARTBEAT = 2 # server <- client
	REQUEST = 3 # server -> client
	RESPONSE = 4 # server <- client


class GatewayRequestType(Enum):
	UNDEFINED = 0
	RELOAD_AU = 1