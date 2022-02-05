import discord
from discord.ext import commands
from keep_alive import keep_alive


bot = commands.Bot(command_prefix=';;',
                   status=discord.Status.online, intents=discord.Intents.all())


@bot.event
async def on_ready():
  print(f'Gongone.Service: Pay Script Runned on [{bot.user}]')

keep_alive()

def running(token):
  bot.run(token)
