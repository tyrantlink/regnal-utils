from enum import Enum

class TTSMode(Enum):
	def __str__(self) -> str:
		return self.name

	never = 0
	only_when_muted = 1
	always = 2

class TWBFMode(Enum):
	def __str__(self) -> str:
		return self.name

	true = 0
	whitelist = 1
	blacklist = 2
	false = 3

class AUCooldownMode(Enum):
	def __str__(self) -> str:
		return self.name

	none = 0
	user = 1
	channel = 2
	guild = 3

class AutoResponseMethod(Enum):
	def __str__(self) -> str:
		return self.name

	exact = 0
	contains = 1
	regex = 2 # different from data.regex, this method uses raw matching rather than adding word delimitation
	mention = 3
	disabled = 4

class AutoResponseType(Enum):
	def __str__(self) -> str:
		return self.name

	text = 0
	file = 1
	script = 2
	deleted = 3