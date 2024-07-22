
from datetime import timedelta
from beanie import Document
from pydantic import Field


class Log(Document):
    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    class Settings:
        name = 'logs'
        use_cache = True
        validate_on_save = True
        use_state_management = True
        cache_expiration_time = timedelta(minutes=5)

    id: int = Field(description='message id')
    data: dict = Field(default={}, description='log data')
