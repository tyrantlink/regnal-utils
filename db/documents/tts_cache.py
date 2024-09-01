from beanie import Document, BsonBinary, TimeSeriesConfig
from datetime import timedelta, datetime
from pydantic import Field


class TTSCache(Document):
    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    class Settings:
        name = 'tts_cache'
        use_cache = True
        validate_on_save = True
        use_state_management = True
        cache_expiration_time = timedelta(minutes=30)
        #! make it a timeseries document when https://github.com/BeanieODM/beanie/issues/1005 is fixed
        # timeseries = TimeSeriesConfig(
        #     time_field='ts',
        #     expire_after_seconds=2592000 # 30 days
        # )

    id: str = Field(description='TTSMessage hash')
    ts: datetime = Field(default_factory=datetime.now)
    data: BsonBinary = Field(description='TTSMessage data')
