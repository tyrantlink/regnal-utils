from pydantic import BaseModel, Field
from datetime import timedelta
from beanie import Document


class INFBase(Document):
    class Settings:
        name = 'inf'
        use_cache = True
        validate_on_save = True
        use_state_management = True
        cache_expiration_time = timedelta(hours=1)
    id: str


class INFTextCorrection(INFBase):
    value: dict[str, str] = Field(description='dictionary of text corrections')


class INFExcuses(INFBase):
    class INFExcuseObject(BaseModel):
        intro: list[str] = Field(description='list of excuse intros')
        scapegoat: list[str] = Field(description='list of scapegoats')
        delay: list[str] = Field(description='list of delays')

    value: INFExcuseObject = Field(description='excuse object')


class INFInsults(INFBase):
    class INFInsultObject(BaseModel):
        adjective: list[str] = Field(description='list of adjectives')
        noun: list[str] = Field(description='list of nouns')

    value: INFInsultObject = Field(description='insult object')


class INFEightBall(INFBase):
    value: list[str] = Field(description='list of eight ball responses')


class INFBees(INFBase):
    value: list[str] = Field(description='list of bees :wink:')


class Inf:
    @staticmethod
    async def text_correction() -> dict[str, str]:
        """inf text correction"""
        return (await INFTextCorrection.find_one({'_id': 'text_correction'})).value

    @staticmethod
    async def excuses() -> INFExcuses.INFExcuseObject:
        """inf excuses"""
        return (await INFExcuses.find_one({'_id': 'excuses'})).value

    @staticmethod
    async def insults() -> INFInsults.INFInsultObject:
        """inf insults"""
        return (await INFInsults.find_one({'_id': 'insults'})).value

    @staticmethod
    async def eight_ball() -> list[str]:
        """inf eight ball"""
        return (await INFEightBall.find_one({'_id': 'eight_ball'})).value

    @staticmethod
    async def bees() -> list[str]:
        """inf bees"""
        return (await INFBees.find_one({'_id': 'bees'})).value
