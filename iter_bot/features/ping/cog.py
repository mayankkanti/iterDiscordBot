from discord.ext import commands

from iter_bot.core import BaseCog, ITERBot
from iter_bot.shared import EmbedType


class PingCog(BaseCog):
    """
    Cog for basic ping command to check bot latency
    """

    def __init__(self, bot: ITERBot):
        super().__init__(bot)

    @commands.command(name='ping', description="Check the bot's latency")
    async def ping(self, ctx: commands.Context):

        latency = round(self.bot.latency * 1000, 2)
        embed, file = await self.create_embed(
            EmbedType.NORMAL, 'Pong! 🏓', f'**Bot latency**: {latency}ms'
        )

        await ctx.send(embed=embed, file=file)

    @commands.command(name='hello', description="Check the bot's latency")
    async def hello(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000, 2)
        embed, file = await self.create_embed(
            EmbedType.NORMAL, 'Hi! 👋', f'**Bot latency**: {latency}ms'
        )

        await ctx.send(embed=embed, file=file)

async def setup(bot: ITERBot):
    await bot.add_cog(PingCog(bot))