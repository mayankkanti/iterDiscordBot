import logging
from pathlib import Path
from typing import List

from discord import Intents, Message
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ITERBot(commands.AutoShardedBot):
    
    DEFAULT_PREFIX = ['? ', 'iter ', 'ITER ']
    FEATURES_DIRECTORY = Path('iter_bot/features')

    def __init__(self) -> None:
        intents = Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=self.get_prefix,
            intents=intents,
            help_command=None,
        )

    async def get_prefix(self, message: Message) -> List[str]:
        return commands.when_mentioned_or(*self.DEFAULT_PREFIX)(self, message)

    async def load_cogs(self) -> None:
        if not self.FEATURES_DIRECTORY.exists():
            logger.error(f'Features directory not found: {self.FEATURES_DIRECTORY}')
            return

        for feature_dir in self.FEATURES_DIRECTORY.iterdir():
            if not feature_dir.is_dir():
                continue

            cog_file = feature_dir / 'cog.py'
            if not cog_file.exists():
                logger.error(f"No cog found in dir: {feature_dir}")
                continue

            try:
                cog_path = f'iter_bot.features.{feature_dir.name}.cog'
                await self.load_extension(cog_path)
                logger.info(f'Loaded feature: {feature_dir.name} ({cog_path})')
            except Exception as e:
                logger.error(f'Failed to load feature {feature_dir.name}: {str(e)}')

    async def setup_hook(self) -> None:
        await self.load_cogs()

    async def on_ready(self) -> None:
        logger.info(f'Logged in as {self.user.name}')
        logger.info(f'Bot is in {len(self.guilds)} guilds')

    async def on_error(self, event: str, *args, **kwargs) -> None:
        logger.error(f'Error in event {event}')
        if args:
            logger.error(f'Event args: {args}')
        if kwargs:
            logger.error(f'Event kwargs: {kwargs}')
        logger.error('Full traceback:', exc_info=True)