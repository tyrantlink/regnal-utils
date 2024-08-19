from .documents import User, Guild, AutoResponse, AutoResponseFileMask, Log, QOTDResponseMetric, ModMail, TTSCache
from .documents.inf import Inf, INFTextCorrection, INFExcuses, INFInsults, INFEightBall, INFBees
from .documents.ext.enums import AutoResponseMethod
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database as _Database
from beanie import init_beanie, PydanticObjectId


class _MongoNew:
    @staticmethod
    def user(id: int, username: str) -> User:
        return User(id=id, username=username)

    @staticmethod
    def guild(id: int, name: str, owner: int | None) -> Guild:
        return Guild(id=id, name=name, owner=owner)

    @staticmethod
    def auto_response(id: int, method: AutoResponseMethod, trigger: str, response: str) -> AutoResponse:
        return AutoResponse(id=id, method=method, trigger=trigger, response=response)

    @staticmethod
    def au_mask(au: str) -> AutoResponseFileMask:
        return AutoResponseFileMask(au=au)

    @staticmethod
    def log(id: int, data: dict) -> Log:
        return Log(id=id, data=data)

    @staticmethod
    def tts_cache(id: int, data: bytes) -> TTSCache:
        return TTSCache(id=id, data=data)


class MongoDatabase:
    def __init__(self, mongo_uri: str) -> None:
        self._client: _Database = AsyncIOMotorClient(
            mongo_uri, serverSelectionTimeoutMS=5000)['regnal']

    async def connect(self) -> None:
        await init_beanie(self._client, document_models=[
            User,
            Guild,
            AutoResponse,
            AutoResponseFileMask,
            Log,
            ModMail,
            QOTDResponseMetric,
            INFTextCorrection,
            INFExcuses,
            INFInsults,
            INFEightBall,
            INFBees,
            TTSCache
        ])

    @property
    def new(self) -> _MongoNew:
        return _MongoNew

    @property
    def inf(self) -> Inf:
        return Inf

    async def user(self, _id: int | str, ignore_cache: bool = False, create_if_not_found: bool = False) -> User | None:
        """user documents"""
        user = await User.find_one({'_id': _id}, ignore_cache=ignore_cache)
        if user is not None:
            return user

        if not create_if_not_found:
            return None

        user = self.new.user(_id, '')
        await user.insert()

        return user

    async def guild(self, _id: int | str, ignore_cache: bool = False, create_if_not_found: bool = False) -> Guild | None:
        """guild documents"""
        guild = await Guild.find_one({'_id': _id}, ignore_cache=ignore_cache)

        if guild is not None:
            return guild

        if not create_if_not_found:
            return None

        guild = self.new.guild(_id, '', None)
        await guild.insert()

        return guild

    async def auto_response(self, _id: str, ignore_cache: bool = False) -> AutoResponse | None:
        """auto response documents"""
        return await AutoResponse.find_one({'_id': _id}, ignore_cache=ignore_cache)

    async def au_mask(self, _id: PydanticObjectId, ignore_cache: bool = False) -> AutoResponseFileMask | None:
        """auto response file mask documents"""
        return await AutoResponseFileMask.find_one({'_id': _id}, ignore_cache=ignore_cache)

    async def modmail(self, _id: str, ignore_cache: bool = False) -> ModMail | None:
        """modmail documents"""
        return await ModMail.find_one({'_id': _id}, ignore_cache=ignore_cache)

    async def qotd_metric(self, _id: int | str, ignore_cache: bool = False) -> QOTDResponseMetric:
        """qotd metric documents"""
        metric = await QOTDResponseMetric.find_one({'_id': _id}, ignore_cache=ignore_cache)

        if metric is None:
            metric = QOTDResponseMetric(_id=_id)
            await metric.insert()

        return metric

    async def log(self, _id: int | str, ignore_cache: bool = False) -> Log | None:
        """log documents"""
        return await Log.find_one({'_id': _id}, ignore_cache=ignore_cache)

    async def tts_cache(self, _id: int, ignore_cache: bool = False) -> TTSCache | None:
        """tts cache documents"""
        return await TTSCache.find_one({'_id': _id}, ignore_cache=ignore_cache)
