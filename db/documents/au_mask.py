
from datetime import timedelta
from beanie import Document
from pydantic import Field


class AutoResponseFileMask(Document):
	def __eq__(self, other: object) -> bool:
		return isinstance(other, type(self)) and self.id == other.id
	
	def __hash__(self) -> int:
		return hash(self.id)

	class Settings:
		name = 'au_mask'
		use_cache = True
		validate_on_save = True
		use_state_management = True
		cache_expiration_time = timedelta(seconds=5)

	au:str = Field(description='auto response id')