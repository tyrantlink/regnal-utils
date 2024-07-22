from aiohttp import ClientSession
from asyncio import create_task
from datetime import datetime
from json import dumps
from enum import Enum


class LogLevel(Enum):
    NONE = 0
    CRITICAL = 1
    ERROR = 2
    WARNING = 3
    INFO = 4
    DEBUG = 5


class Logger:
    def __init__(
        self,
        url: str,
        logstream: str,
        logstream_padding: int,
        token: str,
        log_level: LogLevel
    ) -> None:
        self.base_url = url
        self.logstream = logstream
        self.logstream_padding = logstream_padding
        self.log_level = log_level
        self.url = f'{self.base_url}/{self.logstream}'
        self.headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json"
        }

    async def logstream_init(self) -> None:
        ...
        # async with ClientSession() as session:
        # 	logstreams = [d['name'] for d in await (await session.get(self.base_url,headers=self.headers)).json()]
        # 	if self.logstream not in logstreams:
        # 		async with session.put(self.url,headers=self.headers) as resp:
        # 			if resp.status != 200:
        # 				raise Exception(f'Logger failed with status {resp.status}\n{await resp.text()}')

    def _log(self, message: str, label: LogLevel, guild_id: int | None = None, metadata: dict | None = None) -> None:
        if label.value > self.log_level.value:
            return

        logstream = f'[{self.logstream.upper()}]'.ljust(
            self.logstream_padding+2
        )

        padded_label = f'[{label.name}]'.ljust(
            max([len(l.name) for l in LogLevel])+2
        )
        print(
            f'[{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}] {logstream} {padded_label} {message}'
        )
        # create_task(self._log_to_parseable(message,label,guild_id,metadata))

    async def _log_to_parseable(self, message: str, label: str, guild_id: int | None = None, metadata: dict | None = None) -> None:
        headers = {
            **self.headers,
            f'X-P-Tag-label': label,
            f'X-P-Tag-guild_id': str(guild_id).lower(),
            **{f'X-P-Meta-{k}': str(v) for k, v in (metadata or {}).items()}
        }

        async with ClientSession() as session:
            try:
                async with session.post(self.url, headers=headers, data=dumps([{'label': label, 'message': message}])) as resp:
                    if resp.status != 200:
                        raise Exception(f'Logger failed with status {resp.status}\n{await resp.text()}')
            except Exception:
                print('failed to log message to parseable')

    def custom(
        self,
        label: LogLevel,
        message: str,
        guild_id: int | None = None,
        **metadata
    ) -> None:
        self._log(message, label, guild_id, metadata)

    def info(
        self,
        message: str,
        guild_id: int | None = None,
        **metadata
    ) -> None:
        self.custom(LogLevel.INFO, message, guild_id, **metadata)

    def error(
        self,
        message: str,
        guild_id: int | None = None,
        **metadata
    ) -> None:
        self.custom(LogLevel.ERROR, message, guild_id, **metadata)

    def warning(
        self,
        message: str,
        guild_id: int | None = None,
        **metadata
    ) -> None:
        self.custom(LogLevel.WARNING, message, guild_id, **metadata)

    def debug(
        self,
        message: str,
        guild_id: int | None = None,
        **metadata
    ) -> None:
        self.custom(LogLevel.DEBUG, message, guild_id, **metadata)

    def critical(
        self,
        message: str,
        guild_id: int | None = None,
        **metadata
    ) -> None:
        self.custom(LogLevel.CRITICAL, message, guild_id, **metadata)
