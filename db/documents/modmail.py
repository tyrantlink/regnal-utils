from pydantic import Field,BaseModel
from datetime import timedelta
from beanie import Document
from typing import Optional


class ModMail(Document):
	class Settings:
		name = 'modmail'
		use_cache = True
		validate_on_save = True
		use_state_management = True
		cache_expiration_time = timedelta(seconds=1)

	class ModMailMessage(BaseModel):
		author:Optional[int] = Field(None,description='author id, none for anonymous')
		content:str = Field(max_length=4096,description='message content')
		attachments:list[str] = Field([],description='message attachment urls')
		timestamp:int = Field(description='message timestamp')

	id:str = Field(description='{guild_id}:{modmail_id}')
	guild:int = Field(description='guild id')
	modmail_id:int = Field(description='modmail id')
	anonymous:bool = Field(description='whether the modmail is anonymous')
	title:str = Field(description='modmail title')
	message:int|None = Field(description='reported message id')
	thread:Optional[int] = Field(None,description='thread id')
	send_all:bool = Field(False,description='whether every message is sent to the user, or just pings')
	closed:bool = Field(False,description='whether the modmail is closed')
	messages:list[ModMailMessage] = Field([],description='modmail messages')