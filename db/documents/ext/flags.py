from enum import IntFlag

class UserFlags(IntFlag):
	AUTO_RESPONSE_BANNED = 1 << 0 # force ignore all auto responses
	ADMIN                = 1 << 1 # bypass all permission checks
	UNLIMITED_TTS        = 1 << 2 # bypass all TTS length checks

class APIFlags(IntFlag):
	ADMIN     = 1 << 0 # bypass all permission checks
	BOT       = 1 << 1 # allows access to /i endpoint
	RELOAD_AU = 1 << 2 # allows access to /au_reload api endpoint