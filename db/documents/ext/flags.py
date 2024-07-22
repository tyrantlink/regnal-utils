from enum import IntFlag


class UserFlags(IntFlag):
    ADMIN = 1 << 0
    """bypasses all permission checks"""
    AUTO_RESPONSE_BANNED = 1 << 1
    """forces all auto responses to be ignored"""
    UNLIMITED_TTS = 1 << 2
    """bypasses all TTS message length checks"""


class APIFlags(IntFlag):
    ADMIN = 1 << 0
    """bypasses all permission checks"""
    BOT = 1 << 1
    """allows access to /i (internal) api endpoint"""
    RELOAD_AU = 1 << 2
    """allows access to /au_reload api endpoint"""
