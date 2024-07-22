from pydantic import BaseModel, Field
from typing import Optional, Any
from .ext.enums import TTSMode
from datetime import timedelta
from beanie import Document


class User(Document):
    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    class Settings:
        name = 'users'
        use_cache = True
        validate_on_save = True
        use_state_management = True
        cache_expiration_time = timedelta(seconds=1)

    class UserConfig(BaseModel):
        class UserConfigGeneral(BaseModel):
            no_track: bool = Field(
                default=False,
                description='disable found au, message counts, command usage logging and api usage logging\n\nsince found au is disabled, you will not be able to use the --au <id> argument'
            )
            private_profile: bool = Field(
                default=False,
                description='make your profile private\n\nif enabled, your profile will only show id, username, display name and creation date'
            )
            talking_stick: bool = Field(
                default=True,
                description='allows you to recieve the talking stick\n\ndisable to remove potential unwanted pings'
            )
            hide_commands: bool = Field(
                default=True,
                description='commands used will only be visible to you\n\neven disabled, some commands with sensitive information will still be hidden'
            )
            auto_responses: bool = Field(
                default=True,
                description='enable/disable auto responses\n\nif guild.auto_responses.mode is set to disabled, this will be ignored'
            )
            developer_mode: bool = Field(
                default=False,
                description='enable developer mode\n\nif enabled, shows more information in some commands, mainly auto responses'
            )
            disable_media_link_replacement: bool = Field(
                default=False,
                description='disable media link replacement\n\nif enabled, media links will not be replaced with their respective embeds'
            )

        class UserConfigTTS(BaseModel):
            mode: TTSMode = Field(
                default=TTSMode.only_when_muted,
                description='when to use tts'
            )
            name: Optional[str] = Field(
                default=None,
                min_length=1,
                max_length=32,
                description='name used by tts\n\nif not set, your current display name will be used'
            )
            auto_join: bool = Field(
                default=False,
                description='automatically join voice channel\n\nif disabled, you will have to invite tts manually with {cmd_ref[tts join]}'
            )
            voice: Optional[str] = Field(
                default=None,
                description='voice used by tts\n\nif not set, guild.tts.default_voice will be used'
            )
            speaking_rate: float = Field(
                default=0.8,
                ge=0.25,
                le=4,
                description='speaking rate used by tts'
            )
            text_correction: bool = Field(
                default=True,
                description='silently corrects text so it\'s more accurately pronounced'
            )

        class UserConfigAutoResponses(BaseModel):
            disabled: list[str] = Field(
                default=[],
                description='auto responses disabled'
            )

        general: UserConfigGeneral = Field(
            default=UserConfigGeneral(),
            description='general options'
        )
        tts: UserConfigTTS = Field(
            default=UserConfigTTS(),
            description='text-to-speech options'
        )

    class UserData(BaseModel):
        class UserDataAPI(BaseModel):
            token: Optional[str] = Field(
                default=None,
                pattern=r'^\$2[ayb]\$.{56}$',
                description='api token'
            )
            permissions: int = Field(default=0, description='api permissions')

        class UserDataAutoResponses(BaseModel):
            found: list[str] = Field(
                default=[],
                description='auto responses found'
            )
            disabled: list[str] = Field(
                default=[],
                description='auto responses disabled'
            )

        class UserDataStatistics(BaseModel):
            messages: dict[str, int] = Field(
                default={},
                description='message counts by guild id\n\nlegacy data under _legacy'
            )
            command_usage: int = Field(default=0, description='commands used')
            api_usage: int = Field(default=0, description='api calls made')
            tts_usage: int = Field(
                default=0,
                description='tts characters used'
            )

        api: UserDataAPI = Field(default=UserDataAPI(), description='api data')
        auto_responses: UserDataAutoResponses = Field(
            default=UserDataAutoResponses(),
            description='auto response data'
        )
        statistics: UserDataStatistics = Field(
            default=UserDataStatistics(),
            description='user statistics'
        )
        dm_threads: dict[str, int] = Field(
            default={},
            description='dictionary of dm threads {bot_id:thread_id}'
        )
        modmail_threads: dict[str, int] = Field(
            default={},
            description='dictionary of modmail threads {"guild_id:modmail_id":latest_read_message_index}'
        )
        flags: int = Field(default=0, description='flags the user has')
        extra: dict[str, Any] = Field(default={}, description='extra data')

    id: int = Field(description='user\'s discord id')
    username: str = Field(description='user\'s discord username')
    config: UserConfig = Field(default=UserConfig(), description='user config')
    data: UserData = Field(default=UserData(), description='user data')
