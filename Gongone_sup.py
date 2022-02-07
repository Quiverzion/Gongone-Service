import discord
from discord.ext import commands
from keep_alive import keep_alive
import os


bot = commands.Bot(command_prefix=';;',
                   status=discord.Status.online, intents=discord.Intents.all())


@bot.event
async def on_ready():
  print(f'Gongone.Service: Pay Script Runned on [{bot.user}]')


@bot.event
async def on_message(ctx):
  if ctx.channel.id == 937561123912306758:
    if ctx.content[0] == "!":
      await ctx.channel.send("전적이는 여기서! <#934776289884262441>", reference=ctx)
  
  ban_words = ['시발', 'ㅅㅂ']
  for i in range(len(ban_words)):
    for j in range(len(ctx.content)-len(ban_words[i])+1):
      if ctx.content[j:j+len(ban_words[i])-1] == ban_words[i]:
        if ctx.channel.id == 940161168486567957 or ctx.channel.id == 939841339816820766:
          return
        await ctx.channel.send("욕ㄴㄴ", reference=ctx)
        return



keep_alive()


bot.run(os.environ["token"])
