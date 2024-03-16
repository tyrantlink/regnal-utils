from .enums import GatewayRequestType
from pydantic import BaseModel,Field
from .models import Request
from typing import Optional

class RequestReloadAU(Request):
	req:GatewayRequestType = GatewayRequestType.RELOAD_AU
	data:dict = {}

class RequestSendMessage(Request):
	class Data(BaseModel):
		content:str = Field(description='message content')
		channel:Optional[str] = Field(None,description='channel id to send message to')
		user:Optional[str] = Field(None,description='user id to dm message to')
		reply:Optional[str] = Field(None,description='message id to reply to')
		reply_mention:Optional[bool] = Field(False,description='whether to mention the replied message author')

	req:GatewayRequestType = GatewayRequestType.SEND_MESSAGE
	data:Data = Field(...,description='request data')

class RequestBotInfo(Request):
	req:GatewayRequestType = GatewayRequestType.BOT_INFO
	data:dict = {}