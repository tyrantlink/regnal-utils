
from datetime import timedelta
from beanie import Document
from pydantic import Field


class Log(Document):
	class Settings:
		name = 'logs'
		use_cache = True
		validate_on_save = True
		use_state_management = True
		cache_expiration_time = timedelta(minutes=5)

	id:int = Field(description='message id')
	data:dict = Field({},description='log data')