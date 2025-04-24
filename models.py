from pydantic import BaseModel
from enum import Enum


class BotType(Enum):
    SMALL = 0
    LARGE = 1


class BotData(BaseModel):
    enabled: bool
    """whether the bot is enabled"""
    type: BotType
    """bot type"""
    logstream: str
    """parseable logstream"""
    token: str
    """bot token"""
    api_token: str
    """bot crapi token"""
    guilds: list[int]
    """guilds the bot is limited to (unrestricted if empty)"""
    disabled_extensions: list[str]
    """disabled extensions by name"""
    custom_extension: bool
    """whether the bot has a custom extension"""


class _ProjectConfig(BaseModel):
    log_level: int
    """log level (0-5)"""
    dev_bypass: bool
    """allows users on dev team to bypass all permissions"""
    base_guilds: list[int]
    """additional guilds small bots should join (emote servers, etc)"""
    git_branch: str
    """branch to pull from"""
    github_secret: str
    """github webhook secret"""
    pluralkit_token: str
    """pluralkit token"""
    plural_token: str
    """/plu/ral token"""
    contact_email: str
    """email used in pk user agent"""
    dm_proxy_channel: int
    """channel to proxy dms to, must be forum channel"""
    primary_bot_id: int
    """primary bot id, should be the only bot with access to dm proxy channel"""
    scripted_auto_response_repo: str
    """repo to pull scripted auto responses from and to direct users to"""
    base_version: list[int]
    """base version to start with when counting commits (e.g. [1, 0, 0])"""
    start_commit: str
    """commit hash to start counting from"""
    live_reload: bool
    """whether to live reload changes"""


class _ProjectWebhooks(BaseModel):
    support: str
    """forum channel for issues and suggestions"""
    support_issue_tag: int
    """tag id for issues"""
    support_suggestion_tag: int
    """tag id for suggestions"""
    updates: str
    """announcement channel for updates"""
    errors: str
    """text channel for error logging"""
    dm_proxy: str
    """webhook to send dms to, must direct to dm proxy channel (see config.dm_proxy_channel)"""


class _ProjectMongo(BaseModel):
    uri: str
    """mongodb connection uri"""


class _ProjectAPI(BaseModel):
    url: str
    """crapi url"""


class _ProjectParseable(BaseModel):
    base_url: str
    """base url for parseable"""
    token: str
    """parseable token"""
    logstream: str
    """hypervisor logstream"""
    logstream_padding: int
    """padding to keep all loggers the same length; -1 = auto"""


class _ProjectSauceNao(BaseModel):
    api_key: str
    """sauce nao api key"""


class _ProjectGoogleCloud(BaseModel):
    type: str
    """google cloud type"""
    project_id: str
    """google cloud project id"""
    private_key_id: str
    """google cloud private key id"""
    private_key: str
    """google cloud private key"""
    client_email: str
    """google cloud client email"""
    client_id: str
    """google cloud client id"""
    auth_uri: str
    """google cloud auth uri"""
    token_uri: str
    """google cloud token uri"""
    auth_provider_x509_cert_url: str
    """google cloud auth provider x509 cert url"""
    client_x509_cert_url: str
    """google cloud client x509 cert url"""


class _ProjectDeveloper(BaseModel):
    dev_mode: bool
    """if enabled, only loads certain extensions"""
    dev_extensions: list[str]
    """extensions to load when in dev mode"""


class Project(BaseModel):
    config: _ProjectConfig
    bot: BotData
    webhooks: _ProjectWebhooks
    mongo: _ProjectMongo
    api: _ProjectAPI
    parseable: _ProjectParseable
    saucenao: _ProjectSauceNao
    google_cloud: _ProjectGoogleCloud
    developer: _ProjectDeveloper


class Version(BaseModel):
    semantic: str
    """full semantic version (e.g. 1.0.0)"""
    commit: str
    """commit hash (short)"""
    commit_full: str
    """commit hash (full)"""
    timestamp: int
    """timestamp of commit"""
