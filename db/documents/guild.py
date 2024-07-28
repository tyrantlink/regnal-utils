from .ext.enums import TWBFMode, AUCooldownMode
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import timedelta
from datetime import datetime
from beanie import Document
from pytz import timezone


class GuildDataQOTDQuestion(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=256,
        description='question to be asked'
    )
    author: str = Field(
        min_length=1,
        max_length=32,
        description='author of the question'
    )
    icon: str = Field(
        min_length=1,
        max_length=200,
        description='icon of the author'
    )


class Guild(Document):
    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    class Settings:
        name = 'guilds'
        use_cache = True
        validate_on_save = True
        use_state_management = True
        cache_expiration_time = timedelta(seconds=1)

    class GuildConfig(BaseModel):
        class GuildConfigGeneral(BaseModel):
            hide_commands: TWBFMode = Field(
                default=TWBFMode.false,
                description='commands will only be visible to the user\n\neven disabled, some commands with sensitive information will still be hidden\n\ntrue: commands will always be hidden\nwhitelist: commands will be hidden in selected channels\nblacklist: commands will be hidden in all channels except selected channels\nfalse: commands will never be force hidden'
            )
            embed_color: str = Field(
                default='69ff69',
                min_length=6,
                max_length=6,
                pattern=r'^[a-fA-F\d]{6}$',
                description='color used by embeds\n\nif not set, the default color will be used'
            )
            timezone: str = Field(
                default='America/Los_Angeles',
                min_length=2,
                max_length=32,
                description='timezone used for events\n\nplease refer to [this list on wikipedia](<https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>) for a list of options'
            )
            replace_media_links: bool = Field(
                default=False,
                description='replaces media links with urls that have better discord embed support'
            )
            moderator_role: Optional[int] = Field(
                default=None,
                description='role that will be pinged for emergency situations (e.g. anti scam bot protection)'
            )
            anti_scam_bot: bool = Field(
                default=False,
                description='enable/disable anti scam bot\n\nif enabled, detect self bots and prompt admins to ban them'
            )

        class GuildConfigAutoResponses(BaseModel):
            enabled: TWBFMode = Field(
                default=TWBFMode.true,
                description='enable/disable auto responses\n\ntrue: auto responses enabled in all channels\nwhitelist: auto responses enabled in selected channels\nblacklist: auto responses disabled in selected channels\nfalse: auto responses disabled in all channels'
            )
            cooldown: int = Field(
                default=0,
                ge=0,
                description='cooldown between auto responses in seconds'
            )
            cooldown_mode: AUCooldownMode = Field(
                default=AUCooldownMode.channel,
                description='cooldown mode\n\nnone: no cooldown\nuser: cooldown per user\nchannel: cooldown per channel\nguild: cooldown server-wide'
            )
            allow_cross_guild_responses: bool = Field(
                default=False,
                description='allow custom auto responses from other guilds to be used (using the --au argument)\n\nvery, very dangerous permission, allows users to send arbitrary auto responses\nuse at your own risk.'
            )
            custom_only: bool = Field(
                default=False,
                description='only use custom auto responses, ignoring all other types'
            )

        class GuildConfigLogging(BaseModel):
            enabled: bool = Field(
                default=False,
                description='enable/disable logging\n\nif disabled, all logging will be disabled\nif enabled you can view logs on https://logs.regn.al'
            )
            channel: Optional[int] = Field(
                default=None,
                description='channel used for some logging\nfull logs still visible on https://logs.regn.al'
            )
            log_bots: bool = Field(
                default=False,
                description='enable/disable logging of bot messages'
            )
            log_commands: bool = Field(
                default=True,
                description='enable/disable logging of command usage'
            )
            deleted_messages: bool = Field(
                default=False,
                description='enable/disable logging of deleted messages'
            )
            edited_messages: bool = Field(
                default=False,
                description='enable/disable logging of edited messages'
            )
            member_join: bool = Field(
                default=False,
                description='enable/disable logging of member joins'
            )
            member_leave: bool = Field(
                default=False,
                description='enable/disable logging of member leaves'
            )
            member_ban: bool = Field(
                default=False,
                description='enable/disable logging of member bans'
            )
            member_unban: bool = Field(
                default=False,
                description='enable/disable logging of member unbans'
            )
            activity_roles: bool = Field(
                default=False,
                description='enable/disable logging of activity role changes'
            )
            pluralkit_support: bool = Field(
                default=False,
                description='suppress messages deleted by pluralkit'
            )

        class GuildConfigQOTD(BaseModel):
            enabled: bool = Field(
                default=False,
                description='enable/disable qotd\n\nif disabled, all qotd will be disabled'
            )
            channel: Optional[int] = Field(default=None)
            time: str = Field(
                default='00:00',
                min_length=5,
                max_length=5,
                pattern=r'^\d{2}:\d{2}$',
                description='time of day to send qotd\n\nformat: HH:MM (24 hour)\nfollows guild set timezone'
            )

        class GuildConfigTTS(BaseModel):
            enabled: bool = Field(
                default=True,
                description='allow tts to be used'
            )
            channels: list[int] = Field(
                default=[],
                description='channels where tts is allowed\n\nvoice-text channels will always allow tts'
            )
            default_voice: Optional[str] = Field(
                default=None,
                description='default voice used by tts\n\nif not set, the default voice (en-US-Neural2-H) will be used'
            )

        class GuildConfigTalkingStick(BaseModel):
            enabled: bool = Field(
                default=False,
                description='daily random roll to give an active user a specific role\n\nintended to give users send_messages permissions in a channel, but can be used for anything'
            )
            channel: Optional[int] = Field(
                default=None,
                description='channel used to announce the talking stick'
            )
            role: Optional[int] = Field(
                default=None,
                description='role given to the user'
            )
            limit: Optional[int] = Field(
                default=None,
                description='role that limits who can get the talking stick\n\nif not set, all users can get the talking stick'
            )
            time: str = Field(
                default='09:00',
                min_length=5, max_length=5,
                pattern=r'^\d{2}:\d{2}$',
                description='time of day talking stick is announced\n\nformat: HH:MM (24 hour)\nfollows guild set timezone'
            )
            announcement_message: str = Field(
                default='congrats {user} you have the talking stick.',
                max_length=200,
                description='message sent when a user gets the talking stick\n\nformat: {user} is replaced with the user\'s mention'
            )

        class GuildConfigModMail(BaseModel):
            enabled: bool = Field(
                default=False,
                description='enable/disable mod mail'
            )
            channel: Optional[int] = Field(
                default=None,
                description='forum channel used for mod mail'
            )
            allow_anonymous: bool = Field(
                default=True,
                description='allow users to send mod mail anonymously'
            )

        class GuildConfigActivityRoles(BaseModel):
            enabled: bool = Field(
                default=False,
                description='enable/disable activity roles'
            )
            role: Optional[int] = Field(
                default=None,
                description='role given to active users'
            )
            timeframe: int = Field(
                default=7,
                ge=1,
                description='number of days to look back for activity'
            )
            max_roles: int = Field(
                default=10,
                ge=1,
                description='maximum number of roles to give'
            )
            ignored_roles: list[int] = Field(
                default=[],
                description='roles that are ignored for activity roles'
            )

        class GuildConfigSauceNao(BaseModel):
            api_key: Optional[str] = Field(
                default=None,
                description='sauce nao api key\n\nif not set, the default api key will be used (with a very low limit)]\n\nget an api key at https://saucenao.com/user.php?page=account-upgrades'
            )

        general: GuildConfigGeneral = Field(
            default=GuildConfigGeneral(),
            description='general options'
        )
        auto_responses: GuildConfigAutoResponses = Field(
            default=GuildConfigAutoResponses(),
            description='auto response options'
        )
        logging: GuildConfigLogging = Field(
            default=GuildConfigLogging(),
            description='logging options'
        )
        qotd: GuildConfigQOTD = Field(
            default=GuildConfigQOTD(),
            description='qotd options'
        )
        tts: GuildConfigTTS = Field(
            default=GuildConfigTTS(),
            description='text-to-speech options'
        )
        talking_stick: GuildConfigTalkingStick = Field(
            default=GuildConfigTalkingStick(),
            description='talking stick options'
        )
        modmail: GuildConfigModMail = Field(
            default=GuildConfigModMail(),
            description='mod mail options'
        )
        activity_roles: GuildConfigActivityRoles = Field(
            default=GuildConfigActivityRoles(),
            description='activity roles options'
        )
        saucenao: GuildConfigSauceNao = Field(
            default=GuildConfigSauceNao(),
            description='sauce nao options'
        )

    class GuildData(BaseModel):
        class GuildDataAutoResponses(BaseModel):
            whitelist: list[int] = Field(
                default=[],
                description='channels where auto responses are whitelisted'
            )
            blacklist: list[int] = Field(
                default=[],
                description='channels where auto responses are blacklisted'
            )
            overrides: dict[str, dict] = Field(
                default={},
                description='auto response overrides'
            )
            imported_scripts: list[str] = Field(
                default=[],
                description='scripted auto responses that have been imported'
            )

        class GuildDataQOTD(BaseModel):
            last: int = Field(
                default=0,
                ge=0,
                description='day of last question sent'
            )
            last_thread: Optional[int] = Field(
                default=None,
                description='thread id of last question sent'
            )
            nextup: list[GuildDataQOTDQuestion] = Field(
                default=[],
                description='questions that will be sent next (custom)'
            )
            asked: dict[str, str] = Field(
                default={},
                description='question asked stored as {pack:bitstring}'
            )
            packs: list[str] = Field(
                default=['base'],
                description='question packs'
            )

        class GuildDataTalkingStick(BaseModel):
            current: Optional[int] = Field(
                default=None,
                description='user currently holding the talking stick'
            )
            last: int = Field(
                default=0,
                ge=0,
                description='day of last talking stick given'
            )

        class GuildDataHideCommands(BaseModel):
            whitelist: list[int] = Field(
                default=[],
                description='channels where commands are whitelisted'
            )
            blacklist: list[int] = Field(
                default=[],
                description='channels where commands are blacklisted'
            )

        class GuildDataTTS(BaseModel):
            banned: list[int] = Field(
                default=[],
                description='users banned from using tts'
            )

        class GuildDataActivityRoles(BaseModel):
            last_day: int = Field(
                default=0,
                ge=0,
                description='day of last activity role update'
            )

        class GuildDataStatistics(BaseModel):
            messages: int = Field(
                default=0,
                ge=0,
                description='total messages sent'
            )
            commands: int = Field(
                default=0,
                ge=0,
                description='total commands used'
            )
            questions: int = Field(
                default=0,
                ge=0,
                description='total questions asked'
            )
            tts: int = Field(
                default=0,
                ge=0,
                description='total tts characters used'
            )

        activity: dict[str, dict[str, int]] = Field(
            default={},
            max_length=31,
            description='activity data for at most last 30 days\n\nformat {day:{user_id:count}}'
        )
        auto_responses: GuildDataAutoResponses = Field(
            default=GuildDataAutoResponses(),
            description='auto response data'
        )
        permissions: dict[str, list[str]] = Field(
            default={'@everyone': []},
            description='permissions for user/roles\n\nformat {id:[permission1,...]}'
        )
        qotd: GuildDataQOTD = Field(
            default=GuildDataQOTD(),
            description='qotd data'
        )
        talking_stick: GuildDataTalkingStick = Field(
            default=GuildDataTalkingStick(),
            description='talking stick data'
        )
        hide_commands: GuildDataHideCommands = Field(
            default=GuildDataHideCommands(),
            description='hide commands data'
        )
        tts: GuildDataTTS = Field(
            default=GuildDataTTS(),
            description='text-to-speech data'
        )
        activity_roles: GuildDataActivityRoles = Field(
            default=GuildDataActivityRoles(),
            description='activity roles data'
        )
        leaderboards: dict[str, dict[str, int]] = Field(
            default={},
            description='leaderboard data'
        )
        modmail_threads: dict[str, int] = Field(
            default={},
            description='mod mail threads\n\nformat {thread_id:modmail_id}'
        )
        statistics: GuildDataStatistics = Field(
            default=GuildDataStatistics(),
            description='guild statistics'
        )
        flags: int = Field(default=0, description='flags the guild has')
        extra: dict[str, Any] = Field(default={}, description='extra data')

    id: int = Field(description='guild\'s discord id')
    name: str = Field(description='guild\'s discord name')
    owner: int | None = Field(description='guild\'s discord owner id')
    attached_bot: int | None = Field(
        default=None,
        description='bot attached to the guild'
    )
    config: GuildConfig = Field(
        default=GuildConfig(),
        description='guild config'
    )
    data: GuildData = Field(default=GuildData(), description='guild data')

    def get_current_day(self) -> int:
        _guild_timezone = timezone(self.config.general.timezone)
        return (datetime.now(_guild_timezone)-datetime(2021, 5, 5, tzinfo=_guild_timezone)).days

    def get_day_in(
        self,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0
    ) -> int:
        _guild_timezone = timezone(self.config.general.timezone)
        return (
            datetime.now(_guild_timezone)
            + timedelta(
                days=days,
                hours=hours,
                minutes=minutes,
                seconds=seconds)
            - datetime(2021, 5, 5, tzinfo=_guild_timezone)
        ).days
