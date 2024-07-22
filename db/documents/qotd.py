
from datetime import timedelta
from beanie import Document
from pydantic import Field


class QOTDResponseMetric(Document):
    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    class Settings:
        name = 'qotd_responses'
        use_cache = True
        validate_on_save = True
        use_state_management = True
        cache_expiration_time = timedelta(seconds=5)

    id: str = Field(description='question id (pack_name#question_id)')
    asked: int = Field(default=0, description='number of times asked')
    responses: int = Field(default=0, description='number of responses')
