import logging

from discord.ext import commands

from iter_bot.core.bot import ITERBot
from iter_bot.shared import EmbedType, get_embed

logger = logging.getLogger(__name__)


class BaseCog(commands.Cog):
    """Base cog class that all other cogs should inherit from"""

    def __init__(self, bot: ITERBot) -> None:
        self.bot = bot
        logger.info(f'Initialized {self.__class__.__name__}')

    async def create_embed(self, type: EmbedType, title: str, description: str):
        return await get_embed(type, title, description)

    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        embed, file = await self.create_embed(EmbedType.ERROR, 'Error', str(error))
        
        await ctx.send(embed=embed, file=file)
        logger.error(f'Error in {ctx.command.name}: {str(error)}')