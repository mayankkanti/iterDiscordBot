import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
import os
import dotenv
from datetime import datetime
import urllib

import scraper

# VARIABLES
dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')
OWNER = int(os.getenv('OWNER'))
ADMIN = int(os.getenv('ADMIN'))
LOGS = int(os.getenv('LOG_CHANNEL'))
SERVERID = int(os.getenv('SERVER_ID'))
GUILD = discord.Object(id=SERVERID)

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command('help')

def search_for_notice_updates():
    SAVED_NOTICES = scraper.load_notices()
    FETCH_NOTICES = scraper.get_notices()
    NEW_NOTICES = [notice for notice in FETCH_NOTICES if not any(existing[2] == notice[0] and existing[3] == urllib.parse.urljoin('https://www.soa.ac.in/', notice[1]) for existing in SAVED_NOTICES)]
    return NEW_NOTICES

def save_notices(notices):
    NOTICES = scraper.load_notices()
    for notice in notices:
        element = [len(NOTICES) + 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), notice[0], urllib.parse.urljoin('https://www.soa.ac.in/', notice[1])]
        NOTICES.append(element)
    scraper.save_notices(NOTICES)

# User Commands

@bot.tree.command(name='help', description='Command help',guild=GUILD)
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Help - Command List",
        description="Here are the available commands:",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    embed.add_field(name="/ping", value="Check bot latency.", inline=False)
    embed.add_field(name="/hello", value="Get a greeting message.", inline=False)
    embed.add_field(name="/say", value="Make the bot say something.", inline=False)
    embed.add_field(name="/purge", value="Delete a specified number of messages (Admin only).", inline=False)
    embed.add_field(name="/kick", value="Kick a user (Admin only).", inline=False)
    embed.add_field(name="/ban", value="Ban a user (Admin only).", inline=False)
    embed.add_field(name="/unban", value="Unban a user (Admin only).", inline=False)
    embed.set_footer(text="made by Mayank!")
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name='ping', description='Ping bot', guild=GUILD)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! Latency: {round(bot.latency * 1000)}ms')


@bot.tree.command(name='say', description='Make the bot say something!',guild=GUILD)
@app_commands.describe(say='Make the bot say something.')
async def hello(interaction: discord.Interaction, say: str):
    await interaction.response.send_message(f'{say}')

# Moderation Commands

