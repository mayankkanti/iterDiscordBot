from discord.ext import commands

from iter_bot.core import BaseCog, ITERBot
from iter_bot.shared import EmbedType
from config import DEV_USER_ID

class KillCog(BaseCog):
    """
    Cog for shutdown.
    """

    def __init__(self, bot: ITERBot):
        super().__init__(bot)

    @commands.command(name='kill', description="Shutdown")
    async def kill(self, ctx: commands.Context):
        
        if (ctx.author.id != DEV_USER_ID):
            embed, file = await self.create_embed(
                EmbedType.WARNING, 'You are not him.', f'ITERBot walks away.')
            await ctx.send(embed=embed)
            return
        
        embed, file = await self.create_embed(
            EmbedType.ERROR, 'Aghhh he\'s too powerfull!!!', f'ITERBot was killed by  {ctx.author.mention}.')
        await ctx.send(embed=embed) 
        await self.bot.close()
        
        
        

async def setup(bot: ITERBot):
    await bot.add_cog(KillCog(bot))