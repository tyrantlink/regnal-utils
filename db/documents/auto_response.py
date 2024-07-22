from .ext.enums import AutoResponseMethod, AutoResponseType
from pydantic import BaseModel, Field, conlist
from ...tyrantlib import merge_dicts
from typing import Optional, Self
from datetime import timedelta
from beanie import Document


class AutoResponse(Document):
    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    class Settings:
        name = 'auto_responses'
        use_cache = True
        validate_on_save = True
        use_state_management = True
        cache_expiration_time = timedelta(seconds=5)

    class AutoResponseData(BaseModel):
        class AutoResponseFollowup(BaseModel):
            delay: float = Field(
                default=0,
                ge=0,
                description='auto response followup delay in seconds'
            )
            response: str = Field(
                max_length=1024,
                description='auto response followup response'
            )

        weight: int = Field(
            default=1000,
            description='auto response weight (for when multiple auto responses are triggered)'
        )
        chance: float = Field(
            default=100.0,
            gt=0,
            le=100,
            description='auto response chance\n\nchance to trigger when selected, if failed, auto response is rerolled'
        )
        ignore_cooldown: bool = Field(
            default=False,
            description='auto response ignores cooldown\n\nwarning, people can use this to spam'
        )
        custom: bool = Field(
            default=False,
            description='auto response is guild custom'
        )
        regex: bool = Field(
            default=False,
            description='auto response trigger is regex'
        )
        nsfw: bool = Field(
            default=False,
            description='auto response is nsfw'
        )
        case_sensitive: bool = Field(
            default=False,
            description='auto response trigger is case sensitive'
        )
        delete_trigger: bool = Field(
            default=False,
            description='auto response trigger is deleted'
        )
        user: Optional[int] = Field(
            default=None,
            description='auto response user'
        )
        guild: Optional[int] = Field(
            default=None,
            description='auto response guild'
        )
        source: Optional[str] = Field(
            default=None,
            description='auto response source'
        )
        followups: conlist(AutoResponseFollowup, max_length=10) = Field(  # type: ignore # it's fine, it's pydantic black magic
            default=[],
            description='auto response followups'
        )

    class AutoResponseStatistics(BaseModel):
        trigger_count: int = Field(
            default=0,
            ge=0,
            description='auto response trigger count'
        )

    id: str = Field(
        description='auto response id'
    )
    method: AutoResponseMethod = Field(
        description='auto response method'
    )
    trigger: str = Field(
        description='auto response trigger'
    )
    response: str = Field(
        max_length=1024,
        description='auto response response'
    )
    type: AutoResponseType = Field(
        description='auto response type'
    )
    data: AutoResponseData = Field(
        default=AutoResponseData(),
        description='auto response data'
    )
    statistics: AutoResponseStatistics = Field(
        default=AutoResponseStatistics(),
        description='auto response statistics'
    )

    def with_overrides(self, overrides: dict) -> Self:
        return self.model_validate(merge_dicts(self.model_dump(), overrides))