@bot.tree.command(name='purge', description='Delete specified number of messages.',guild=GUILD)
@app_commands.describe(limit='Delete a specified number of messages.')
async def purge(interaction: discord.Interaction, limit: int):
    if interaction.user.id == OWNER or discord.utils.get(interaction.user.roles, id=ADMIN):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=limit)
        await interaction.followup.send(f'Purged {limit} messages!', ephemeral=True)
        
        embed = discord.Embed(
            title="Purge",
            description=f"{interaction.user} purged {limit} messages in {interaction.channel}.",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        await bot.get_channel(LOGS).send(embed=embed)
    else:
        await interaction.response.send_message('You do not have permission to use this command.', ephemeral=True)

@bot.tree.command(name='kick', description='Kick a user.',guild=GUILD)
@app_commands.describe(user='Kick a user.')
async def kick(interaction: discord.Interaction, user: discord.Member, *, reason: str):
    if interaction.user.id == OWNER or discord.utils.get(interaction.user.roles, id=ADMIN):
        if user.guild_permissions.administrator:
            await interaction.response.send_message('You cannot kick an admin.')
        else:
            await user.kick(reason=reason)
            await interaction.response.send_message(f'{user} has been kicked for {reason}.')
            
            embed = discord.Embed(
                title="Kick",
                description=f"{interaction.user} kicked {user} for {reason}.",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            await bot.get_channel(LOGS).send(embed=embed)
    else:
        await interaction.response.send_message('You do not have permission to use this command.')

@bot.tree.command(name='ban', description='Ban a user.',guild=GUILD)
@app_commands.describe(user='Ban a user.')
async def ban(interaction: discord.Interaction, user: discord.Member, *, reason: str):
    if interaction.user.id == OWNER or discord.utils.get(interaction.user.roles, id=ADMIN):
        if user.guild_permissions.administrator:
            await interaction.response.send_message('You cannot ban an admin.')
        else:
            await user.ban(reason=reason)
            await interaction.response.send_message(f'{user} has been banned for {reason}.')
            
            embed = discord.Embed(
                title="Ban",
                description=f"{interaction.user} banned {user} for {reason}.",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            await bot.get_channel(LOGS).send(embed=embed)
    else:
        await interaction.response.send_message('You do not have permission to use this command.')

@bot.tree.command(name='unban', description='Unban a user.',guild=GUILD)
@app_commands.describe(user='Unban a user.')
async def unban(interaction: discord.Interaction, *, user: str):
    if interaction.user.id == OWNER or discord.utils.get(interaction.user.roles, id=ADMIN):
        banned_users = await interaction.guild.bans()
        member_name, member_discriminator = user.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await interaction.guild.unban(user)
                await interaction.response.send_message(f'{user} has been unbanned.')
                
                embed = discord.Embed(
                    title="Unban",
                    description=f"{interaction.user} unbanned {user}.",
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                await bot.get_channel(LOGS).send(embed=embed)
                return
        await interaction.response.send_message(f'{user} was not found in the ban list.')
    else:
        await interaction.response.send_message('You do not have permission to use this command.')

@bot.tree.command(name='mute', description='Mute a user.', guild=GUILD)
@app_commands.describe(user='Mute a user.')
async def mute(interaction: discord.Interaction, user: discord.Member):
    if interaction.user.id == OWNER or discord.utils.get(interaction.user.roles, id=ADMIN):
        role = discord.utils.get(interaction.guild.roles, name='Muted')
        if role:
            await user.add_roles(role)
            await interaction.response.send_message(f'{user} has been muted.')
            embed = discord.Embed(
                title="Mute",
                description=f"{interaction.user} muted {user}.",
                color=discord.Color.orange(),
                timestamp=datetime.now()
            )
            await bot.get_channel(LOGS).send(embed=embed)
        else:
            await interaction.response.send_message('Muted role not found.')
    else:
        await interaction.response.send_message('You do not have permission to use this command.')

@bot.tree.command(name='unmute', description='Unmute a user.', guild=GUILD)
@app_commands.describe(user='Unmute a user.')
async def unmute(interaction: discord.Interaction, user: discord.Member):
    if interaction.user.id == OWNER or discord.utils.get(interaction.user.roles, id=ADMIN):
        role = discord.utils.get(interaction.guild.roles, name='Muted')
        if role:
            await user.remove_roles(role)
            await interaction.response.send_message(f'{user} has been unmuted.')
            embed = discord.Embed(
                title="Unmute",
                description=f"{interaction.user} unmuted {user}.",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            await bot.get_channel(LOGS).send(embed=embed)
        else:
            await interaction.response.send_message('Muted role not found.')
    else:
        await interaction.response.send_message('You do not have permission to use this command.')

# Bot Events

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over the server 👀"))
    try:
        synced = await bot.tree.sync(guild=GUILD)
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")
        
    if not check_notices.is_running():
        check_notices.start()
        print("Started check_notices loop")
        
    embed = discord.Embed(
        title="Bot Status",
        description="Bot is online! 🟢",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    await bot.get_channel(LOGS).send(embed=embed)
    print("Bot is online! 🟢  ")

@bot.event
async def on_member_join(member):
    
    role = discord.utils.get(member.guild.roles, name='Member')
    if role:
        await member.add_roles(role)
    
    channel = discord.utils.get(member.guild.text_channels, name='welcome')
    if channel:
        embed = discord.Embed(title=f"Welcome to the server.",
                      description=f"{member.mention}Hope ya enjoy your stay!",
                      timestamp=datetime.now())
        embed.set_author(name="InfoBuddy")
        embed.set_image(url=f"{member.avatar.url}")
        embed.set_footer(text="InfoBuddy")
        await channel.send(embed=embed)
       
# Bot Periodic Tasks

# Check for new notices every 15 minutes that's 96 times a day
@tasks.loop(minutes=15)
async def check_notices():
    NOTICES = search_for_notice_updates()
    channel = discord.utils.get(bot.get_all_channels(), name='announcements')
    
    if channel and NOTICES:
        for notice in NOTICES:
            role = discord.utils.get(channel.guild.roles, name="Member")
            embed = discord.Embed(
                title=f"Notice!  📢",
                url="https://www.soa.ac.in/iter-news-and-events",
                description=f"[{notice[0]}]({urllib.parse.urljoin('https://www.soa.ac.in/', notice[1])})",
                colour=0xff0000,
                timestamp=datetime.now()
            )

            embed.set_author(
                name="InfoBuddy",
                icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCZHeOeTJ3UVPCVUlgN1BmTn0KUNcCRvDsYQ&s"
            )

            embed.set_footer(text="InfoBuddy")

            await channel.send(content=role.mention, embed=embed)
    
    save_notices(NOTICES)
    
    embed = discord.Embed(
        title="Notice Check",
        description="Checked Notice Board for new notices!",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    await bot.get_channel(LOGS).send(embed=embed)

# Bot Start
bot.run(TOKEN)