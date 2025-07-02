import logging
import time
from .noticescrapper import get_new_notices, save_notices
from discord.ext import commands, tasks

from iter_bot.core import BaseCog, ITERBot
from iter_bot.shared import EmbedType

from config import NCHANNEL, LCHANNEL


logger = logging.getLogger(__name__)

class NoticeCog(BaseCog):
    """
    Cog for checking notices
    """

    def __init__(self, bot: ITERBot):
        super().__init__(bot)
        self.times_checked = 0
        self.bot.loop.create_task(self.start_notice_checker())

    async def start_notice_checker(self):
        await self.bot.wait_until_ready()
        logger.info("Bot is ready. Starting notice_checker task.")
        self.notice_checker.start()
    
    @tasks.loop(minutes=10)
    async def notice_checker(self):
        channel = self.bot.get_channel(NCHANNEL)
        if channel is None:
            logger.critical("Notice channel not found. Unable to send and save notices. \n")
            return
        
        new_notices, all_notices = get_new_notices()
        if new_notices:
            for notice in new_notices:
                title = notice["Title"]
                link = notice["Link"]
                                
                embed, file = await self.create_embed(
                    EmbedType.INFORMATION, title , f"[Click here to view the notice]({link})")
                await channel.send(embed=embed)
            
            save_notices(all_notices)

        # Code for last update
        timestamp = f"<t:{int(time.time())}:R>"
        self.times_checked += 1
        await channel.edit(topic=f"Last Checked {timestamp} | Checked {self.times_checked}")
                
async def setup(bot: ITERBot):
    await bot.add_cog(NoticeCog(bot))