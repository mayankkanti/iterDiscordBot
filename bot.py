import discord
from discord.ext import commands
from discord.ext import tasks
import scraper
import datetime
import urllib

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

OWNER = 467313214065999882
ADMIN_ROLE_Id = 1352853208774742127

@tasks.loop(minutes=10)
async def periodic_task():
    # Replace this with your desired functionality
    channel = discord.utils.get(bot.get_all_channels(), name="announcements")
    NOTICES = scraper.load_notices()
    new_notices = scraper.get_notices()
    new_notices = [
        notice for notice in new_notices
        if not any(existing[2] == notice[0] and existing[3] == notice[1] for existing in NOTICES)
    ]
    if new_notices:
        for notice in new_notices:
            TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            element = [len(NOTICES) + 1, TIME, notice[0], notice[1]]
            NOTICES.append(element)
            await channel.send("New notice! 📢")
            await channel.send(f"[{notice[0]}]({urllib.parse.urljoin("https://www.soa.ac.in/", notice[1])})")
        scraper.save_notices(NOTICES)
    await BOTLOGS.send("Checked Notice Board for new notices!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    global BOTLOGS
    BOTLOGS = bot.get_channel(1352856983476109454)
    if BOTLOGS:
        await BOTLOGS.send("Online! 🟢")
    else:
        print("BOTLOGS channel not found!")
    if not periodic_task.is_running():
        periodic_task.start()

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}! 🎉")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! 🏓 Latency: {latency}ms")        

@bot.command()
async def info(ctx):
    if ctx.author.id == OWNER or discord.utils.get(ctx.author.roles, id=ADMIN_ROLE_Id):
        # Admin help message
        help_message = """
**Admin Commands:**
- `!ping` - Check bot latency.
- `!purge <limit>` - Delete a specified number of messages.
- `!ban <@member> [reason]` - Ban a member from the server.
- `!kick <@member> [reason]` - Kick a member from the server.
- `!unban <username#discriminator>` - Unban a previously banned member.
- `!mute <@member> [reason]` - Mute a member.
- `!unmute <@member>` - Unmute a member.
"""
    else:
        # Regular user help message
        help_message = """
**User Commands:**
- `!ping` - Check bot latency.
"""

    await ctx.send(help_message)

@bot.command()
async def purge(ctx, limit):
    if ctx.author.id == OWNER or discord.utils.get(ctx.author.roles, id=ADMIN_ROLE_Id):
        await ctx.channel.purge(limit=int(limit) + 1)
        await ctx.send(f"Purged {limit} messages!", delete_after=5)
        await BOTLOGS.send(f"{limit} messages purged in {ctx.channel.mention}")
    else:
        await ctx.send("You do not have permission to use this command!")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    if ctx.author.id == OWNER or discord.utils.get(ctx.author.roles, id=ADMIN_ROLE_Id):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned! \nReason: {reason}")
        await BOTLOGS.send(f"{member.mention} has been banned! \nReason: {reason}")
    else:
        await ctx.send("You do not have permission to use this command!")
        
@bot.command()
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    if ctx.author.id == OWNER or discord.utils.get(ctx.author.roles, id=ADMIN_ROLE_Id):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked! \nReason: {reason}")
        await BOTLOGS.send(f"{member.mention} has been kicked! \nReason: {reason}")
    else:
        await ctx.send("You do not have permission to use this command!")
        
@bot.command()
async def unban(ctx, *, member):
    if ctx.author.id == OWNER or discord.utils.get(ctx.author.roles, id=ADMIN_ROLE_Id):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        
        for ban_entry in banned_users:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} has been unbanned!")
                await BOTLOGS.send(f"{user.mention} has been unbanned!")
                return
    else:
        await ctx.send("You do not have permission to use this command!")

@bot.command()
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
    if ctx.author.id == OWNER or discord.utils.get(ctx.author.roles, id=ADMIN_ROLE_Id):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        await ctx.send(f"{member.mention} has been muted! \nReason: {reason}")
        await BOTLOGS.send(f"{member.mention} has been muted! \nReason: {reason}")
    else:
        await ctx.send("You do not have permission to use this command!")
        
@bot.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.id == OWNER or discord.utils.get(ctx.author.roles, id=ADMIN_ROLE_Id):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} has been unmuted!")
        await BOTLOGS.send(f"{member.mention} has been unmuted!")
    else:
        await ctx.send("You do not have permission to use this command!")

bot.run("<add discord bot token here>")