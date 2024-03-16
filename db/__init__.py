from .documents.inf import Inf,INFTextCorrection,INFExcuses,INFInsults,INFEightBall,INFBees
from .documents import User,Guild,AutoResponse,AutoResponseFileMask,Log
from .documents.ext.enums import AutoResponseMethod
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database as _Database
from beanie import init_beanie,PydanticObjectId


class _MongoNew:
	@staticmethod
	def user(id:int,username:str) -> User:
		return User(id=id,username=username)

	@staticmethod
	def guild(id:int,name:str,owner:int) -> Guild:
		return Guild(id=id,name=name,owner=owner)

	@staticmethod
	def auto_response(id:int,method:AutoResponseMethod,trigger:str,response:str) -> AutoResponse:
		return AutoResponse(id=id,method=method,trigger=trigger,response=response)

	@staticmethod
	def au_mask(au:str) -> AutoResponseFileMask:
		return AutoResponseFileMask(au=au)
	
	@staticmethod
	def log(id:int,data:dict) -> Log:
		return Log(id=id,data=data)

class MongoDatabase:
	def __init__(self,mongo_uri:str) -> None:
		self._client:_Database = AsyncIOMotorClient(mongo_uri,serverSelectionTimeoutMS=5000)['regnal']

	async def connect(self) -> None:
		await init_beanie(self._client,document_models=[User,Guild,AutoResponse,AutoResponseFileMask,Log,INFTextCorrection,INFExcuses,INFInsults,INFEightBall,INFBees])

	@property
	def new(self) -> _MongoNew:
		return _MongoNew

	@property
	def inf(self) -> Inf:
		return Inf

	async def user(self,_id:int|str,ignore_cache:bool=False) -> User|None:
		"""user documents"""
		return await User.find_one({'_id': _id},ignore_cache=ignore_cache)

	async def guild(self,_id:int|str,ignore_cache:bool=False) -> Guild|None:
		"""guild documents"""
		return await Guild.find_one({'_id': _id},ignore_cache=ignore_cache)

	async def auto_response(self,_id:int|str,ignore_cache:bool=False) -> AutoResponse|None:
		"""auto response documents"""
		return await AutoResponse.find_one({'_id': _id},ignore_cache=ignore_cache)

	async def au_mask(self,_id:PydanticObjectId,ignore_cache:bool=False) -> AutoResponseFileMask|None:
		"""auto response file mask documents"""
		return await AutoResponseFileMask.find_one({'_id':_id},ignore_cache=ignore_cache)
	
	async def log(self,_id:int|str,ignore_cache:bool=False) -> Log|None:
		"""log documents"""
		return await Log.find_one({'_id': _id},ignore_cache=ignore_cache)