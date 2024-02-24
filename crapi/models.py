from .enums import GatewayOpCode,GatewayRequestType
from pydantic import BaseModel,Field
from typing import Optional

class BaseGatewayMessage(BaseModel):
	op:GatewayOpCode
	seq:int = Field(0,ge=0,description='sent on any request, must be incremented on every message')
	error:Optional[str] = Field(None,description='error message if the message is an error')

class Ack(BaseGatewayMessage): #? ack is response without a body
	op:GatewayOpCode = GatewayOpCode.ACK

class Heartbeat(BaseGatewayMessage):
	op:GatewayOpCode = GatewayOpCode.HEARTBEAT

class Request(BaseGatewayMessage):
	op:GatewayOpCode = GatewayOpCode.REQUEST
	req:GatewayRequestType = Field(description='request type')

class Response(BaseGatewayMessage):
	op:GatewayOpCode = GatewayOpCode.RESPONSE
	data:dict = Field(description='response data')