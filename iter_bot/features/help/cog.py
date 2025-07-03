from discord.ext import commands

from iter_bot.core import BaseCog, ITERBot
from iter_bot.shared import EmbedType
from config import TASK_FREQUENCY

class HelpCog(BaseCog):
    """
    Cog for help command
    """

    def __init__(self, bot: ITERBot):
        super().__init__(bot)

    @commands.command(name='help', description="Lists available commands")
    async def help(self, ctx: commands.Context):
        help_text = f"""
        **Available Commands:**
        
        🏓 `? ping` - Check the bot's latency
        👋 `? hello` - Say hello to the bot
        📌 `? checknotices` - Manually check for new ITER notices
        🔧 `? kill` - Shutdown the bot (Developer only)
        ❓ `? help` - Show this help message
        
        ! Notice board check frequency - {TASK_FREQUENCY} minutes.
        """
        
        embed, file = await self.create_embed(
            EmbedType.INFORMATION, '🤖 ITER Bot Help', help_text
        )

        await ctx.send(embed=embed, file=file) if file else await ctx.send(embed=embed)

async def setup(bot: ITERBot):
    await bot.add_cog(HelpCog(bot))