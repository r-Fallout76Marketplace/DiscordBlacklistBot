import os
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

import trello_blacklist

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')


async def on_error(event, *args, **kwargs):
    with open('DiscordBlacklistBot.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="mmmmmmmmmmmmiss ;)"))
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(f'{guild.name} (id: {guild.id})\n')


@bot.event
async def on_message(message):
    if message.channel.name == "blacklist_check":
        if message.author.bot:
            return
        if len(message.content) == 0:
            return
        else:
            user_name = message.content
            response = trello_blacklist.check_user_in_blacklist(user_name)
            await message.channel.send(response)

    await bot.process_commands(message)


bot.run(TOKEN)
