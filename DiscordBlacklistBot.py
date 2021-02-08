import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
import discord

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
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You must include a user name to check when calling the blacklist bot.')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="mmmmmmmmmmmmiss ;)"))
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(f'{guild.name} (id: {guild.id})\n')


@bot.command(name='blacklist', help='Checks the blacklist for a named user.')
async def check_blacklist(ctx, *args):
    UserName = " ".join(args[:])

    response = trello_blacklist.check_user_in_blacklist(UserName)
    await ctx.send(response)


bot.run(TOKEN)
