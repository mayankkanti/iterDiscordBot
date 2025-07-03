import logging
import time
import pytz
from datetime import datetime
from .noticescrapper import get_new_notices, save_notices
from discord.ext import commands, tasks

from iter_bot.core import BaseCog, ITERBot
from iter_bot.shared import EmbedType

from config import NCHANNEL, TASK_FREQUENCY


logger = logging.getLogger(__name__)

class NoticeCog(BaseCog):
    """
    Cog for checking notices
    """

    def __init__(self, bot: ITERBot):
        super().__init__(bot)
        self.times_checked = -1
        self.today_day = -1
        self.start_time = time.time()
        self.bot.loop.create_task(self.start_notice_checker())

    async def start_notice_checker(self):
        await self.bot.wait_until_ready()
        logger.info("Bot is ready. Starting notice_checker task.")
        self.notice_checker.start()
    
    @tasks.loop(minutes=TASK_FREQUENCY)
    async def notice_checker(self):
        channel = self.bot.get_channel(NCHANNEL)
        if channel is None:
            logger.critical("Notice channel not found. Unable to send and save notices. \n")
            return
        
        new_notices, all_notices = get_new_notices()
        if new_notices:
            await channel.send(content = "@everyone")
            for notice in new_notices:
                title = notice["Title"]
                link = notice["Link"]
                                
                embed, file = await self.create_embed(
                    EmbedType.INFORMATION, title , f"[Click here to view the notice]({link})")
                await channel.send(embed=embed)
            
            save_notices(all_notices)

        # Code for last update
        today_day = datetime.now(pytz.timezone("Asia/Kolkata")).day
        if self.today_day == today_day:
            self.times_checked += 1
        else:
            self.times_checked = 1
            self.today_day = today_day
        timestamp = f"<t:{int(time.time())}:R>"
        
        uptime_secs = int(time.time() - self.start_time)
        uptime = f"{uptime_secs // 3600}h {(uptime_secs % 3600) // 60}m"
        
        topic = f'Last Checked: {timestamp} | Today: {self.times_checked} time' + ("s" if self.times_checked != 1 else "") + f' | Uptime: {uptime}'
        
        await channel.edit(topic=topic)
        logger.info("Ran notice_checker task at %s", datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S"))

    @commands.command(name='checknotices', description="Force a notice check task.")
    async def checknotices(self, ctx: commands.Context):
        embed, file = await self.create_embed(
            EmbedType.INFORMATION, '📌 Forced Notice Check', 'A manual notice check was triggered. Scanning for updates...'
        )

        await ctx.send(embed=embed, file=file) if file else await ctx.send(embed=embed)
        await self.notice_checker()
                
async def setup(bot: ITERBot):
    await bot.add_cog(NoticeCog(bot))