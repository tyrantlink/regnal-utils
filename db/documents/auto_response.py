from .ext.enums import AutoResponseMethod,AutoResponseType
from pydantic import BaseModel,Field,conlist
from ...tyrantlib import merge_dicts
from typing import Optional,Self
from datetime import timedelta
from beanie import Document

class AutoResponse(Document):
	class Settings:
		name = 'auto_responses'
		use_cache = True
		validate_on_save = True
		use_state_management = True
		cache_expiration_time = timedelta(seconds=5)

	class AutoResponseData(BaseModel):
		class AutoResponseFollowup(BaseModel):
			delay:float = Field(0,ge=0,description='auto response followup delay in seconds')
			response:str = Field(max_length=1024,description='auto response followup response')

		weight:int = Field(1000,description='auto response weight (for when multiple auto responses are triggered)')
		ignore_cooldown:bool = Field(False,description='auto response ignores cooldown\n\nwarning, people can use this to spam')
		custom:bool = Field(False,description='auto response is guild custom')
		regex:bool = Field(False,description='auto response trigger is regex')
		nsfw:bool = Field(False,description='auto response is nsfw')
		case_sensitive:bool = Field(False,description='auto response trigger is case sensitive')
		delete_trigger:bool = Field(False,description='auto response trigger is deleted')
		user:Optional[int] = Field(None,description='auto response user')
		guild:Optional[int] = Field(None,description='auto response guild')
		source:Optional[str] = Field(None,description='auto response source')
		followups:conlist(AutoResponseFollowup,max_length=10) = Field([],description='auto response followups') # type: ignore # it's fine, it's pydantic black magic

	id:str = Field(description='auto response id')
	method:AutoResponseMethod = Field(description='auto response method')
	trigger:str = Field(description='auto response trigger')
	response:str = Field(max_length=1024,description='auto response response')
	type:AutoResponseType = Field(description='auto response type')
	data:AutoResponseData = Field(description='auto response data')

	def with_overrides(self,overrides:dict) -> Self:
		return self.model_validate(merge_dicts(self.model_dump(),overrides))